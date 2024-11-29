from data import save_data, load_data, export_to_csv, import_from_csv


def contacts_func():
    contacts_file = 'contacts.json'
    contacts = [contact_from_dict(contact) for contact in load_data(contacts_file)]

    while True:
        print(
        '''
            --- Управление контактами ---
            1. Добавить новый контакт
            2. Поиск контакта
            3. Редактировать контакт
            4. Удалить контакт
            5. Импорт/экспорт контактов
            6. Вернуться в главное меню
        '''
        )
        choice = input('Выберите действие:')

        if choice == '1':
            add_contact(contacts, contacts_file)
        elif choice == '2':
            search_contact(contacts)
        elif choice == '3':
            edit_contact(contacts, contacts_file)
        elif choice == '4':
            delete_contact(contacts, contacts_file)
        elif choice == '5':
            import_export_contacts(contacts, contacts_file)
        elif choice == '6':
            break
        else:
            print('Некорректный ввод Попробуйте снова')


class Contact:
    def __init__(self, contact_id, name, phone, email=''):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

    def update_from_dict(self, data):
        self.name = data.get('name', self.name)
        self.phone = data.get('phone', self.phone)
        self.email = data.get('email', self.email)


def contact_from_dict(data):
    return Contact(
        contact_id=data['id'],
        name=data['name'],
        phone=data['phone'],
        email=data.get('email', ''),
    )


def get_contact_by_id(id: int, contacts: list) -> dict:
    for c in contacts:
        if int(id) == int(c.id):
            return c
    return None


def add_contact(contacts, file):
    contact_id = len(contacts) + 1
    name = input('Введите имя контакта:')
    phone = input('Введите номер телефона:')
    email = input('Введите адрес электронной почты:')
    contact = Contact(contact_id, name, phone, email)
    contacts.append(contact)
    save_data(file, [contact.to_dict() for contact in contacts])
    print('Контакт успешно добавлен!')


def search_contact(contacts):
    query = input('Введите имя или номер телефона для поиска:')
    results = [
        contact for contact in contacts
        if query.lower() in contact.name.lower() or query in contact.phone
    ]
    if results:
        for contact in results:
            print(f'[{contact.id}] {contact.name} {contact.phone} {contact.email}')
    else:
        print('Контакты не найдены')


def edit_contact(contacts, file):
    contact_id = int(input('Введите ID контакта для редактирования:'))
    contact = get_contact_by_id(id=contact_id, contacts=contacts)
    if not contact:
        print('Контакт с указанным ID не найден')
        return 0

    print(f'Редактирование контакта: {contact.name} {contact.phone} {contact.email}')
    name = input(f'Новое имя ({contact.name}):') or contact.name
    phone = input(f'Новый телефон ({contact.phone}):') or contact.phone
    email = input(f'Новый email ({contact.email}):') or contact.email

    contact.update_from_dict(
        {
            'name': name, 
            'phone': phone, 
            'email': email
         }
         )
    save_data(file, [c.to_dict() for c in contacts])
    print('Контакт успешно обновлён!')


def delete_contact(contacts, file):
    contact_id = int(input('Введите ID контакта для удаления:'))
    contact = get_contact_by_id(id=contact_id, contacts=contacts)
    if not contact:
        print('Контакт с указанным ID не найден')
        return

    contacts.remove(contact)
    save_data(file, [c.to_dict() for c in contacts])
    print('Контакт успешно удалён!')


def import_export_contacts(contacts, file):
    print(
        '''
            1. Экспорт контактов в CSV
            2. Импорт контактов из CSV
        '''
        )
    
    choice = input('Выберите действие:')
    if choice == '1':
        file_name = input('Введите имя файла для экспорта:')
        export_to_csv([contact.to_dict() for contact in contacts], file_name)
    elif choice == '2':
        file_name = input('Введите имя файла для импорта:')
        imported_contacts = import_from_csv(file_name)
        contacts.extend(contact_from_dict(contact) for contact in imported_contacts)
        save_data(file, [c.to_dict() for c in contacts])
        print('Контакты успешно импортированы')
    else:
        print('Некорректный ввод')
