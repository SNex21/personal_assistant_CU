from note import notes_func
from task import tasks_func
from finance import finance_func

def main_menu():
    while True:
        print(
        '''
            Добро пожаловать в Персональный помощник!
            Выберите действие:
            1. Управление заметками
            2. Управление задачами
            3. Управление контактами
            4. Управление финансовыми записями
            5. Калькулятор
            6. Выход
        '''
        )
        choice = input('Введите номер действия:')
        if choice == '1':
            notes_func()
        elif choice == '2':
            tasks_func()
        elif choice == '3':
            pass
        elif choice == '4':
            finance_func()
        elif choice == '5':
            pass
        elif choice == '6':
            print('ПОКА!')
            break
        else:
            print('Некорректный ввод. Попробуйте снова.')


if __name__=='__main__':
    main_menu()
