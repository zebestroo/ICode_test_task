STATUSES = {

    'CHOOSE_OBJECT': {
        1: 'PROJECT',
        2: 'CONTRACT',
        3: 'QUIT',
    },

    'PROJECT': {
        1: 'CREATE_PROJECT',
        2: 'ADD_CONTRACT',
        3: 'COMPLETE_CONTRACT_USING_PROJECT',
        4: 'CHOOSE_OBJECT',
    },

    'CREATE_PROJECT': {
        1: 'PROJECT',
        2: 'CHOOSE_OBJECT',
    },

    'ADD_CONTRACT': {
        1: 'PROJECT',
        2: 'CHOOSE_OBJECT',
    },

    'COMPLETE_CONTRACT_USING_PROJECT': {
        1: 'PROJECT',
        2: 'CHOOSE_OBJECT',
    },


    'CONTRACT': {
        1: 'CREATE_CONTRACT',
        2: 'CONFIRM_CONTRACT',
        3: 'COMPLETE_CONTRACT',
        4: 'CHOOSE_OBJECT',
    },

    'CREATE_CONTRACT': {
        1: 'CONTRACT',
        2: 'CHOOSE_OBJECT',
    },

    'CONFIRM_CONTRACT': {
        1: 'CONTRACT',
        2: 'CHOOSE_OBJECT',
    },

    'COMPLETE_CONTRACT': {
        1: 'CONTRACT',
        2: 'CHOOSE_OBJECT',
    },
}

DESCRIPTIONS = {
    'CHOOSE_OBJECT': 'Выбрать объект',
    'PROJECT': 'Управление проектами',
    'CREATE_PROJECT': 'Создать проект',
    'ADD_CONTRACT': 'Добавить договор',
    'COMPLETE_CONTRACT_USING_PROJECT': 'Завершить договор',

    'CONTRACT': 'Управление договорами',
    'CREATE_CONTRACT': 'Создать договор',
    'CONFIRM_CONTRACT': 'Подтвердить договор',
    'COMPLETE_CONTRACT': 'Завершить договор',

    'QUIT': 'Выход',
}
