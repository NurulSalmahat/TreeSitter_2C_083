; 1. Nama fungsi dan parameternya
(function_definition
  name: (identifier) @nama
  parameters: (parameters) @params)

; 2. Pemanggilan print()
(call
  function: (identifier) @fn
  arguments: (argument_list) @args
  (#eq? @fn "print"))

; 3. Import modul menggunakan import
(import_statement
  name: (dotted_name) @modul)

; 4. Import modul menggunakan from ... import ...
(import_from_statement
  module_name: (dotted_name) @modul)

; 5. Docstring sebagai pernyataan pertama dalam fungsi
(function_definition
  body: (block
    .
; Tanda titik di sini berarti node expression_statement harus menjadi anak pertama dari block. Jadi, query tidak mengambil sembarang string di dalam fungsi.
    (expression_statement
      (string) @docstring)))