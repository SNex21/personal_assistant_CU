import os, json, csv


def export_to_csv(data: dict, file_name: str):
    keys = data[0].keys() if data else []
    with open(file_name, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f'Данные экспортированы в {file_name}')


def import_from_csv(file_name: str):
    if os.path.exists(file_name):
        with open(file_name, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    print(f'Файл {file_name} не найден')
    return []


def load_data(file):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_data(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
