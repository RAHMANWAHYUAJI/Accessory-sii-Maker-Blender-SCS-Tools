import re
import bpy

# === FUNGSI VALIDASI BARU (LEBIH CANGGIH) ===
def validate_ets2_name(self, context):
    name = getattr(self, "definition_name", "")
    if name:
        segments = []
        current = ""
        for char in name:
            if char == ".":
                if current:
                    segments.append(current)
                    current = ""
            else:
                if re.match(r'[a-z0-9_]', char.lower()):
                    if len(current) < 12:
                        current += char.lower()
        if current:
            segments.append(current)
        for i, seg in enumerate(segments):
            if seg and seg[0].isdigit():
                segments[i] = "_" + seg
        fixed = ".".join(segments)
        self["definition_name"] = fixed

# === FUNGSI VALIDASI BARU UNTUK NAMA FILE ===
def validate_sii_filename(self, context):
    name = getattr(self, "sii_filename", "")
    if name and not re.match(r'^[a-z_][a-z0-9_.]*$', name):
        clean = re.sub(r'[^a-z0-9_]', '', name.lower())
        if clean and clean[0].isdigit():
            clean = '_' + clean
        self["sii_filename"] = clean

# FUNGSI UNTUK MEMBUAT DAFTAR ITEM DROPDOWN SECARA DINAMIS
def get_variant_items(self, context):
    items = []
    obj = context.active_object
    if obj and hasattr(obj, "scs_object_variant_inventory") and obj.scs_object_variant_inventory:
        for variant in obj.scs_object_variant_inventory:
            # Menggunakan .format() untuk kompatibilitas Python 3.5
            items.append((variant.name, variant.name, "Gunakan variant '{}' yang sudah ada".format(variant.name)))
    items.append(("MANUAL_INPUT", "(Ketik Manual)", "Gunakan input teks manual"))
    return items

def get_look_items(self, context):
    items = []
    obj = context.active_object
    if obj and hasattr(obj, "scs_object_look_inventory") and obj.scs_object_look_inventory:
        for look in obj.scs_object_look_inventory:
            # Menggunakan .format() untuk kompatibilitas Python 3.5
            items.append((look.name, look.name, "Gunakan look '{}' yang sudah ada".format(look.name)))
    items.append(("MANUAL_INPUT", "(Ketik Manual)", "Gunakan input teks manual"))
    return items

class SiiStringItem(bpy.types.PropertyGroup):
    pass

class SiiGeneratorProperties(bpy.types.PropertyGroup):
    """Properties for the SCS .sii File Generator"""
    pass

# Assign properties setelah definisi class (gaya Blender 2.79)
SiiStringItem.value = bpy.props.StringProperty(
    name="Value",
    description=(
        "Contoh :\n"
        "Suitable For & Conflict With = defname.base_mod.chassis\n"
        "Defaults & Overrides = /def/vehicle/truck/example/accessory/example1.sii"
    )
)

SiiGeneratorProperties.sii_filename = bpy.props.StringProperty(
    name="Nama File",
    description="Nama untuk file .sii. Contoh: bumper_satu",
    update=validate_sii_filename # <-- DITAMBAHKAN
)
SiiGeneratorProperties.def_type = bpy.props.EnumProperty(
    name="Tipe",
    items=[('accessory', 'Accessory', ''), ('cabin', 'Cabin', ''), ('chassis', 'Chassis', '')],
    default='accessory'
)
SiiGeneratorProperties.definition_name = bpy.props.StringProperty(
    name="Nama Def",
    description="Nama unik untuk def (Maksimal 12 karakter per segmen). \nContoh: bumper1\nContoh lain: bumper1.walawe.wokwok",
    # maxlen=12 dihapus karena validasi baru lebih baik
    update=validate_ets2_name
)
SiiGeneratorProperties.truck_base_name = bpy.props.StringProperty(
    name="Truck Base Name", description="Nama dasar truk. \nContoh: scania.s_2016",
    update=validate_ets2_name
)
SiiGeneratorProperties.accessory_locator_name = bpy.props.StringProperty(
    name="Accessory Locator", description="Nama slot/locator aksesori. \nContoh: f_bumper",
    update=validate_ets2_name
)
SiiGeneratorProperties.display_name = bpy.props.StringProperty(
    name="Nama Display",
    description="Nama yang akan ditampilkan di dalam game. \nContoh: My Bumper 1"
)
SiiGeneratorProperties.icon_name = bpy.props.StringProperty(
    name="Nama Ikon",
    description="Nama ikon (.dds) yang akan digunakan. \nContoh: ico_bumper1"
)
SiiGeneratorProperties.price = bpy.props.IntProperty(
    name="Price", description="Harga aksesori di dalam game", default=100, min=1
)
SiiGeneratorProperties.unlock = bpy.props.IntProperty(
    name="Unlock Level", description="Level yang dibutuhkan untuk membuka aksesori", default=1, min=1
)
SiiGeneratorProperties.variant_enum = bpy.props.EnumProperty(
    name="Variant", items=get_variant_items, description="Pilih Variant yang sudah ada pada Root Object"
)
SiiGeneratorProperties.look_enum = bpy.props.EnumProperty(
    name="Look", items=get_look_items, description="Pilih Look yang sudah ada pada Root Object"
)
SiiGeneratorProperties.variant_manual = bpy.props.StringProperty(
    name="Variant Manual", description="Ketik nama variant secara manual. \nContoh: default"
)
SiiGeneratorProperties.look_manual = bpy.props.StringProperty(
    name="Look Manual", description="Ketik nama look secara manual. \nContoh: default"
)
SiiGeneratorProperties.interior_model_custom_path = bpy.props.StringProperty(
    name="Interior Model Path",
    description="Klik open file untuk mencari .pim interior_model yang ada dan otomatis akan menjadi .pmd\nCentang 'Gunakan Path Interior Model' untuk mengaktifkan."
)
SiiGeneratorProperties.use_interior_model_custom_path = bpy.props.BoolProperty(
    name="Gunakan Path Interior Model",
    description="Aktifkan untuk menggunakan path interior model manual.",
    default=False # <-- DITAMBAHKAN
)

# === PROPERTI BARU UNTUK TOMBOL "BUKA FOLDER" ===
SiiGeneratorProperties.last_generated_file = bpy.props.StringProperty(
    name="Last Generated File",
    description="Path file .sii terakhir yang dibuat",
    default=""
)
SiiGeneratorProperties.is_open_folder_enabled = bpy.props.BoolProperty(
    name="Is Open Folder Enabled",
    description="Saklar untuk mengaktifkan tombol 'Buka Folder'",
    default=False
)
# === AKHIR PROPERTI BARU ===

SiiGeneratorProperties.suitable_for = bpy.props.CollectionProperty(type=SiiStringItem)
SiiGeneratorProperties.defaults = bpy.props.CollectionProperty(type=SiiStringItem)
SiiGeneratorProperties.conflict_with = bpy.props.CollectionProperty(type=SiiStringItem)
SiiGeneratorProperties.overrides = bpy.props.CollectionProperty(type=SiiStringItem)

def register():
    bpy.utils.register_class(SiiStringItem)
    bpy.utils.register_class(SiiGeneratorProperties)
    bpy.types.Object.sii_generator_props = bpy.props.PointerProperty(type=SiiGeneratorProperties)

def unregister():
    del bpy.types.Object.sii_generator_props
    bpy.utils.unregister_class(SiiGeneratorProperties)
    bpy.utils.unregister_class(SiiStringItem)