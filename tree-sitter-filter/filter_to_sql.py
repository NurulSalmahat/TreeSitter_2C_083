# hanya mencakup kasus AND belum ada OR, NOT, IN, CONTAINS, dll.
import tree_sitter_filter as tsfilter
from tree_sitter import Language, Parser

FILTER_LANGUAGE = Language(tsfilter.language())
parser = Parser(FILTER_LANGUAGE)


def compile_node(node, params):
    # Mengubah ekspresi perbandingan
    if node.type == "comparison":
        field_node = node.child_by_field_name("field")
        value_node = node.child_by_field_name("value")

        # Operator berada di antara field dan value
        operator_node = node.children[1]

        field = field_node.text.decode()
        operator = operator_node.text.decode()
        raw_value = value_node.text.decode()

        # Mengubah tipe nilai sesuai jenisnya
        if value_node.type == "string":
            value = raw_value[1:-1]
        elif value_node.type == "number":
            value = float(raw_value) if "." in raw_value else int(raw_value)
        else:
            value = raw_value == "true"

        params.append(value)

        return f"{field} {operator} ?"

    # Mengubah ekspresi AND
    elif node.type == "and_expression":
        left = node.child_by_field_name("left")
        right = node.child_by_field_name("right")

        left_sql = compile_node(left, params)
        right_sql = compile_node(right, params)

        return f"({left_sql} AND {right_sql})"

    raise ValueError(f"Node belum didukung: {node.type}")


# Membaca file filter
with open("contoh.filter", "rb") as file:
    source = file.read()

tree = parser.parse(source)

if tree.root_node.has_error:
    raise ValueError("Query filter memiliki kesalahan sintaks!")

params = []
where_sql = compile_node(tree.root_node.named_children[0], params)

print("SQL:")
print("WHERE", where_sql)

print("\nParameters:")
print(params)
