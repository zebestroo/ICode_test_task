from config import *
import logging
from models import Contract, Project, CustomFormatter
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fmt = '%(levelname)s ---> %(message)s'

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(CustomFormatter(fmt))

logger.addHandler(handler)


def configure_database(cursor):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Contracts';")
    if not cursor.fetchone():
        logger.warning('Table *Contracts* does not exist.')
        cursor.execute("""CREATE TABLE Contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            create_date DATETIME,
            status VARCHAR(255) DEFAULT 'Draft',
            project VARCHAR(255),
            sign_date DATETIME
            )""")
        logger.info('Table *Contracts* created successfully.')

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Projects';")
    if not cursor.fetchone():
        logger.warning('Table *Projects* does not exist.')
        cursor.execute("""CREATE TABLE Projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            create_date DATETIME
            )""")
        logger.info('Table *Projects* created successfully.')

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Links';")
    if not cursor.fetchone():
        logger.warning('Table *Links* does not exist.')
        cursor.execute("""CREATE TABLE Links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER,
            project_id INTEGER,
            FOREIGN KEY (contract_id) REFERENCES Contracts (id)
            )""")
        logger.info('Table *Links* created successfully.')


def get_menu(status):
    menu = ''
    for i, option in STATUSES[status].items():
        menu += f'{i}: {DESCRIPTIONS[option]}\n'
    return menu


def choose_object(cursor, status):
    print(get_menu(status))
    print('0: Список проектов и договоров')
    pointer = int(input('Перейти в: '))

    while pointer == 0:
        show_all_objects(cursor)
        print('\n')
        print(DESCRIPTIONS[status])
        print(get_menu(status))
        print('0: Список проектов и договоров')
        pointer = int(input('Перейти в: '))
    print('\n')

    return pointer


def dump_object(obj, cursor):
    obj.dump(cursor)


def get_all_projects_names(cursor):
    cursor.execute(f"""SELECT name FROM Projects""")
    return [tp[0] for tp in cursor.fetchall()]


def get_all_contracts_names(cursor):
    cursor.execute(f"""SELECT name FROM Contracts""")
    return [tp[0] for tp in cursor.fetchall()]


def get_all_active_contracts(cursor):
    cursor.execute(f"""SELECT * FROM Contracts WHERE status='Active'""")
    return cursor.fetchall()


def is_active_contract_exists(cursor):
    if get_all_active_contracts(cursor):
        return True
    else:
        return False


def create_project(cursor, connection):
    if is_active_contract_exists(cursor):
        name = input('Имя проекта: ')

        if name in get_all_projects_names(cursor):
            logger.error(
                'Проект с таким именем существует. Необходимо указать другое имя.')
            return

        project = Project()

        project.set_name(name)
        dump_object(project, cursor)
        connection.commit()
        logger.info('Проект создан.')
    else:
        logger.error(
            'Не существует активных договоров. Необходимо создать активный договор.')


def create_contract(cursor, connection):
    name = input('Имя договора: ')

    if name in get_all_contracts_names(cursor):
        logger.error(
            'Договор с таким именем существует. Необходимо указать другое имя.')
        return

    contract = Contract()

    contract.set_name(name)
    dump_object(contract, cursor)
    connection.commit()
    logger.info('Договор создан.')


def confirm_contract(cursor):
    contract_id = int(input('Подтвердить договор(ID): '))
    cursor.execute(f"""SELECT id FROM Contracts WHERE status='Draft'""")
    ids = [tp[0] for tp in cursor.fetchall()]

    if contract_id not in ids:
        logger.error('Нет такого договора, либо он уже подтверждён. Задайте правильный ID.')
        return

    cursor.execute(
        f"""UPDATE Contracts SET status='Active', sign_date='{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE id={contract_id}""")
    logger.info('Договор упешно подтверждён')


def show_all_projects(cursor):
    cursor.execute(f"""SELECT * FROM Projects""")
    print('Проекты:')
    for project in cursor.fetchall():
        print(
            f'ID: {project[0]:>3}  |  Имя проекта: {project[1]:>25}  |   Дата создания: {project[2]:>20}  |')


def show_all_contracts(cursor, project_id=None):
    if project_id:
        cursor.execute(
            f"""SELECT name FROM Projects WHERE id='{project_id}'""")
        project_name = cursor.fetchone()[0]
        cursor.execute(
            f"""SELECT * FROM Contracts WHERE project='{project_name}'""")

    else:
        cursor.execute(f"""SELECT * FROM Contracts""")

    print('\nДоговора:')
    contracts = cursor.fetchall()
    for contract in contracts:
        print(f'ID: {contract[0]:>3}  |  Имя договора: {contract[1]:>24}  |   Дата создания: {contract[2]:>20}  |   Статус: {contract[3]:>10}   |   Проект: {contract[4]:>18} |')
    return contracts


