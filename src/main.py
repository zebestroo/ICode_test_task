import sqlite3 as sql
from controls import *


status = 'CHOOSE_OBJECT'

with sql.connect('database.sqlite3') as connection:
    cursor = connection.cursor()
    configure_database(cursor)

    while True:
        try:
            print(DESCRIPTIONS[status])
            match status:

                case 'CHOOSE_OBJECT':
                    pointer = choose_object(cursor, status)
                    status = STATUSES[status][pointer]

                case 'PROJECT':
                    pointer = choose_object(cursor, status)
                    status = STATUSES[status][pointer]

                case 'CREATE_PROJECT':
                    create_project(cursor, connection)
                    status = 'PROJECT'

                case 'ADD_CONTRACT':
                    show_all_objects(cursor)
                    add_contract(cursor, connection)
                    status = 'PROJECT'

                case 'COMPLETE_CONTRACT_USING_PROJECT':
                    complete_contract_using_project(cursor, connection)
                    status = 'PROJECT'

                case 'CONTRACT':
                    pointer = choose_object(cursor, status)
                    status = STATUSES[status][pointer]

                case 'CREATE_CONTRACT':
                    create_contract(cursor, connection)
                    status = 'CONTRACT'

                case 'CONFIRM_CONTRACT':
                    show_all_contracts(cursor)
                    confirm_contract(cursor)
                    status = 'CONTRACT'

                case 'COMPLETE_CONTRACT':
                    show_all_contracts(cursor)
                    complete_contract_using_id(cursor, connection)
                    status = 'CONTRACT'

                case 'QUIT':
                    break

        except KeyError as e:
            logger.warning('Invalid option. Try again:)')
        except ValueError as e:
            logger.warning('Invalid option. Please, be careful:)')
