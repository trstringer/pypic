"""API to persist and read upload data metrics"""

import os
import sqlite3

DATABASE_FILENAME = os.path.expanduser('~/pypic.db')


def create_upload_table():
    """Create the necessary database objects for upload monitoring and
    persistent data regarding all things video uploads
    """

    db_connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = db_connection.cursor()
    if not len(
            cursor.execute(
                'select * from sqlite_master where name = ?',
                ('uploads',)
            ).fetchall()):
        cursor.execute(
            '''create table uploads (
                date_created text,
                file_name text,
                uploaded integer,
                other_info text
            )'''
        )


def insert_upload_data(file_name, date_created, is_uploaded, other_info):
    """Insert the necessary data to reflect whether or not a video was
    uploaded
    """

    db_connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = db_connection.cursor()
    cursor.execute(
        'insert into uploads values (?, ?, ?, ?)',
        (str(date_created), file_name, int(is_uploaded), other_info)
    )
    db_connection.commit()
    db_connection.close()
