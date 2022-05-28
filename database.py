import re
import sqlite3
from typing import NamedTuple

import aiogram.types

REGISTER_QUERY_TEMPLATE = 'INSERT INTO users (id,Lastname,Name,SecondName,DocNumber) VALUES ("{}","{}","{}","{}","{}");'
USER_REGISTERED_QUERY_TEMPLATE = 'SELECT id FROM users WHERE id={};'
GET_USER_DATA_TEMPLATE = 'SELECT Lastname,Name,SecondName,DocNumber FROM users WHERE id={};'

REGISTER_DATA_REGEXP = re.compile(r'^[А-аЯ-я]{3,15}\s[А-аЯ-я]{3,15}\s[А-аЯ-я]{3,15}\s\d{6}$')

connection = sqlite3.connect('NCMSTracker.sqlite3')


class UserData(NamedTuple):
    Lastname: str
    Name: str
    SecondName: str
    DocNumber: int


def is_user_registered(message: aiogram.types.Message) -> bool:
    cur = connection.cursor()
    cur.execute(USER_REGISTERED_QUERY_TEMPLATE.format(
        message.from_user.id
    ))
    return cur.fetchone() is not None


def register_user(message: aiogram.types.Message) -> str:
    connection.cursor().execute(REGISTER_QUERY_TEMPLATE.format(
        message.from_user.id, *message.text.split()
    ))
    connection.commit()
    return 'готово'


def get_user_data(user_id: int) -> UserData:
    cur = connection.cursor()
    cur.execute(GET_USER_DATA_TEMPLATE.format(user_id))
    data = cur.fetchone()
    return UserData(*data)
