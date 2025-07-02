import bpy
import os
from io_scs_tools.utils import path as _path_utils
from io_scs_tools.utils import get_scs_globals as _get_scs_globals

LABELS = {
    'ID': {
        'attr_box': "Atribut Tambahan:",
        'sii_filename': "Nama File .sii",
        'def_type': "Tipe Def",
        'accessory_addon_data': "accessory_addon_data :",
        'definition_name': "Nama Definisi",
        'truck_base_name': "Nama Truck Base",
        'accessory_locator_name': "Nama Locator",
        'display_name': "Nama Display",
        'unlock': "Level Buka",
        'price': "Harga",
        'icon_name': "Nama Ikon",
        'variant': "Variant",
        'look': "Look",
        'suitable_for': "Suitable For",
        'defaults': "Defaults",
        'conflict_with': "Conflict With",
        'overrides': "Overrides",
        'exterior_model': "exterior_model (Otomatis):",
        'interior_model': "interior_model:",
        'root_required': "Pilih sebuah SCS Root Object",
        'preview': "Preview SII",
        'batch': "Buat .SII Semua yg diseleksi",
        'generate': "BUAT .SII",
        'open_folder': "Buka Folder Tujuan",
    },
    'EN': {
        'attr_box': "Additional Attributes:",
        'sii_filename': ".sii File Name",
        'def_type': "Def Type",
        'accessory_addon_data': "accessory_addon_data :",
        'definition_name': "Definition Name",
        'truck_base_name': "Truck Base Name",
        'accessory_locator_name': "Locator Name",
        'display_name': "Display Name",
        'unlock': "Unlock Level",
        'price': "Price",
        'icon_name': "Icon Name",
        'variant': "Variant",
        'look': "Look",
        'suitable_for': "Suitable For",
        'defaults': "Defaults",
        'conflict_with': "Conflict With",
        'overrides': "Overrides",
        'exterior_model': "exterior_model (Auto):",
        'interior_model': "interior_model:",
        'root_required': "Select an SCS Root Object",
        'preview': "Preview SII",
        'batch': "Batch Generate",
        'generate': "Generate SII",
        'open_folder': "Open Destination Folder",
    }
}

