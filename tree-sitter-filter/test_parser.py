
import tree_sitter_filter as tsfilter
from tree_sitter import Language, Parser

# Menghubungkan grammar filter ke Python
FILTER_LANGUAGE = Language(tsfilter.language())
parser = Parser(FILTER_LANGUAGE)

# Contoh query yang akan diuji
kode = b'status = "open"'

# Melakukan parsing
tree = parser.parse(kode)

# Menampilkan syntax tree
print(tree.root_node)
