import bpy
import os
import re
import subprocess
from bpy.props import StringProperty
from io_scs_tools.utils import path as _path_utils
from io_scs_tools.utils import get_scs_globals as _get_scs_globals

# Operator untuk membuka folder
class SCS_OT_open_sii_folder(bpy.types.Operator):
    """Buka folder lokasi file .sii yang baru dibuat"""
    bl_idname = "scs.open_sii_folder"
    bl_label = "Open Folder"

    folder_path = bpy.props.StringProperty()

    def execute(self, context):
        if self.folder_path and os.path.isdir(self.folder_path):
            try:
                subprocess.Popen(["explorer", os.path.normpath(self.folder_path)])
            except Exception as e:
                self.report({'ERROR'}, "Gagal membuka folder: {}".format(e))
                return {'CANCELLED'}
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Folder tidak ditemukan atau path kosong.")
            return {'CANCELLED'}

class SCS_OT_batch_generate_sii(bpy.types.Operator):
    """Generate file .sii untuk semua object terpilih"""
    bl_idname = "scs.batch_generate_sii"
    bl_label = "Batch Generate .sii"

    def execute(self, context):
        count = 0
        for obj in context.selected_objects:
            if hasattr(obj, "scs_props") and obj.scs_props.empty_object_type == 'SCS_Root':
                context.scene.objects.active = obj
                result = bpy.ops.scs.generate_sii()
                if 'FINISHED' in result:
                    count += 1
        self.report({'INFO'}, "Batch generate selesai: {} file dibuat.".format(count))
        return {'FINISHED'}

class SCS_OT_SelectInteriorModelPath(bpy.types.Operator):
    """Pilih file .pim untuk Interior Model (khusus SII Generator, path relatif dari SCS Project Base)"""
    bl_idname = "scs.select_interior_model_path"
    bl_label = "Pilih Interior Model Path"
    bl_description = "Pilih file .pim untuk interior model (relatif dari SCS Project Base)"

    filepath = StringProperty(
        name="File Path",
        description="Pilih file .pim untuk interior model",
        subtype='FILE_PATH',
    )
    filter_glob = StringProperty(
        default="*.pim",
        options={'HIDDEN'}
    )

    def execute(self, context):
        scs_globals = _get_scs_globals()
        if not scs_globals.scs_project_path:
            self.report({'ERROR'}, "SCS Project Base Path belum diatur di preferensi Addon.")
            return {'CANCELLED'}
        if _path_utils.startswith(self.filepath, scs_globals.scs_project_path):
            rel_path = _path_utils.relative_path(scs_globals.scs_project_path, self.filepath)
            base, _ = os.path.splitext(rel_path)
            rel_path = base + ".pmd"
            context.active_object.sii_generator_props.interior_model_custom_path = rel_path
        else:
            context.active_object.sii_generator_props.interior_model_custom_path = "//"
            self.report({'ERROR'}, "Path yang dipilih di luar SCS Project Base Path, path direset.")
            return {'CANCELLED'}
        return {'FINISHED'}

    def invoke(self, context, event):
        scs_path = _get_scs_globals().scs_project_path
        if os.path.isdir(scs_path):
            self.filepath = os.path.join(scs_path, "")
        else:
            self.filepath = ""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class SCS_OT_add_sii_item(bpy.types.Operator):
    bl_idname = "scs.add_sii_item"
    bl_label = "Tambah Item"
    prop_name = bpy.props.StringProperty()

    def execute(self, context):
        props = context.active_object.sii_generator_props
        getattr(props, self.prop_name).add()
        return {'FINISHED'}

class SCS_OT_remove_sii_item(bpy.types.Operator):
    bl_idname = "scs.remove_sii_item"
    bl_label = "Hapus Item"
    prop_name = bpy.props.StringProperty()
    index = bpy.props.IntProperty()

    def execute(self, context):
        props = context.active_object.sii_generator_props
        collection = getattr(props, self.prop_name)
        if 0 <= self.index < len(collection):
            collection.remove(self.index)
        return {'FINISHED'}

class SCS_OT_ClearSiiProperty(bpy.types.Operator):
    """Mengosongkan nilai dari properti Sii Generator yang dipilih"""
    bl_idname = "scs.clear_sii_property"
    bl_label = "Clear Input"
    bl_options = {'UNDO'}

    property_name = bpy.props.StringProperty()

    def execute(self, context):
        sii_props = context.active_object.sii_generator_props
        if hasattr(sii_props, self.property_name):
            prop = sii_props.bl_rna.properties.get(self.property_name)
            if prop.type == 'STRING':
                setattr(sii_props, self.property_name, "")
            elif prop.type == 'INT':
                setattr(sii_props, self.property_name, prop.default)
        return {'FINISHED'}

