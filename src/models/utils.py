from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os
from sqlalchemy.inspection import inspect

import base
import user

def get_db_file() -> str:
    bd_directory = os.path.expanduser('~/.password_manager')

    if not os.path.exists(bd_directory):
        os.makedirs(bd_directory)

    return bd_directory + '/password_manager.sqlite3'


def get_session():
    return Session(get_engine())


def get_engine():
    return create_engine('sqlite:///'+ get_db_file(), echo=False)


def create_db():
    with get_session() as session:
        base.Base.metadata.create_all(get_engine())
        session.commit()

def check():
    inspector = inspect(get_engine())

    # Get the table names
    table_names = inspector.get_table_names()
    print(table_names)

    # Iterate over the table names
    for table_name in table_names:
        print("Table:", table_name)

        # Get the column names for each table
        column_names = inspector.get_columns(table_name)
        for column in column_names:
            print("Column:", column['name'])

        print()

if __name__ == '__main__':
    create_db()
    print(user.add('kubaa', 'k'))

    users = user.get_all()
    for userr in users:
        print(userr)