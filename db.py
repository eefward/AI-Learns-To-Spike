import sqlite3

con = sqlite3.connect("moves.db")
cur = con.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS intervals (
        interval INT PRIMARY KEY,
        dict TEXT NOT NULL
    )
''')

a = {}
seconds = 6
tick = .25

while (tick <= seconds):
    interval = tick * 4
    exists = cur.execute("SELECT interval FROM intervals WHERE interval = ?", (interval,)).fetchone()

    if (exists):
        ...
    else:
        a["rt"] = .125
        a["rm"] = .125
        a["rb"] = .125
        a["mt"] = .125
        a["mm"] = .125
        a["mb"] = .125
        a["lt"] = .125
        a["lm"] = .125
        a["lb"] = .125

        cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (interval, str(a)))
        a.clear()

    tick += .25

con.commit()