import os
import psycopg2
from time import sleep

# Connect to CockroachDB
# run .  cockdb_env.sh first
connection = psycopg2.connect(os.environ['DATABASE_URL'])

def exec_statement(stmt):
    global connection
    conn = connection
    try:
        with conn.cursor() as cur:
            cur.execute(stmt)
            #row = cur.fetchone()
            conn.commit()
            #if row: print(row[0])
    except psycopg2.ProgrammingError as e:
        print("psycopg2.ProgrammingError ", e)
        connection.close()
        connection = psycopg2.connect(os.environ['DATABASE_URL'])
        return
    except psycopg2.errors.InFailedSqlTransaction as e:
        print("psycopg2.errors.InFailedSqlTransaction ", e)
        connection.close()
        connection = psycopg2.connect(os.environ['DATABASE_URL'])
        return
    # psycopg2.OperationalError: SSL connection has been closed unexpectedly
    except psycopg2.OperationalError as e:
        print("psycopg2.OperationalError ", e)
        connection.close()
        connection = psycopg2.connect(os.environ['DATABASE_URL'])
        return


def fetchall_statement(stmt):
    global connection
    conn = connection
    try:
        with conn.cursor() as cur:
            cur.itersize = 1024
            cur.execute(stmt)
            row = cur.fetchall()
            conn.commit()
            if row: 
              print("Total: ", len(row))
              for x in row: print(x)
    except psycopg2.ProgrammingError:
        return
    except psycopg2.errors.InFailedSqlTransaction:
        return


def init():

    statements = [
        # CREATE the messages table
        "CREATE TABLE IF NOT EXISTS stocks (id TEXT PRIMARY KEY , message STRING)",
        # INSERT a row into the messages table
        "INSERT INTO stocks (id, message) VALUES ('First Message', 'Hello world!')",
        # SELECT a row from the messages table
        "SELECT message FROM stocks"
    ]

    for statement in statements:
        exec_statement(statement)


def close():
    global connection
    # Close communication with the database
    connection.close()
    
# ('AAPL-1655072301.603004', '06/12/2022 18:18:21 | This is another test')
def save(tick, msg, wait=True):
    from datetime import datetime
    tm = str(datetime.now().timestamp())
    nowstr = datetime.now().strftime("%m/%d/%Y %H:%M:%S |")
    #statement = "INSERT INTO stocks (message) VALUES ('" + nowstr+ msg + "')"
    statement = "INSERT INTO stocks VALUES ('" + tick+"-"+ tm +"','"+ nowstr+" "+ msg + "')"
    exec_statement(statement)
    if wait: sleep(0.2)
def savetm(tick, msg, now, wait=True):
    #from datetime import datetime
    tm = str(now.timestamp())
    nowstr = now.strftime("%m/%d/%Y %H:%M:%S |")
    #statement = "INSERT INTO stocks (message) VALUES ('" + nowstr+ msg + "')"
    statement = "INSERT INTO stocks VALUES ('" + tick+"-"+ tm +"','"+ nowstr+" "+ msg + "')"
    exec_statement(statement)
    if wait: sleep(0.2)
"""
if random > 0 then it will return the <random> number of records. it is useful for a large table.
Do not use "order by" as it will scan the full tables and then sort which takes long in large table.
"""
def show(random=0):
    statement = "SELECT * FROM stocks"
    if random > 0: statement = "select * from stocks where random() < 0.01 limit " + str(random) +";"
    fetchall_statement(statement)

def showid(tick, random=0):
    statement = "SELECT * FROM stocks where id like '" + tick +"-%'"
    if random > 0: statement += " and random() < 0.01 limit " + str(random)
    statement += ";"
    fetchall_statement(statement)

if __name__ == "__main__":
    #init() # run only once 
    #save("AAPL", "This is another test")
    #show(100)
    showid("TSLA", 100)
