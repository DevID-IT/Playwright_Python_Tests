import pandas as pd
import json
import os
import re
import time
import uuid
import hashlib

# === KONFIGURACJA ===
EXCEL_PATH = "Documentation/parabank_test_cases_filled.xlsx"
OUTPUT_DIR = "allure-results"

# Mapowanie statusów z Excela na statusy Allure
STATUS_MAP = {
    "Zrobiony": "passed",
    "Niepowodzenie": "failed",
    "Zablokowany": "skipped",
    "Do zrobienia": "skipped",
}

# Jaki typ wykonania uznajemy za "manualny"
MANUAL_TYPE_NORMALIZED = "manualny"


def normalize_text(value) -> str:
    """Bezpieczna normalizacja tekstu (do porównań)."""
    if not isinstance(value, str):
        value = str(value)
    return value.strip().lower()


def is_manual(row) -> bool:
    """Zwraca True tylko dla wierszy, gdzie Typ wykonania == 'Manualny' (case-insensitive)."""
    exec_type_raw = row.get("Typ wykonania", "")
    return normalize_text(exec_type_raw) == MANUAL_TYPE_NORMALIZED


def split_steps(raw_steps: str):
    """
    Rozbij 'Kroki testowe' na listę kroków.
    Usuwa numerację '1. ...', '2. ...' itp.
    """
    if not isinstance(raw_steps, str):
        return []

    steps = []
    for line in raw_steps.splitlines():
        # usuń "1. ", "2. " itd.
        step_text = re.sub(r'^\s*\d+\.\s*', '', line).strip()
        if step_text:
            steps.append(step_text)
    return steps


def parse_test_data_to_parameters(test_data: str):
    """
    Parsuje 'Dane testowe' w formacie:
        Login: Dawid6286
        Hasło: Dawid6286

    Na listę parametrów Allure:
        [
            {"name": "Login", "value": "Dawid6286"},
            {"name": "Hasło", "value": "Dawid6286"}
        ]
    """
    if not isinstance(test_data, str):
        return []

    params = []
    for line in test_data.splitlines():
        line = line.strip()
        if not line:
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            params.append({
                "name": key.strip(),
                "value": value.strip()
            })
    return params


def make_history_id(case_id: str, case_name: str) -> str:
    """
    Stabilny hash na bazie ID + nazwy przypadku,
    żeby Allure mógł grupować historię testu.
    """
    base = f"{case_id}|{case_name}"
    return hashlib.md5(base.encode("utf-8")).hexdigest()


def row_to_allure_result_advanced(row):
    """
    Konwersja pojedynczego wiersza Excela (przypadku testowego)
    do struktury JSON Allure (jeden result).
    Zakładamy, że ten wiersz jest już zweryfikowany jako "Manualny".
    """
    area = str(row.get("Obszar", "")).strip()
    case_id = str(row.get("ID Przypadku", "")).strip()
    case_name = str(row.get("Nazwa przypadku", "")).strip()
    test_data = str(row.get("Dane testowe", "")).strip()
    steps_raw = row.get("Kroki testowe", "")
    expected = str(row.get("Oczekiwany rezultat", "")).strip()
    exec_type = str(row.get("Typ wykonania", "")).strip()
    status_text = str(row.get("Status", "")).strip()

    status = STATUS_MAP.get(status_text, "unknown")

    # Parametry z danych testowych
    params = parse_test_data_to_parameters(test_data)

    # Kroki
    step_texts = split_steps(steps_raw)
    steps = []

    for i, s in enumerate(step_texts):
        step_obj = {
            "name": s,
            "status": status
        }
        # Do pierwszego kroku podpinamy parametry (opcjonalnie)
        if i == 0 and params:
            step_obj["parameters"] = params
        steps.append(step_obj)

    # Krok z weryfikacją oczekiwanego rezultatu (opcjonalnie)
    if expected:
        steps.append({
            "name": "Weryfikacja oczekiwanego rezultatu: " + expected.replace("\n", " "),
            "status": status
        })

    now_ms = int(time.time() * 1000)
    history_id = make_history_id(case_id, case_name)

    result = {
        "name": f"{case_id} - {case_name}",
        "status": status,
        "description": (
            f"Obszar: {area}\n\n"
            f"Typ wykonania: {exec_type}\n\n"
            f"Oczekiwany rezultat:\n{expected}"
        ),
        "steps": steps,
        "parameters": params,
        "start": now_ms,
        "stop": now_ms,
        "uuid": str(uuid.uuid4()),
        "historyId": history_id,
        "testCaseId": history_id,
        "fullName": f"Testy manualne.{area}.{case_id}.{case_name}",
        "labels": [
            {"name": "parentSuite", "value": "Testy manualne"},
            {"name": "suite", "value": area},
            {"name": "framework", "value": "manual"},
            {"name": "language", "value": "none"},
        ],
        "titlePath": [
            "Testy manualne",
            area,
            case_id,
            case_name
        ]
    }

    return result


def main():
    if not os.path.exists(EXCEL_PATH):
        print(f"[BŁĄD] Nie znaleziono pliku Excela: {EXCEL_PATH}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_excel(EXCEL_PATH)

    total_rows = len(df)
    generated = 0
    skipped_not_manual = 0

    # Do walidacji / raportowania
    exec_type_counter = {}

    for idx, row in df.iterrows():
        exec_type_raw = row.get("Typ wykonania", "")
        exec_type_norm = normalize_text(exec_type_raw)
        exec_type_counter[exec_type_raw] = exec_type_counter.get(exec_type_raw, 0) + 1

        # filtr -> tylko manualne przypadki
        if exec_type_norm != MANUAL_TYPE_NORMALIZED:
            skipped_not_manual += 1
            continue

        # Tylko tutaj generujemy JSON (Manualny)
        result = row_to_allure_result_advanced(row)
        file_name = f"{result['uuid']}-result.json"
        out_path = os.path.join(OUTPUT_DIR, file_name)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        generated += 1

    # === PODSUMOWANIE ===
    print("=== PODSUMOWANIE GENEROWANIA ALLURE JSON ===")
    print(f"Łączna liczba wierszy w Excelu: {total_rows}")
    print("Typy wykonania znalezione w Excelu:")
    for t, count in exec_type_counter.items():
        print(f"  '{t}': {count} wierszy")

    print(f"\nPliki wynikowe zapisano w katalogu: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
