import os
import sqlite3
import logging
from sqlite3 import Error

DB_FILE = str(os.getcwd()) + "/database.db"


class Database:
    def __init__(self):
        self.path = DB_FILE

    def _connect_DB(self):
        """
        Connect the Database
        """
        conn = None
        try:
            conn = sqlite3.connect(self.path)
        except Error as err:
            logging.error("Error occurred while connecting database {}".format(
                str(err))
            )
        return conn

    def _close_connection(self, connection):
        """
        CLose the database connection
        """
        connection.commit()
        connection.close()

    def create_table(self):
        """
        Create movie table to store the movie data
        """
        conn = self._connect_DB()
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS url_table (id INT, url, visit_count INT);"
        )
        self._close_connection(conn)

    def check_if_url_present(self, cur, url):
        # Check if the url is already present
        # If the url is already present, then
        # increase the visit count by 1
        # And get the id of the url
        cur.execute("SELECT id FROM url_table WHERE url =?", (url,))
        url_id = cur.fetchall()
        if url_id:
            # Get the visit count of the url
            cur.execute("SELECT visit_count FROM url_table WHERE url =?", (url,))
            visit_count = cur.fetchall()
            # Update the visit count
            cur.execute("UPDATE url_table "
                        "set visit_count = ? WHERE url = ?", (visit_count+1, url,))
            return url_id
        else:
            return False

    def get_id(self, cur, url):
        """
        Fetch the url_id from database
        """
        # If the url is not present, then fetch the
        # Max row id and return the id = max row id+1
        cur.execute("SELECT count(*) FROM url_table")
        url_id = cur.fetchone()
        return url_id[0]+1

    def insert_movie_data(self, url):
        """
        Insert the url data into database table
        """
        url_id = 0
        conn = self._connect_DB()
        cur = conn.cursor()
        # Check if the url is present
        check_status = self.check_if_url_present(cur, url)
        if not check_status:
            url_id = self.get_id(cur, url)
            print(url_id)
            print(url)
            cur.executemany(
                'INSERT INTO url_table VALUES(?,?,?);',
                (url_id, url, 1,)
            )
            self._close_connection(conn)
        else:
            url_id = check_status
        return url_id

