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

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: {node.text.decode().strip()}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        nama = cap["nama"][0].text.decode()
        fungsi = cap["fungsi"][0]

        jumlah_baris = (
            fungsi.end_point[0] - fungsi.start_point[0] + 1
        )

        if jumlah_baris > 30:
            print(
                f"{path}: fungsi '{nama}' memiliki "
                f"{jumlah_baris} baris"
            )

    # Fitur 3 (TODO): file yang pohonnya mengandung error

for path in Path(sys.argv[1]).rglob("*.py"):
    cek_file(path)
