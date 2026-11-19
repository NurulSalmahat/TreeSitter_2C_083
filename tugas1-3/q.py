import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

query = Query(PY, pola)
hasil = QueryCursor(query).matches(tree.root_node)

for indeks, cap in hasil:

    if indeks == 0:
        nama = cap["nama"][0].text.decode()
        jumlah = cap["params"][0].named_child_count
        print(f"Fungsi: {nama}, Jumlah parameter: {jumlah}")

    elif indeks == 1:
        fn = cap["fn"][0]
        args = cap["args"][0]
        print(f"Pemanggilan: {fn.text.decode()}() "
              f"- Baris {fn.start_point[0] + 1}")

    elif indeks == 2 or indeks == 3:
        for node in cap["modul"]:
            print(f"Modul: {node.text.decode()} "
                  f"- Baris {node.start_point[0] + 1}")

    elif indeks == 4:
        node = cap["docstring"][0]
        print(f"Docstring: {node.text.decode()} "
              f"- Baris {node.start_point[0] + 1}")