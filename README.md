# Universal File Converter

Aplikacja desktopowa (Python + Tkinter) do konwersji plików między wybranymi
formatami. Po wyborze formatu źródłowego pokazywane są tylko możliwe formaty
docelowe. Konwersja działa w tle, status i komunikaty trafiają do okna Log.

Projekt na zajęcia Programowanie V.

---

## Wymagania

- Python 3.10+ (testowane na 3.13)
- Windows / Linux / macOS
- Pandoc (do DOCX / TXT / ODT)

Zależności Pythona są w `requirements.txt`.

---

## Instalacja

```bat
cd Universal-File-Converter
python -m pip install -r requirements.txt
```

`pypandoc_binary` w requirements zwykle wystarcza (Pandoc jest w paczce).
Jeśli nadal brak Pandoc, zainstaluj go osobno i dodaj do PATH albo użyj:

```bat
python -m pip install pypandoc_binary
```

---

## Uruchomienie

```bat
python main.py
```

1. Wybierz **From** (format wejściowy).
2. Wybierz **To** (tylko dozwolone opcje).
3. **Open File** — plik wejściowy.
4. **Save Path** — gdzie zapisać wynik (domyślna nazwa i rozszerzenie).
5. **Convert**.

Status: `waiting` / `converting` / `ready` / `error`.  
Szczegóły błędów i sukcesu są w polu **Log** oraz w pliku `logs/app.log`.

Logi testów automatycznych zapisują się do `logs/tests.log`
(każdy test osobno: PASSED / FAILED).

---

## Macierz konwersji

| From | To | Grupa | Narzędzie |
|---|---|---|---|
| csv | json | A — dane strukturalne | csv + json (stdlib) |
| json | csv | A | csv + json |
| docx | txt | B — tekst/dokument | Pandoc (pypandoc) |
| txt | docx | B | Pandoc |
| docx | odt | C — formaty biurowe | Pandoc |
| odt | docx | C | Pandoc |

Razem **6 kierunków**.

### Semantyka CSV / JSON

- Kodowanie: **UTF-8**
- CSV: pierwszy wiersz = nagłówki kolumn (`csv.DictReader` / `DictWriter`)
- JSON: lista obiektów, np. `[{"id": "1", "name": "..."}, ...]`
- Kolejność i nazwy kolumn są zachowywane przy csv↔json
- Puste pola (np. `notes`) są dozwolone
- Polskie znaki są zachowywane (`ensure_ascii=False` przy zapisie JSON)

Przykładowe dane: folder `samples/` (`people.csv`, `people.json`, …).  
Plik uszkodzony do testów: `samples/broken.json`.

---

## Struktura projektu

```
main.py          — start aplikacji
ui.py            — budowa okna
actions.py       — obsługa przycisków, wątek konwersji
converters.py    — walidacja + konwertery + rejestr
utils.py         — ścieżki / nazwy plików
app_logger.py    — zapis logów do plików
logs/            — app.log (GUI) i tests.log (pytest)
samples/         — dane testowe
tests/           — pytest + raport testów
requirements.txt
pytest.ini
```

Logika konwersji jest oddzielona od GUI. Nowa para formatów = funkcja + wpis
w `TARGETS` / `CONVERTERS` (bez przebudowy całego interfejsu).

---

## Testy

Automatyczne:

```bat
python -m pytest -q
```

Raport (auto + ręczne): `tests/TEST_REPORT.md`

---

## Znane ograniczenia

- Nie gwarantujemy pełnego formatowania dokumentów (style, wykresy, makra).
- Konwersje DOCX/TXT/ODT wymagają Pandoc.
- TXT→DOCX idzie przez Pandoc jako markdown (prosty tekst / akapity).
- Aplikacja nie konwertuje „wszystkiego na wszystko” — tylko pary z tabeli.
- Nadpisanie istniejącego pliku wyjściowego jest potwierdzane przez systemowe
  okno „Save As” (pytanie o zastąpienie pliku).

---

## Źródła i narzędzia

- Python `csv`, `json`, `pathlib`, `threading`, `tkinter`
- [pypandoc](https://github.com/JessicaTegner/pypandoc) + Pandoc
- pytest
- Dokumentacja projektu / fragment wzorcowy rejestru konwerterów z instrukcji

## Użycie AI

W projekcie został użyty AI. Kod został przejrzany i jest zrozumiany przez autora.

---

## Autor

Vladyslav Hordiienko 105591
