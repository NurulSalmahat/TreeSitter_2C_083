# Pendeteksi TODO, Fungsi Panjang, dan Syntax Error (`cek.py`)

CLI sederhana berbasis **Tree-sitter** untuk memindai seluruh file Python (`*.py`) di dalam sebuah folder dan melaporkan tiga hal secara otomatis:

1. **Komentar `TODO` / `FIXME`** — melaporkan path file, nomor baris, dan isi komentarnya (menggunakan query Tree-sitter dengan predikat `#match?`).
2. **Fungsi yang panjang (> 30 baris)** — melaporkan nama fungsi dan jumlah barisnya berdasarkan `start_point` dan `end_point` dari node `function_definition`.
3. **File dengan syntax error** — mendeteksi `root_node.has_error` dan melaporkan nomor baris node pertama yang berstatus `is_error` atau `is_missing`.

## Prasyarat & Instalasi

Pastikan Python 3.10+ sudah terpasang, lalu instal dependensi berikut:

```bash
pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan

Dari folder `cek/`:

```bash
python cek.py <path_folder>
```

Atau dari root repositori:

```bash
python cek/cek.py <path_folder>
```

## Catatan Perilaku

- **Semua fungsi dihitung:** method di dalam `class` maupun fungsi bersarang (*nested function*) tetap dihitung karena sama-sama direpresentasikan sebagai node `function_definition` pada syntax tree Python.
- **Filter folder otomatis:** direktori `.git`, `venv`, `.venv`, `node_modules`, dan `__pycache__` dilewati secara otomatis.
- **Encoding aman:** decoding teks menggunakan `errors="replace"` untuk mencegah `UnicodeDecodeError` pada file dengan encoding non-UTF-8.

## Contoh Output

### 1. Pengujian pada Folder Uji Buatan (`cek/uji/`)

```bash
python cek/cek.py cek/uji/
```

Output:

```text
cek\uji\contoh_error.py: syntax error pada baris 1
cek\uji\contoh_fungsi.py: fungsi 'fungsi_panjang' memiliki 32 baris
cek\uji\contoh_todo.py:1: # TODO: tambahkan validasi input
cek\uji\contoh_todo.py:5: # FIXME: perbaiki proses pengurangan
```

### 2. Pengujian pada Repositori Python Nyata (`crud-extractor`, 17 file `.py`)

```bash
python cek/cek.py D:\TUBES_PLP2026_2C_083_085\crud-extractor
```

Output:

```text
D:\TUBES_PLP2026_2C_083_085\crud-extractor\evaluate.py: fungsi 'main' memiliki 32 baris
D:\TUBES_PLP2026_2C_083_085\crud-extractor\crud\cli.py: fungsi 'main' memiliki 59 baris
D:\TUBES_PLP2026_2C_083_085\crud-extractor\crud\lexer.py:110: # TODO(T3): dukung komentar blok /* ... */ (SPESIFIKASI.md bagian 2.3).
D:\TUBES_PLP2026_2C_083_085\crud-extractor\crud\lexer.py: fungsi '_scan_token' memiliki 61 baris
D:\TUBES_PLP2026_2C_083_085\crud-extractor\crud\parser.py:218: # TODO(T1): dukung INSERT INTO ... SELECT ... (SPESIFIKASI.md bagian 3 dan 5).
D:\TUBES_PLP2026_2C_083_085\crud-extractor\crud\parser.py: fungsi '_primary' memiliki 32 baris
D:\TUBES_PLP2026_2C_083_085\crud-extractor\crud\resolver.py:183: # TODO(T2): kolom tanpa qualifier (SPESIFIKASI.md bagian 4.3).
```

### Verifikasi Manual (2 File Acak)

| File | Hasil `cek.py` | Pengecekan Manual | Status |
| --- | --- | --- | --- |
| `crud/resolver.py` (201 baris) | 1 TODO (baris 183), 0 fungsi > 30 baris, 0 syntax error | Baris 183 berisi `# TODO(T2)...`; fungsi terpanjang `_expr` & `_column` masing-masing 27 baris; sintaks valid | Cocok |
| `crud/lexer.py` (211 baris) | 1 TODO (baris 110), `_scan_token` 61 baris, 0 syntax error | Baris 110 berisi `# TODO(T3)...`; `_scan_token` baris 99–159 (`159 - 99 + 1 = 61` baris); sintaks valid | Cocok |
