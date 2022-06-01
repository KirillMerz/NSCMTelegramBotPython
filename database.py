import os.path
import sqlite3
from typing import NamedTuple

import aiogram.types

import config


class UserData(NamedTuple):
    Lastname: str
    Name: str
    SecondName: str
    DocNumber: int


if not os.path.exists(config.DB_FILENAME):
    connection = sqlite3.connect(config.DB_FILENAME)
    connection.execute(open('sql/create_db.sql').read())
    connection.commit()
else:
    connection = sqlite3.connect(config.DB_FILENAME)


def is_user_registered(user_id: int) -> bool:
    user_registered_query_template = open('sql/is_user_registered_template.sql').read()
    cur = connection.cursor()
    cur.execute(user_registered_query_template.format(user_id))
    return cur.fetchone() is not None


def register_user(message: aiogram.types.Message) -> None:
    register_query_template = open('sql/register_user_template.sql').read()

    connection.cursor().execute(register_query_template.format(
        message.from_user.id, *message.text.split()
    ))

    connection.commit()


def get_user_data(user_id: int) -> UserData:
    get_user_data_template = open('sql/get_user_data_template.sql').read()
    cur = connection.cursor()
    cur.execute(get_user_data_template.format(user_id))
    return UserData(
        *cur.fetchone()
    )


def unregister_user(user_id: int) -> None:
    connection.cursor().execute(
        open('sql/unregister_user_template.sql').read().format(user_id)
    )
    connection.commit()
