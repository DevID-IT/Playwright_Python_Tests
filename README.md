# Testy automatyczne dla ParaBank

Repozytorium zawiera testy automatyczne dla strony [ParaBank](https://parabank.parasoft.com/parabank) napisane w **Pythonie** z użyciem **Playwright** i **Pytest**.

---

## 🛠 Technologie

* Python 3.11+
* Playwright
* Pytest
* Allure
* Page Object Model (POM) dla lepszej organizacji testów

---

## 📂 Struktura projektu

```
playwright-tests/
│
├── Tests/                # Pliki z testami
│   ├── test_api.py
│   ├── test_login.py
│   ├── test_register.py
│
├── Pages/                # Page Object Model
│   ├── homePage.py
│
├── reports/              # Raporty testów (opcjonalnie)
├── environment.yml
├── conftest.py           # Globalne fixture i hooki
├── pytest.ini            # Konfiguracja uruchamiania testów
└── README.md
```

---

## ⚡ Instalacja

1. Sklonuj repozytorium:

```bash
git clone <url-repozytorium>
cd playwright-tests
```

2. (Opcjonalnie) Utwórz i aktywuj wirtualne środowisko:

```bash
conda activate parabank-tests
```

3. Zainstaluj zależności:

```bash
conda env create -f environment.yml
```

4. Zainstaluj przeglądarki Playwright:

```bash
python -m playwright install
```

---

## 🚀 Uruchamianie testów

Uruchom wszystkie testy:

```bash
pytest
```

Uruchom testy w trybie szczegółowym:

```bash
pytest -v
```

Uruchom konkretny plik z testami:

```bash
pytest tests/test_login.py
```

Wygeneruj raport HTML:

```bash
pytest --html=reports/report.html
```

---

## ⚙️ Konfiguracja testów

### `conftest.py`

Plik `conftest.py` definiuje globalne fixture i hooki dla testów.
* Po każdym teście sprawdza, czy test zakończył się błędem.
* Jeśli tak, wykonuje screenshot strony i dodaje go do raportu Allure.
* Ułatwia szybkie debugowanie i analizę błędów.

---

### `pytest.ini`

Plik `pytest.ini` ustawia domyślne opcje uruchamiania testów:

```ini
[pytest]
addopts = --browser chromium --browser firefox --browser webkit --tracing=retain-on-failure
```

* Testy uruchamiane są we wszystkich trzech głównych przeglądarkach Playwright.
* Trace (nagranie sesji) jest tworzone tylko dla testów, które zakończyły się błędem.

---

## 📝 Przykładowy test

```python
def test_login_valid_user(page):
        self.home_page.navigate()
        self.home_page.login("xxx", "xxx")
        expect_url = "https://parabank.parasoft.com/parabank/overview.htm"
        expect(self.page).to_have_url(expect_url)
        expect(self.page.locator("#showOverview > h1")).to_have_text("Accounts Overview")
```

---

💡 **Podsumowanie**

Dzięki tej konfiguracji:

* Testy mają dostęp do gotowych obiektów stron (POM).
* Błędy są automatycznie dokumentowane screenshotami i trace’ami.
* Testy uruchamiane są w wielu przeglądarkach bez dodatkowych poleceń.
