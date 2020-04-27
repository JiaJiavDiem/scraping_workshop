# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Common functions

# code taken from http://www.sqlitetutorial.net/sqlite-python/creating-database/
import sqlite3
from sqlite3 import Error
import pandas as pd
import requests

# create a new database - not needed as the connection creates it if needed
# create connection
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print("conn open")
        print(sqlite3.version)
        return(conn)
    except Error as e:
        print(e)
# check out whether this does not close off the connection too early
    return None

# create table with paramaters connection and sql for table
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
        
# create table with paramaters connection and sql for table
def modify_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def read_CSV(file):
    df_CSV = pd.read_csv(file, sep=';')
    print(df_CSV.head())
    return df_CSV

def write_to_db(df, table, conn):
    df.to_sql(table, conn, if_exists="replace")
    
def retrieve_data(sql, conn):
    df_data = pd.read_sql_query(sql, conn)
    return df_data

def scrape(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
    res_1st = requests.get('http://' + url, headers=headers).text
    return res_1st

def write_to_db_scrape1(company, url, text, links_1st, id_link, conn):
    sql = """INSERT INTO firstScrape VALUES
            (
            ?,?,?,?,?
            )"""           
    list_values = [company, url, text, links_1st, id_link]
    print(list_values)        
    cur = conn.cursor()
    cur.execute(sql, list_values)
    conn.commit()
