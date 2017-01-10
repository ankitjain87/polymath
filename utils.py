import os
import requests
import sqlite3

import config


def is_db_exists():
    return True if os.path.isfile(config.DB_NAME) else False

def connect_db():
    try:
        con = sqlite3.connect(config.DB_NAME)
        return con
    except Exception as ex:
        print("Connection Error", ex)

def is_table_exists(table_name='category'):
    try:
        con = connect_db()
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "';"
        cursor = con.execute(query)
        cursor = cursor.fetchall()
        return True if len(cursor) > 0 else False
    except Exception as ex:
        print("Error in checking if table exists.", ex)

def create_category_table():
    try:
        con = connect_db()
        con.execute(config.CATEGORY_TABLE)
        con.close()
    except Exception as ex:
        print("Error in Category table creation.", ex)

def drop_category_table():
    try:
        con = connect_db()
        con.execute(config.DROP_TABLE)
        con.close()
    except Exception as ex:
        print("Error in Drop Category table.", ex)

def insert_category_data(data):
    try:
        con = connect_db()
        con.executemany(config.INSERT_STMT, data)
        con.commit()
        con.close()
        print("Data inserted successfully.")
    except Exception as ex:
        print("Error in inserting data in category table.", ex)

def dispatch_http_post_request(end_point, payload, headers):
    response = requests.post(end_point, data=payload, headers=headers)
    return response

def get_category_data(category_id):
    try:
        con = connect_db()
        stmt = config.SELECT_STMT + 'where category_id=' + str(category_id)
        cursor = con.execute(stmt)
        data = cursor.fetchall()
        con.close()
        return data
    except Exception as ex:
        print('Error while getting data for a category', category_id, ex)

def get_category_children(category_id):
    try:
        con = connect_db()
        stmt = config.SELECT_STMT + 'where parent_id=' + str(category_id)
        cursor = con.execute(stmt)
        data = cursor.fetchall()
        con.close()
        return data
    except Exception as ex:
        print('Error while getting children for a category', category_id, ex)

