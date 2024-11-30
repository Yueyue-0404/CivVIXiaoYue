from sqlite3 import Connection

function_list = []


def register(DB: Connection):
    for i in function_list:
        DB.create_function(i.__name__, -1, i)


def concat(*arg):
    return ''.join(arg)


function_list.append(concat)
