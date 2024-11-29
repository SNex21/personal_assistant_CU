from datetime import datetime

from data import save_data, load_data, export_to_csv, import_from_csv


def finance_func():
    finance_file = 'finance.json'
    records = [finance_from_dict(record) for record in load_data(finance_file)]

    while True:
        print(
            '''
                --- Управление финансовыми записями ---
                1. Добавить новую запись
                2. Просмотреть все записи
                3. Фильтровать записи
                4. Генерация отчёта
                5. Подсчёт баланса
                6. Импорт/экспорт записей
                7. Вернуться в главное меню
        ''')
        choice = input('Выберите действие: ')

        if choice == '1':
            add_finance_record(records, finance_file)
        elif choice == '2':
            list_finance_records(records)
        elif choice == '3':
            filter_finance_records(records)
        elif choice == '4':
            generate_financial_report(records)
        elif choice == '5':
            calculate_balance(records)
        elif choice == '6':
            import_export_finances(records, finance_file)
        elif choice == '7':
            break
        else:
            print('Некорректный ввод. Попробуйте снова.')


class FinanceRecord:
    def __init__(self, 
                 finance_id: int, 
                 amount: float, 
                 category: str, 
                 description: str, 
                 date=None):
        self.id = finance_id
        self.amount = amount
        self.category = category
        self.date = date or datetime.now().strftime('%d-%m-%Y')
        self.description = description

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description,
        }

    def update_from_dict(self, data: dict) -> None:

        self.title = data.get('title', self.title)
        self.amount = data.get('amount', self.amount)
        self.category = data.get('category', self.category)
        self.description = data.get('description', self.description)
        self.date = datetime.now().strftime('%d-%m-%Y')


def finance_from_dict(data: dict):
    return FinanceRecord(
        finance_id=data['id'],
        amount=data['amount'],
        category=data['category'],
        date=data['date'],
        description=data['description']
)
    

def get_finance_by_id(id: int, finances: list) -> dict:
    for f in finances:
        if int(id) == int(f.id):
            return f
    return None


def add_finance_record(records, file):
    record_id = len(records) + 1
    amount = float(input('Введите сумму операции:'))
    category = input('Введите категорию операции:')
    date = input('Введите дату операции (ДД-ММ-ГГГГ):')
    description = input('Введите описание операции:')
    record = FinanceRecord(record_id, amount, category, description, date)
    records.append(record)
    save_data(file, [record.to_dict() for record in records])
    print('Финансовая запись добавлена!')


def list_finance_records(records):
    if not records:
        print('Список финансовых записей пуст')
        return 0
    for record in records:
        print(f'[{record.id}] {record.category} {record.amount} {record.date} {record.description}')


def filter_finance_records(records):
    print('''
        Фильтровать записи по:
        1. Дате
        2. Категории
    ''')
    choice = input('Выберите фильтр:')
    if choice == '1':
        date = input('Введите дату (ДД-ММ-ГГГГ):')

        filtered = [record for record in records if record.date == date]

        print(records[0].date)
    elif choice == '2':
        category = input('Введите категорию:')
        filtered = [record for record in records if record.category.lower() == category.lower()]
    else:
        print('Некорректный ввод')
        return 0

    if filtered:
        for record in filtered:
            print(f'[{record.id}] {record.category} {record.amount} {record.date} {record.description}')
    else:
        print('Записи по данному фильтру не найдены')


def generate_financial_report(finance_records):
    start_date = input('Введите начальную дату (ДД-ММ-ГГГГ):')
    end_date = input('Введите конечную дату (ДД-ММ-ГГГГ):')

    try:
        start_date_obj = datetime.strptime(start_date, '%d-%m-%Y')
        end_date_obj = datetime.strptime(end_date, '%d-%m-%Y')

        filtered_records = [
            record for record in finance_records
            if start_date_obj <= datetime.strptime(record.date, '%d-%m-%Y') <= end_date_obj
        ]

        income = sum(record.amount for record in filtered_records if record.amount > 0)
        expenses = sum(record.amount for record in filtered_records if record.amount < 0)
        balance = income + expenses

        print(f'\nФинансовый отчёт за период с {start_date} по {end_date}:')
        print(f'- Общий доход: {income:.2f} руб.')
        print(f'- Общие расходы: {abs(expenses):.2f} руб.')
        print(f'- Баланс: {balance:.2f} руб.')

        filename = f'report_{start_date}_{end_date}.csv'
        export_to_csv(filtered_records, filename)

        print(f'Подробная информация сохранена в файле {filename}\n')
    except ValueError:
        print('Некорректный формат даты. Используйте ДД-ММ-ГГГГ')


def calculate_balance(records):
    balance = sum([record.amount for record in records])
    print(f'Общий баланс: {balance}')


def import_export_finances(records, file):
    print(
        '''
            1. Экспорт финансовых записей в CSV
            2. Импорт финансовых записей из CSV
        '''
    )
    choice = input('Выберите действие:')
    if choice == '1':
        file_name = input('Введите имя файла для экспорта:')
        export_to_csv([record.to_dict() for record in records], file_name)

    elif choice == '2':
        file_name = input('Введите имя файла для импорта:')
        imported_records = import_from_csv(file_name)
        records.extend(finance_from_dict(record) for record in imported_records)
        save_data(file, [record.to_dict() for record in records])
        print('Финансовые записи успешно импортированы')
    else:
        print('Некорректный ввод')
