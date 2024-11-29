from datetime import datetime

from data import save_data, load_data, export_to_csv, import_from_csv


def notes_func():
    notes_file = 'notes.json'
    notes = [note_from_dict(note) for note in load_data(notes_file)] 

    while True:
        print(
            '''
                --- Управление заметками ---
                1. Создать новую заметку
                2. Просмотреть все заметки
                3. Просмотреть заметку
                4. Редактировать заметку
                5. Удалить заметку
                6. Импорт/экспорт заметок
                7. Вернуться в главное меню
            '''
            )
        choice = input('Выберите действие:')

        if choice == '1':
            create_note(notes, notes_file)
        elif choice == '2':
            list_notes(notes)
        elif choice == '3':
            view_note_describe(notes)
        elif choice == '4':
            edit_note(notes, notes_file)
        elif choice == '5':
            delete_note(notes, notes_file)
        elif choice == '6':
            import_export_notes(notes, notes_file)
        elif choice == '7':
            break
        else:
            print('Некорректный ввод Попробуйте снова')


# Класс заметки объявляем
class Note:
    def __init__(self, note_id: int, title: str, content: str, timestamp=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

    def update_from_dict(self, data: dict) -> None:

        self.title = data.get('title', self.title)
        self.content = data.get('content', self.content)
        self.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def note_from_dict(data: dict):
    return Note(
        note_id=data['id'],
        title=data['title'],
        content=data['content'],
        timestamp=data['timestamp']
)
    

def get_note_by_id(id: int, notes: list) -> dict:
    for n in notes:
        if int(id) == int(n.id):
            return n
    return None


# Далее написаны методы для заметок
def create_note(notes: list, file):
    note_id = len(notes) + 1
    title = input('Введите заголовок заметки:')
    content = input('Введите содержание заметки:')
    note = Note(note_id, title, content)
    notes.append(note)
    save_data(file, [note.to_dict() for note in notes])
    print('Заметка создана!')


def list_notes(notes):
    if not notes:
        print('Заметок пока нет.')
        return None
    
    for note in notes:
        print(f'[{note.id}] {note.title} ({note.timestamp})')


def view_note_describe(notes):
    note_id = input('Введите ID заметки для просмотра:')
    note = get_note_by_id(id=note_id, notes=notes)
    if note:
        print(
            f'''
                ID: {note.id}
                Заголовок: {note.title}
                Содержание: {note.content}
                Дата изменения: {note.timestamp}
            '''
            )
    else:
        print('Заметка с таким ID не найдена')


def edit_note(notes, file):
    note_id = input('Введите ID заметки для редактирования:')
    note = get_note_by_id(id=note_id, notes=notes)
    if note:
        print('Введите новые данные (оставьте поле пустым, чтобы не менять его):')
        new_title = input('Новый заголовок:')
        new_content = input('Новое содержание:')
        note.update_from_dict({'title': new_title, 'content': new_content})
        save_data(file, [note.to_dict() for note in notes])
        print('Заметка обновлена!')
    else:
        print('Заметка с таким ID не найдена.')


def import_export_notes(notes, file):
    print('''
1. Экспорт заметок в CSV
2. Импорт заметок из CSV
    ''')
    choice = input('Выберите действие: ')
    if choice == '1':
        file_name = input('Введите имя файла для экспорта (например, notes.csv): ')
        export_to_csv([note.to_dict() for note in notes], file_name)
    elif choice == '2':
        file_name = input('Введите имя файла для импорта (например, notes.csv): ')
        imported_notes = import_from_csv(file_name)
        notes.extend(note_from_dict(note) for note in imported_notes)
        save_data(file, [note.to_dict() for note in notes])
        print('Заметки успешно импортированы.')
    else:
        print('Некорректный ввод.')


def delete_note(notes, file):
    note_id = input('Введите ID заметки для удаления: ')
    note = next((note for note in notes if str(note.id) == note_id), None)
    if note:
        notes.remove(note)
        save_data(file, [note.to_dict() for note in notes])
        print('Заметка удалена.')
    else:
        print('Заметка с таким ID не найдена.')
