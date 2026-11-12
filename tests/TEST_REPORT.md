# Raport testów

Projekt: Universal File Converter  
Data: 12.11.2026  
Python 3.13, pytest 9.2.0 (Windows)

Aplikacja: `python main.py`  
Testy automatyczne: `python -m pytest -q` (z katalogu głównego projektu)

Dane wejściowe: `samples/`  
Logi testów: `logs/tests.log`  
Logi aplikacji (GUI): `logs/app.log`

---

## 1. Testy automatyczne

Uruchomienie dało wynik:

```
20 passed in 1.42s
```

Rozkład (liczba testów, nie procenty z paska pytest):

| Plik | Ile testów | Wynik |
|---|---:|---|
| `test_converters.py` | 8 | 8 passed |
| `test_utils.py` | 6 | 6 passed |
| `test_validate.py` | 6 | 6 passed |
| **Razem** | **20** | **20 passed** |

Uwaga: napisy `[40%]`, `[70%]`, `[100%]` w logu pytest to tylko postęp wykonania
(ile testów już zbiegło z 20). To nie są osobne „procenty zaliczenia”.
8/20 ≈ 40%, potem 14/20 ≈ 70%, na końcu 20/20 = 100%.

### Log pliku `logs/tests.log`

Każdy test jest zapisany osobno. W ostatnim uruchomieniu wszystkie mają status
**PASSED**, sesja kończy się `exitstatus=0`:

```
[2026-11-12 13:12:10] ===== TEST SESSION START =====
[2026-11-12 13:12:10] PASSED: tests/test_converters.py::test_csv_to_json_keeps_polish_and_empty_notes
[2026-11-12 13:12:10] PASSED: tests/test_converters.py::test_json_to_csv_roundtrip_headers
[2026-11-12 13:12:10] PASSED: tests/test_converters.py::test_convert_csv_json_via_registry
[2026-11-12 13:12:10] PASSED: tests/test_converters.py::test_broken_json_raises_clear_error
[2026-11-12 13:12:10] PASSED: tests/test_converters.py::test_broken_csv_missing_header_raises
[2026-11-12 13:12:11] PASSED: tests/test_converters.py::test_txt_to_docx_and_back
[2026-11-12 13:12:11] PASSED: tests/test_converters.py::test_docx_to_odt
[2026-11-12 13:12:11] PASSED: tests/test_converters.py::test_odt_to_docx
[2026-11-12 13:12:11] PASSED: tests/test_utils.py::test_shorten_path_keeps_short_value
[2026-11-12 13:12:11] PASSED: tests/test_utils.py::test_shorten_path_adds_ellipsis
[2026-11-12 13:12:11] PASSED: tests/test_utils.py::test_default_output_name_from_source
[2026-11-12 13:12:11] PASSED: tests/test_utils.py::test_default_output_name_without_source
[2026-11-12 13:12:11] PASSED: tests/test_utils.py::test_ensure_extension_adds_missing_suffix
[2026-11-12 13:12:11] PASSED: tests/test_utils.py::test_ensure_extension_fixes_wrong_suffix
[2026-11-12 13:12:11] PASSED: tests/test_validate.py::test_validate_ok_csv_json
[2026-11-12 13:12:11] PASSED: tests/test_validate.py::test_validate_missing_from_format
[2026-11-12 13:12:11] PASSED: tests/test_validate.py::test_validate_missing_input_file
[2026-11-12 13:12:11] PASSED: tests/test_validate.py::test_validate_unsupported_pair
[2026-11-12 13:12:11] PASSED: tests/test_validate.py::test_validate_wrong_extension
[2026-11-12 13:12:11] PASSED: tests/test_validate.py::test_available_targets_matrix
[2026-11-12 13:12:11] ===== TEST SESSION END (exitstatus=0) =====
```

Wniosek z logu: **20/20 PASSED**, brak FAILED.

### Co sprawdzają

**Walidacja** (`test_validate.py`): brak From, brak pliku, zła para formatów,
niepasujące rozszerzenie, poprawne csv→json, macierz `TARGETS`.

**Konwertery** (`test_converters.py`): csv↔json (polskie znaki, puste `notes`),
uszkodzony JSON/CSV, txt→docx→txt, docx→odt, odt→docx.

**Utils** (`test_utils.py`): skracanie ścieżki, domyślna nazwa pliku, dopisywanie
rozszerzenia.

---

## 2. Testy ręczne (GUI)

Testowałem ręcznie w oknie aplikacji.

| Nr | Co robiłem | Czego oczekiwałem | Wynik |
|---:|---|---|---|
| 1 | csv→json, `people.csv` | JSON z `Łukasz` / `Gdańsk`, puste notes | OK |
| 2 | json→csv, `people.json` | CSV z nagłówkami i polskimi znakami | OK |
| 3 | docx→txt | Czytelny TXT | OK |
| 4 | txt→docx | Otwieralny DOCX | OK |
| 5 | docx→odt | Otwieralny ODT | OK |
| 6 | odt→docx | Otwieralny DOCX | OK |
| 7 | Convert bez wyboru pliku | Komunikat w Log, status error | OK |
| 8 | From=csv | W To nie ma niedozwolonych formatów | OK |
| 9 | From=json, ale plik .csv | Błąd rozszerzenia w Log | OK |
| 10 | `broken.json` → csv | `Broken JSON file...`, aplikacja nie pada | OK |
| 11 | Puste `notes` po csv→json | Zostaje puste pole | OK |
| 12 | Brak Pandoc | Komunikat o instalacji | pominięte (Pandoc jest) |

Ręcznie: 11 OK, 0 FAIL, 1 pominięty.

---

## 3. Podsumowanie

Automatyczne: 20/20 (potwierdzone też w `logs/tests.log` — każdy test PASSED).  
Ręczne: 11 OK (1 scenariusz z brakiem Pandoc nie był uruchamiany, bo Pandoc
jest zainstalowany).

Na podstawie tego uważam, że główne ścieżki konwersji i obsługi błędów działają
wystarczająco do oddania projektu. Ograniczenie: dokumenty zależą od Pandoc;
nie gwarantuję zachowania skomplikowanego formatowania.