def show_all_objects(cursor):
    print('----------' * 15)
    show_all_projects(cursor)
    show_all_contracts(cursor)
    print('----------' * 15)


def is_project_available_to_add(cursor, project_id, contract_id):
    cursor.execute(
        f"""SELECT id FROM Contracts WHERE project='Untitled' AND status='Active'""")
    available_contracts = [tp[0] for tp in cursor.fetchall()]

    cursor.execute(f"""SELECT name FROM Projects WHERE id='{project_id}'""")
    project_name = cursor.fetchone()[0]

    cursor.execute(
        f"""SELECT id FROM Contracts WHERE project='{project_name}' AND status='Active'""")
    active_contracts_of_project = [tp[0] for tp in cursor.fetchall()]

    if contract_id in available_contracts and not active_contracts_of_project:

        cursor.execute(
            f"""SELECT * FROM Links WHERE project_id='{project_id}'""")
        contracts_ids_by_project_id = [tp[1] for tp in cursor.fetchall()]

        if not set(contracts_ids_by_project_id).intersection(
                set(available_contracts)):
            return True

        else:
            logger.error('Договор уже используется в данном проекте.')
            return False
    else:
        logger.error(
            'Договор уже используется в проекте | В проекте существует другой активный договор | Договор не является активным')
        return False


def setup_project_for_contract(cursor, contract_id, project_id):
    cursor.execute(
        f"""INSERT INTO Links (contract_id, project_id) VALUES ({contract_id}, {project_id})""")

    cursor.execute(f"""SELECT name FROM Projects WHERE id='{project_id}'""")
    project_name = cursor.fetchone()[0]
    cursor.execute(
        f"""UPDATE Contracts SET project='{project_name}' WHERE id={contract_id}""")


def add_contract(cursor, connection):
    contract_id = int(input('Добавить договор(ID): '))
    cursor.execute(f"""SELECT id FROM Contracts""")
    contracts_ids = [tp[0] for tp in cursor.fetchall()]

    if contract_id not in contracts_ids:
        logger.error('Нет такого договора. Задайте правильный ID.')
        return

    project_id = int(input('Добавить в проект(ID): '))
    cursor.execute(f"""SELECT id FROM Projects""")
    projects_ids = [tp[0] for tp in cursor.fetchall()]

    if project_id not in projects_ids:
        logger.error('Нет такого проекта. Задайте правильный ID.')
        return

    if is_project_available_to_add(cursor, project_id, contract_id):
        setup_project_for_contract(cursor, contract_id, project_id)
        connection.commit()
        logger.info(
            f'Договор(ID: {contract_id}) добавлен в проект(ID: {project_id}).')

    else:
        logger.warning(
            f'Договор(ID: {contract_id}) не был добавлен в проект(ID: {project_id}).')


def is_contract_not_completed(cursor, contract_id):
    cursor.execute(
        f"""SELECT status FROM Contracts WHERE id='{contract_id}'""")
    contract_status = cursor.fetchone()[0]

    if contract_status != 'Completed':
        return True
    else:
        return False


def complete_contract(cursor, contract_id):
    cursor.execute(
        f"""UPDATE Contracts SET status='Completed' WHERE id={contract_id}""")


def complete_contract_using_project(cursor, connection):
    show_all_projects(cursor)

    project_id = int(input('Проект(ID): '))
    cursor.execute(f"""SELECT id FROM Projects""")
    projects_ids = [tp[0] for tp in cursor.fetchall()]

    if project_id not in projects_ids:
        logger.error('Нет такого проекта. Задайте правильный ID.')
        return

    contracts_ids = [
        tp[0] for tp in show_all_contracts(
            cursor, project_id=project_id)]
    contract_id = int(input('Завершить договор(ID): '))

    if contract_id not in contracts_ids:
        logger.error('Нет такого договора. Задайте правильный ID.')
        return

    if is_contract_not_completed(cursor, contract_id):
        complete_contract(cursor, contract_id)
        connection.commit()
        logger.info('Статус договора успешно изменился. Договор завершён.')

    else:
        logger.warning('Договор уже завершён.')


def complete_contract_using_id(cursor, connection):
    contract_id = int(input('Подтвердить договор(ID): '))
    cursor.execute(f"""SELECT id FROM Contracts""")
    contracts_ids = [tp[0] for tp in cursor.fetchall()]

    if contract_id not in contracts_ids:
        logger.error('Нет такого договора. Задайте правильный ID.')
        return

    if is_contract_not_completed(cursor, contract_id):
        complete_contract(cursor, contract_id)
        connection.commit()
        logger.info('Статус договора успешно изменился. Договор завершён.')

    else:
        logger.warning('Договор уже завершён.')