def build_sii_content(sii_props, root_object, exterior_model_path):
    final_variant = ""
    if hasattr(root_object, "scs_object_variant_inventory") and root_object.scs_object_variant_inventory:
        if sii_props.variant_enum != 'MANUAL_INPUT':
            final_variant = sii_props.variant_enum
        else:
            final_variant = sii_props.variant_manual
    else:
        final_variant = sii_props.variant_manual
    final_look = ""
    if hasattr(root_object, "scs_object_look_inventory") and root_object.scs_object_look_inventory:
        if sii_props.look_enum != 'MANUAL_INPUT':
            final_look = sii_props.look_enum
        else:
            final_look = sii_props.look_manual
    else:
        final_look = sii_props.look_manual

    optional_lines = []
    if getattr(sii_props, "use_interior_model_custom_path", False):
        interior_model_path = getattr(sii_props, "interior_model_custom_path", "").strip()
        if interior_model_path and interior_model_path != "//":
            normalized_interior_path = "/" + interior_model_path.lstrip("/\\")
            base, _ = os.path.splitext(normalized_interior_path)
            normalized_interior_path = base + ".pmd"
            optional_lines.append('\tinterior_model: "{}"'.format(normalized_interior_path))
    if final_variant:
        optional_lines.append("\tvariant: {}".format(final_variant))
    if final_look:
        optional_lines.append("\tlook: {}".format(final_look))
    if optional_lines and (sii_props.suitable_for or sii_props.defaults or sii_props.conflict_with or sii_props.overrides):
        optional_lines.append("")

    has_optional = (
        (sii_props.suitable_for and any(item.value.strip() for item in sii_props.suitable_for)) or
        (sii_props.defaults and any(item.value.strip() for item in sii_props.defaults)) or
        (sii_props.conflict_with and any(item.value.strip() for item in sii_props.conflict_with)) or
        (sii_props.overrides and any(item.value.strip() for item in sii_props.overrides))
    )
    if has_optional:
        optional_lines.append("")

    if sii_props.suitable_for:
        for item in sii_props.suitable_for:
            if item.value.strip():
                optional_lines.append('\tsuitable_for[]: "{}"'.format(item.value.strip()))
        if any(item.value.strip() for item in sii_props.suitable_for):
            optional_lines.append("")
    if sii_props.defaults:
        for item in sii_props.defaults:
            if item.value.strip():
                optional_lines.append('\tdefaults[]: "{}"'.format(item.value.strip()))
        if any(item.value.strip() for item in sii_props.defaults):
            optional_lines.append("")
    if sii_props.conflict_with:
        for item in sii_props.conflict_with:
            if item.value.strip():
                optional_lines.append('\tconflict_with[]: "{}"'.format(item.value.strip()))
        if any(item.value.strip() for item in sii_props.conflict_with):
            optional_lines.append("")
    if sii_props.overrides:
        for item in sii_props.overrides:
            if item.value.strip():
                optional_lines.append('\toverrides[]: "{}"'.format(item.value.strip()))

    optional_block = ""
    if optional_lines:
        optional_block = "\n" + "\n".join(optional_lines)

    sii_content = (
        "SiiNunit\n"
        "{{\n"
        "accessory_addon_data : {def_name}.{truck_base}.{locator}\n"
        "{{\n"
        "\tname: \"{display_name}\"\n"
        "\tprice: {price}\n"
        "\tunlock: {unlock}\n"
        "\ticon: \"{icon_name}\"\n"
        "\texterior_model: \"{exterior_model_path}\"{optional_block}\n"
        "}}\n"
        "}}\n"
        "# Generated by SII Maker | Blender Addon by @rw_aji\n"
    ).format(
        def_name=sii_props.definition_name,
        truck_base=sii_props.truck_base_name,
        locator=sii_props.accessory_locator_name,
        display_name=sii_props.display_name,
        price=sii_props.price,
        unlock=sii_props.unlock,
        icon_name=sii_props.icon_name if sii_props.icon_name else '',
        exterior_model_path=exterior_model_path,
        optional_block=optional_block
    )
    return sii_content

