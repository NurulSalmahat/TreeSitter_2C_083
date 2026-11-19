import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


# Percobaan 1: Kode sederhana
kode_sederhana = b"x = 1\n"

# Percobaan 2: Function
kode_function = b"""def sapa(nama):
    print("Halo", nama)
"""

# Percobaan 3: If/Else
kode_if_else = b"""if x > 0:
    print("positif")
else:
    print("non-positif")
"""

# Percobaan 4: Class dengan satu method
kode_class = b"""class Mahasiswa:
    def sapa(self):
        print("Halo Mahasiswa")
"""


# Menjalankan semua percobaan
percobaan = [
    ("Kode sederhana", kode_sederhana),
    ("Function", kode_function),
    ("If/Else", kode_if_else),
    ("Class", kode_class),
]

for nama, kode in percobaan:
    tree = parser.parse(kode)
    print(f"\n--- {nama} ---")
    print(tree.root_node)


# Percobaan 5: Named dan Anonymous Node
tree = parser.parse(kode_function)

print("\n--- Named dan Anonymous Node ---")

for c in tree.root_node.children[0].children:
    print(c.type, "bernama" if c.is_named else "anonim")

# Melihat anak-anak node parameters
parameters = tree.root_node.children[0].child_by_field_name("parameters")

print("\n--- Anak Node Parameters ---")

for c in parameters.children:
    print(c.type, "bernama" if c.is_named else "anonim")


# Percobaan 6: Error Recovery
# Tanda titik dua (:) sengaja dihapus
kode_rusak = b"""def sapa(nama)
    print("Halo", nama)
"""

tree = parser.parse(kode_rusak)

print("\n--- Error Recovery ---")
print(tree.root_node)
