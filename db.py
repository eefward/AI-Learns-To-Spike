import sqlite3
import ast

con = sqlite3.connect("moves.db")
cur = con.cursor()

def create_db(amount: int):
    con = sqlite3.connect("moves.db")
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS intervals (
            interval INT PRIMARY KEY,
            dict TEXT NOT NULL
        )
    ''')

    a = {'rt': 5,
         'rm': 5, 
         'rb': 5, 
         'mt': 5, 
         'mb': 5, 
         'lt': 5, 
         'lm': 5, 
         'lb': 5}
    
    # Initialize the database at every interval
    for i in range(1, amount + 1): 
        cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (i, str(a)))

    con.commit()
    con.close()



def get_db() -> dict:
    con = sqlite3.connect("moves.db")
    cur = con.cursor()

    dict = cur.execute("SELECT dict FROM intervals").fetchone()
    if not dict: raise Exception("Nothing in database")

    return ast.literal_eval(dict[0])



def main(ticks: float, seconds: float, judgement: list) -> None:
    if seconds % ticks != 0: 
        raise Exception("Seconds has to be divisible by ticks")
    
    con = sqlite3.connect("moves.db")
    cur = con.cursor()
    
    total = int(seconds/ticks)
    for i in range(1, total):
        # Get the dictionary in the ith row of the database
        d = cur.execute("SELECT dict FROM intervals WHERE interval = ?", (i,)).fetchone()
        if not d: raise Exception("Initialize a proper database!")

        a = ast.literal_eval(d[0])
        if judgement[i][0] == 'good' and a[judgement[i][1]] < 10:
            a[judgement[i][1]] += 1
        elif judgement[i][0] == 'bad' and a[judgement[i][1]] > 1:
            a[judgement[i][1]] -= 1
        
        cur.execute("UPDATE intervals SET dict = ? WHERE interval = ?", (str(a), i))

    con.commit()



def wipe_db():
    con = sqlite3.connect("moves.db")
    cur = con.cursor()

    cur.execute("DROP TABLE intervals")

    con.commit()
    con.close()

