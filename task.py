from data import save_data, load_data, export_to_csv, import_from_csv


def tasks_func():
    tasks_file = 'tasks.json'
    tasks = [task_from_dict(task) for task in load_data(tasks_file)]

    while True:
        print(
            '''
                --- Управление заданиями ---
                1. Добавить новую задачу
                2. Просмотреть список задач
                3. Отметить задачу как выполненную
                4. Редактировать задачу
                5. Удалить задачу
                6. Импорт/экспорт задач
                7. Вернуться в главное меню
            '''
            )
        choice = input('Выберите действие:')

        if choice == '1':
            create_task(tasks, tasks_file)
        elif choice == '2':
            list_tasks(tasks)
        elif choice == '3':
            mark_task_done(tasks, tasks_file)
        elif choice == '4':
            edit_task(tasks, tasks_file)
        elif choice == '5':
            delete_task(tasks, tasks_file)
        elif choice == '6':
            import_export_tasks(tasks, tasks_file)
        elif choice == '7':
            break
        else:
            print('Некорректный ввод, попробуйте снова')


class Task:
    def __init__(self, 
                 task_id: int, 
                 title: str, 
                 description: str='', 
                 done: bool=False, 
                 priority: str='средний',
                 due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date or ''

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }

    def update_from_dict(self, data: dict) -> None:
        self.title = data.get('title', self.title)
        self.description = data.get('description', self.description)
        self.done = data.get('done', self.done)
        self.priority = data.get('priority', self.priority)
        self.due_date = data.get('due_date', self.due_date)


def task_from_dict(data: dict):
    return Task(
        task_id=data['id'],
        title=data['title'],
        description=data['description'],
        done=data['done'],
        priority=data['priority'],
        due_date=data['due_date'],
    )


def get_task_by_id(id: int, tasks: list) -> dict:
    for t in tasks:
        if int(id) == int(t.id):
            return t
    return None


def create_task(tasks: list, file):
    task_id = len(tasks) + 1
    title = input('Введите название задачи:')
    description = input('Введите описание задачи:')
    priority = input('Укажите приоритет (высокий, средний, низкий):').lower() or 'средний'
    due_date = input('Введите срок выполнения (ДД-ММ-ГГГГ):')
    task = Task(task_id, 
                title, 
                description, 
                priority=priority, 
                due_date=due_date)
    tasks.append(task)
    save_data(file, [task.to_dict() for task in tasks])
    print('Задача успешно добавлена!')


def list_tasks(tasks: list):
    if not tasks:
        print('Список задач пуст')
        return
    for task in tasks:
        status = '✅ Выполнено' if task.done else '❌ Не выполнено'
        print(f'[{task.id}] {task.title} Приоритет: {task.priority} Срок: {task.due_date or "Без срока"} {status}')


def mark_task_done(tasks: list, file):
    task_id = input('Введите ID задачи, которую нужно отметить как выполненную:')
    task = get_task_by_id(id=task_id, tasks=tasks)
    if task:
        task.done = True
        save_data(file, [task.to_dict() for task in tasks])
        print('Задача отмечена как выполненная')
    else:
        print('Задача с таким ID не найдена')


def edit_task(tasks, file):
    task_id = input('Введите ID задачи для редактирования:')
    task = get_task_by_id(id=task_id, tasks=tasks)
    if task:
        print('Введите новые данные (оставьте поле пустым, чтобы не менять его):')
        new_title = input('Новое название: ')
        new_description = input('Новое описание: ')
        new_priority = input('Новый приоритет (Высокий, Средний, Низкий): ').capitalize()
        new_due_date = input('Новый срок выполнения (ДД-ММ-ГГГГ): ')
        task.update_from_dict({
            'title': new_title,
            'description': new_description,
            'priority': new_priority,
            'due_date': new_due_date
        })
        save_data(file, [task.to_dict() for task in tasks])
        print('Задача обновлена!')
    else:
        print('Задача с таким ID не найдена')


def delete_task(tasks, file):
    task_id = input('Введите ID задачи для удаления:')
    task = get_task_by_id(id=task_id, tasks=tasks)
    if task:
        tasks.remove(task)
        save_data(file, [task.to_dict() for task in tasks])
        print('Задача удалена')
    else:
        print('Задача с таким ID не найдена')


def import_export_tasks(tasks, file):
    print(
    '''
        1. Экспорт задач в CSV
        2. Импорт задач из CSV
    '''
    )
    choice = input('Выберите действие:')
    if choice == '1':
        file_name = input('Введите имя файла для экспорта (например, tasks.csv):')
        export_to_csv([task.to_dict() for task in tasks], file_name)
    elif choice == '2':
        file_name = input('Введите имя файла для импорта (например, tasks.csv):')
        imported_tasks = import_from_csv(file_name)
        tasks.extend(task_from_dict(task) for task in imported_tasks)
        save_data(file, [task.to_dict() for task in tasks])
        print('Задачи успешно импортированы')
    else:
        print('Некорректный ввод')
