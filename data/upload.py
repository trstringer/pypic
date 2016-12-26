"""API to persist and read upload data metrics"""

import os
import sqlite3

DATABASE_FILENAME = os.path.expanduser('~/pypic.db')


def create_upload_dbobjects():
    """Create the necessary database objects for upload monitoring and
    persistent data regarding all things video uploads
    """

    db_connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = db_connection.cursor()
    cursor.execute(
        '''create table uploads (

        )'''
    )