class SCS_OT_generate_sii(bpy.types.Operator):
    """Membuat file def .sii untuk SCS Root Object yang dipilih"""
    bl_idname = "scs.generate_sii"
    bl_label = "Buat File .sii"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and hasattr(obj, "scs_props") and obj.scs_props.empty_object_type == 'SCS_Root'

    def execute(self, context):
        sii_props = context.active_object.sii_generator_props
        root_object = context.active_object

        export_path_full = _path_utils.get_custom_scs_root_export_path(root_object)

        if not all([sii_props.sii_filename, sii_props.definition_name, sii_props.display_name]):
            self.report({'ERROR'}, "Harap isi Nama File, Def, dan Display.")
            return {'CANCELLED'}

        if not export_path_full:
            self.report({'ERROR'}, "Export Path belum diatur. Harap isi di panel.")
            return {'CANCELLED'}

        project_base_path = _get_scs_globals().scs_project_path
        if not project_base_path:
            self.report({'ERROR'}, "SCS Project Base Path belum diatur di preferensi Addon.")
            return {'CANCELLED'}

        export_path_relative = export_path_full.replace(project_base_path, "").strip("/\\")
        model_path = export_path_relative.replace("\\", "/")
        exterior_model_path = "/{}/{}.pmd".format(model_path, root_object.name)

        sii_content = build_sii_content(sii_props, root_object, exterior_model_path)

        def_path_part = os.path.join("def", "vehicle", "truck", sii_props.truck_base_name)

        if sii_props.def_type == 'accessory':
            full_path = os.path.join(project_base_path, def_path_part, "accessory", sii_props.accessory_locator_name)
        else:
            full_path = os.path.join(project_base_path, def_path_part, sii_props.def_type)

        try:
            if not os.path.exists(full_path):
                os.makedirs(full_path)
        except OSError as e:
            self.report({'ERROR'}, "Tidak dapat membuat direktori: {}".format(e))
            return {'CANCELLED'}

        sii_file_name = sii_props.sii_filename
        if not sii_file_name.endswith(".sii"):
            sii_file_name += ".sii"

        file_path = os.path.join(full_path, sii_file_name)

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(sii_content)
        except IOError as e:
            self.report({'ERROR'}, "Gagal menulis file: {}".format(e))
            return {'CANCELLED'}

        # === LOGIKA TIMER DIHAPUS, DIGANTI DENGAN YANG LEBIH SEDERHANA ===
        # Cukup aktifkan tombol dan simpan path file. Tombol akan tetap aktif.
        sii_props.last_generated_file = file_path
        sii_props.is_open_folder_enabled = True
        # === AKHIR BLOK YANG DIPERBARUI ===

        self.report({'INFO'}, "File berhasil dibuat: {}".format(file_path))
        return {'FINISHED'}

class SCS_OT_preview_sii(bpy.types.Operator):
    """Preview isi file .sii yang akan di-generate"""
    bl_idname = "scs.preview_sii"
    bl_label = "Preview SII"

    sii_content = bpy.props.StringProperty()

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        sii_props = context.active_object.sii_generator_props
        root_object = context.active_object

        export_path_full = _path_utils.get_custom_scs_root_export_path(root_object)
        project_base_path = _get_scs_globals().scs_project_path
        if export_path_full and project_base_path:
            export_path_relative = export_path_full.replace(project_base_path, "").strip("/\\")
            model_path = export_path_relative.replace("\\", "/")
            exterior_model_path = "/{}/{}.pmd".format(model_path, root_object.name)
        else:
            exterior_model_path = ""
        self.sii_content = build_sii_content(sii_props, root_object, exterior_model_path)
        return context.window_manager.invoke_popup(self, width=400)

    def draw(self, context):
        for line in self.sii_content.splitlines():
            self.layout.label(text=line.replace('\t', '    '))

def is_valid_ets2_name(name, maxlen=12):
    if not name or len(name) > maxlen:
        return False
    if not re.match(r'^[a-z_][a-z0-9_]*$', name):
        return False
    return True

# FUNGSI disable_button_callback DIHAPUS KARENA TIDAK LAGI DIGUNAKAN

# Daftarkan semua operator yang ada di file ini
classes = (
    SCS_OT_open_sii_folder,
    SCS_OT_batch_generate_sii,
    SCS_OT_SelectInteriorModelPath,
    SCS_OT_add_sii_item,
    SCS_OT_remove_sii_item,
    SCS_OT_ClearSiiProperty,
    SCS_OT_generate_sii,
    SCS_OT_preview_sii,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass