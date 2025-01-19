import sqlite3
import ast

con = sqlite3.connect("moves.db")
cur = con.cursor()

def create_db(amount):
    con = sqlite3.connect("moves.db")
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS intervals (
            interval INT PRIMARY KEY,
            dict TEXT NOT NULL
        )
    ''')

    a = {'rt': 0.125, 
         'rm': 0.125, 
         'rb': 0.125, 
         'mt': 0.125, 
         'mb': 0.125, 
         'lt': 0.125, 
         'lm': 0.125, 
         'lb': 0.125}
    
    for i in range(1, amount + 1):
        cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (i, str(a)))

    con.commit()
    con.close()


def main(ticks, seconds):
    if seconds % ticks != 0: 
        raise Exception("Seconds has to be divisible by ticks")
    
    total = int(seconds/ticks)
    for i in range(1, total):
        d = cur.execute("SELECT dict FROM intervals WHERE interval = ?", (i,)).fetchone()
        if not d: raise Exception("Initialize a proper database!")


        a = ast.literal_eval(d[0])
        print(a)

    con.commit()


def wipe_db():
    con = sqlite3.connect("moves.db")
    cur = con.cursor()

    cur.execute("DROP TABLE intervals")

    con.commit()
    con.close()

create_db(24)
main(.25, 6)