class SCS_PT_sii_generator(bpy.types.Panel):
    """Membuat panel di 3D View untuk .sii generator"""
    bl_label = "SCS .sii Generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'SCS Tools'
    bl_context = "objectmode"

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        self.layout.label(text="", icon='FILE_TEXT')

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        lang = context.scene.scs_tools_language
        L = LABELS[lang]
        props = obj.sii_generator_props

        is_valid_root = obj and hasattr(obj, "scs_props") and obj.scs_props.empty_object_type == 'SCS_Root'

        if not is_valid_root:
            layout.label(text=L['root_required'], icon='INFO')
            return
            
        # Tombol bahasa
        layout.row().prop(context.scene, "scs_tools_language", expand=True)

        sii_props = context.active_object.sii_generator_props
        

        
        def draw_collection_with_add_remove(layout, props, prop_name, label):
            col = layout.column(align=True)
            # Baris label dan tombol tambah di kanan
            header = col.row(align=True)
            header.label(text=label)
            op = header.operator("scs.add_sii_item", text="", icon='ADD', emboss=True)
            op.prop_name = prop_name

            collection = getattr(props, prop_name)
            for idx, item in enumerate(collection):
                row = col.row(align=True)
                row.prop(item, "value", text="")
                op = row.operator("scs.remove_sii_item", text="", icon='X', emboss=True)
                op.prop_name = prop_name
                op.index = idx
            

        def draw_prop_with_clear(layout, prop_name, label):
            row = layout.row(align=True)
            row.label(text=label)
            row.prop(sii_props, prop_name, text="")
            op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
            op.property_name = prop_name

        disable_all = sii_props.def_type in {'chassis', 'cabin'}

        main_box = layout.box()
        col = main_box.column()

        draw_prop_with_clear(col, "sii_filename", L['sii_filename'])

        # Def Type selalu aktif
        col.prop(sii_props, "def_type", expand=True)
        col.separator()

        # Bagian bawah ikut disable_all
        sub_col = col.column()
        sub_col.enabled = not disable_all
        if sii_props.def_type == 'accessory':
            pass  # Tidak melakukan apa-apa untuk aksesori
        elif sii_props.def_type == 'cabin':
            col.separator()
            box = col.box()
            box.label(text="^_^ Segera Hadir ^_^", icon='INFO')
        elif sii_props.def_type == 'chassis':
            col.separator()
            box = col.box()
            box.label(text="^_^ Segera Hadir ^_^", icon='INFO')

        # Gabungkan tiga inputan dalam satu baris, beri jarak antar elemen
        sub_col.label(text=L['accessory_addon_data'])
        row = sub_col.row(align=True)
        row.prop(sii_props, "definition_name", text="")
        op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
        op.property_name = "definition_name"

        row.separator(factor=0.3)  # Jarak antar elemen

        row.prop(sii_props, "truck_base_name", text="")
        op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
        op.property_name = "truck_base_name"

        row.separator(factor=0.3)  # Jarak antar elemen

        row.prop(sii_props, "accessory_locator_name", text="")
        op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
        op.property_name = "accessory_locator_name"
        sub_col.separator(factor=0.5)

        
        data_box = layout.box()
        col = data_box.column(align=True)
        draw_prop_with_clear(col, "display_name", L['display_name'])
        col.separator(factor=0.5)
        
        row = col.row(align=True)
        row.label(text=L['unlock'])
        row.prop(sii_props, "unlock", text="")
        col.separator(factor=0.5)
        
        row = col.row(align=True)
        row.label(text=L['price'])
        row.prop(sii_props, "price", text="")
        col.separator(factor=0.5)
        draw_prop_with_clear(col, "icon_name", L['icon_name'])
        col.separator(factor=0.5)
        
        
        row = col.row(align=True)
        row.label(text=L['variant'])
        has_variants = hasattr(obj, "scs_object_variant_inventory") and obj.scs_object_variant_inventory
        
        if has_variants:
            row.prop(sii_props, "variant_enum", text="")
            if sii_props.variant_enum == 'MANUAL_INPUT':
                row.prop(sii_props, "variant_manual", text="")
                op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
                op.property_name = "variant_manual"
        else:
            row.prop(sii_props, "variant_manual", text="")
            op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
            op.property_name = "variant_manual"
            
        col.separator(factor=0.5)
        
        # Look
        row = col.row(align=True)
        row.label(text=L['look'])
        has_looks = hasattr(obj, "scs_object_look_inventory") and obj.scs_object_look_inventory
        
        if has_looks:
            row.prop(sii_props, "look_enum", text="")
            if sii_props.look_enum == 'MANUAL_INPUT':
                row.prop(sii_props, "look_manual", text="")
                op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
                op.property_name = "look_manual"
        else:
            row.prop(sii_props, "look_manual", text="")
            op = row.operator("scs.clear_sii_property", text="", icon='X', emboss=True)
            op.property_name = "look_manual"
        # Model Path Box
        path_box = layout.box()
        path_box.label(text=L['exterior_model'])

        final_path = _path_utils.get_custom_scs_root_export_path(obj)

        path_box.enabled = not disable_all

        # exterior_model
        row = path_box.row(align=True)
        row.prop(obj.scs_props, 'scs_root_object_allow_custom_path', text="")

        sub = row.row(align=True)
        sub.enabled = obj.scs_props.scs_root_object_allow_custom_path and not disable_all
        sub.prop(obj.scs_props, 'scs_root_object_export_filepath', text="")
        props = sub.operator('scene.scs_tools_select_dir_inside_base', text="", icon='FILEBROWSER')
        props.type = "GameObjectExportPath"

        # interior_model
        path_box.label(text=L['interior_model'])

        row = path_box.row(align=True)
        row.prop(context.active_object.sii_generator_props, 'use_interior_model_custom_path', text="")

        sub = row.row(align=True)
        sub.enabled = context.active_object.sii_generator_props.use_interior_model_custom_path
        sub.prop(context.active_object.sii_generator_props, 'interior_model_custom_path', text="")
        sub.operator('scs.select_interior_model_path', text="", icon='FILEBROWSER')



        # === Tambahkan box baru untuk Atribut Tambahan di bawah model ===
        attr_box = layout.box()
        attr_box.label(text=L['attr_box'])

        draw_collection_with_add_remove(attr_box, sii_props, "suitable_for", L['suitable_for'])
        draw_collection_with_add_remove(attr_box, sii_props, "defaults", L['defaults'])
        draw_collection_with_add_remove(attr_box, sii_props, "conflict_with", L['conflict_with'])
        draw_collection_with_add_remove(attr_box, sii_props, "overrides", L['overrides'])

        row = layout.row()
        row.operator("scs.preview_sii", text=L['preview'], icon='TEXT')
        row = layout.row()
        row.operator("scs.batch_generate_sii", text=L['batch'], icon='FILE_TICK')
        
        # === BLOK KODE BARU DIMULAI DI SINI ===
        row = layout.row()

        # Ikatkan kondisi enabled pada baris ini ke properti saklar kita
        row.enabled = sii_props.is_open_folder_enabled

        # Operator tombolnya tetap sama
        op = row.operator("scs.open_sii_folder", text=L['open_folder'], icon='FILE_FOLDER')

        # Penting: tetap berikan path folder, karena tombol membutuhkannya saat aktif
        if sii_props.last_generated_file:
            folder = os.path.dirname(sii_props.last_generated_file)
            op.folder_path = folder
        # === BLOK KODE BARU SELESAI ===
        
        layout.separator()

        row = layout.row()
        row.scale_y = 2
        row.enabled = bool(final_path) and not disable_all
        row.operator("scs.generate_sii", text=L['generate'])

classes = (SCS_PT_sii_generator,)


def register():
    bpy.types.Scene.scs_tools_language = bpy.props.EnumProperty(
        name="Language",
        description="Pilih bahasa UI",
        items=[
            ('ID', "ID", "Bahasa Indonesia"),
            ('EN', "EN", "English"),
        ],
        default='ID'
    )
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    del bpy.types.Scene.scs_tools_language
    for c in classes:
        try:
            bpy.utils.unregister_class(c)
        except RuntimeError:
            pass  # Sudah tidak terdaftar
