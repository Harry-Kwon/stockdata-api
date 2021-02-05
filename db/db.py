#%%
import json
from pathlib import Path

import psycopg2

connection = None
cursor = None

def open_connection():
    global connection, cursor
    with open(Path(__file__).parent.joinpath("../secrets.json"), "r") as readfile:
        data = json.load(readfile)["db"]

        connection = psycopg2.connect(database=data["database"],
            user=data["username"],
            password=data["password"],
            host=data["host"],
            port=data["port"])

        cursor = connection.cursor()

def write_meta(ticker, name, start_date):
    # first check if ticker entry exists in meta table
    query = "SELECT ticker FROM meta_data WHERE ticker = %s"
    try:
        cursor.execute(query, (ticker,))
    except psycopg2.InterfaceError as e:
        # if the connection is closed, reopen the connection and try the query
        print(e.message)
        open_connection()
        cursor.execute(query, (ticker,))



    if cursor.fetchone() is None:
        # insert new entry for ticker
        query = "INSERT INTO meta_data VALUES (%s, %s, %s)"
        cursor.execute(query, (ticker, name, start_date))
    else:
        # update entry for ticker
        query = """UPDATE meta_data SET company_name = %s, data_start_date = %s
            WHERE ticker = %s"""
        cursor.execute(query, (name, start_date, ticker))
    connection.commit()

def write_latest_price(ticker, open_price, high_price, low_price, close_price, volume, updated_date):
    # first check if ticker entry exists in table
    query = "SELECT ticker FROM latest_price WHERE ticker = %s"
    cursor.execute(query, (ticker,))

    if cursor.fetchone() is None:
        # insert new entry for ticker
        query = "INSERT INTO latest_price VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (ticker, open_price, high_price, low_price, close_price, volume, updated_date))
    else:
        # update entry for ticker
        query = """UPDATE latest_price SET
            open_price = %s,
            high_price = %s,
            low_price = %s,
            close_price = %s,
            volume = %s,
            updated_date = %s
            WHERE ticker = %s"""
        cursor.execute(query, (open_price, high_price, low_price, close_price, volume, updated_date, ticker))
    connection.commit()

open_connection()

if __name__ == "__main__":
    import datetime
    write_meta("AMZN", "Bezos Land", datetime.date(2018, 4, 23))
    write_latest_price("AMZN", 100.0, 200.0, 50.0, 110.0, 70005059)