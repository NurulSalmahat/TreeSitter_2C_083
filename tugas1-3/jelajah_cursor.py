
import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


def jelajah_cursor(cursor, kedalaman=0):
    node = cursor.node

    baris, kolom = node.start_point
    field = cursor.field_name
    label = f"{field}: " if field else ""

    if node.is_named:
        print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

    # Masuk ke anak pertama
    if cursor.goto_first_child():

        while True:
            # Telusuri hanya node yang bernama
            if cursor.node.is_named:
                jelajah_cursor(cursor, kedalaman + 1)

            # Pindah ke saudara berikutnya
            if not cursor.goto_next_sibling():
                break

        # Kembali ke parent
        cursor.goto_parent()


with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())

cursor = tree.walk()
jelajah_cursor(cursor)
