# Raport testów ręcznych — Universal File Converter

Data: 2026-11-07  
Jak uruchomić aplikację: `python tk_test.py`

## Macierz testów

| # | Przypadek | Kroki | Oczekiwany rezultat | Wynik |
|---|---|---|---|---|
| 1 | CSV → JSON (poprawny plik + polskie znaki) | From=`csv`, To=`json`, otwórz `samples/people.csv`, zapisz np. `out.json`, Convert | Status `ready`/`готово`, w JSON widać `Łukasz`, `Gdańsk`, puste `notes` | OK / FAIL |
| 2 | JSON → CSV | From=`json`, To=`csv`, `samples/people.json` | CSV z nagłówkami i polskimi znakami | OK / FAIL |
| 3 | DOCX → TXT | From=`docx`, To=`txt`, `samples/people.docx` | Plik TXT otwieralny, treść zachowana | OK / FAIL |
| 4 | TXT → DOCX | From=`txt`, To=`docx`, `samples/people.txt` | Plik DOCX otwieralny | OK / FAIL |
| 5 | DOCX → ODT | From=`docx`, To=`odt`, `samples/people.docx` | Plik ODT otwieralny | OK / FAIL |
| 6 | ODT → DOCX | From=`odt`, To=`docx`, `samples/people.odt` | Plik DOCX otwieralny | OK / FAIL |
| 7 | Brak pliku wejściowego | Convert bez Open File | Log: `Error: choose an input file`, status error | OK / FAIL |
| 8 | Nieobsługiwana para | Wybierz From=`csv` — w To nie ma `odt` | Nie da się wybrać niedozwolonej pary | OK / FAIL |
| 9 | Zły extension | From=`json`, ale otwórz `.csv` | Log o niezgodnym rozszerzeniu | OK / FAIL |
| 10 | Uszkodzony JSON | From=`json`, To=`csv`, `samples/broken.json` | Log: `Broken JSON file...`, aplikacja nie pada | OK / FAIL |
| 11 | Puste wartości | Po CSV→JSON sprawdź rekord Łukasza | `"notes": ""` zachowane | OK / FAIL |
| 12 | Brak Pandoc (opcjonalnie) | Odinstaluj/ukryj pandoc i spróbuj docx→txt | Log z instrukcją instalacji pandoc/`pypandoc_binary` | OK / FAIL |

## Uwagi

- Testy automatyczne: `pytest -q`
- Dane testowe: folder `samples/`
- Znane ograniczenia: konwersje dokumentów zależą od Pandoc; złożone formatowanie nie jest gwarantowane
