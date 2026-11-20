import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')

Q_FUNGSI = Query(
    PY,
    "(function_definition name: (identifier) @nama) @fungsi"
)

ABAIKAN_FOLDER = {".git", "venv", ".venv", "node_modules", "__pycache__"}

def cari_error(node):
    if node.is_error or node.is_missing:
        return node

    for child in node.children:
        hasil = cari_error(child)
        if hasil is not None:
            return hasil

    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        nama = cap["nama"][0].text.decode(errors="replace")
        fungsi = cap["fungsi"][0]

        jumlah_baris = (
            fungsi.end_point[0] - fungsi.start_point[0] + 1
        )

        if jumlah_baris > 30:
            print(
                f"{path}: fungsi '{nama}' memiliki "
                f"{jumlah_baris} baris"
            )

    # Fitur 3: file yang memiliki syntax error
    if tree.root_node.has_error:
        error = cari_error(tree.root_node)

        if error is not None:
            print(
                f"{path}: syntax error pada baris "
                f"{error.start_point[0] + 1}"
            )

for path in Path(sys.argv[1]).rglob("*.py"):
    if any(part in ABAIKAN_FOLDER for part in path.parts):
        continue
    cek_file(path)
