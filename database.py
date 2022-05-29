import os.path
import re
import sqlite3
from typing import NamedTuple

import aiogram.types

REGISTER_DATA_REGEXP = re.compile(r'^[А-аЯ-я]{3,15}\s[А-аЯ-я]{3,15}\s[А-аЯ-я]{3,15}\s\d{6}$')
DB_FILENAME = 'NCMSTracker.sqlite3'


class UserData(NamedTuple):
    Lastname: str
    Name: str
    SecondName: str
    DocNumber: int


if not os.path.exists(DB_FILENAME):
    connection = sqlite3.connect(DB_FILENAME)
    CREATE_DB_SQL = open('sql/create_db.sql', 'r').read()
    connection.execute(CREATE_DB_SQL)
    connection.commit()
else:
    connection = sqlite3.connect(DB_FILENAME)


def is_user_registered(message: aiogram.types.Message) -> bool:
    user_registered_query_template = open('sql/is_user_registered_template.sql').read()
    cur = connection.cursor()

    cur.execute(user_registered_query_template.format(
        message.from_user.id
    ))

    return cur.fetchone() is not None


def register_user(message: aiogram.types.Message) -> str:
    register_query_template = open('sql/register_user_template.sql').read()

    connection.cursor().execute(register_query_template.format(
        message.from_user.id, *message.text.split()
    ))

    connection.commit()
    return 'готово'


def get_user_data(user_id: int) -> UserData:
    get_user_data_template = open('sql/get_user_data_template.sql').read()
    cur = connection.cursor()
    cur.execute(get_user_data_template.format(user_id))
    data = cur.fetchone()
    return UserData(*data)
