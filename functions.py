import sqlite3

class DB:
    def __init__(self, tick: float, seconds: float):
        self.con = sqlite3.connect("moves.db")
        self.cur = self.con.cursor()

        if (seconds % tick != 0):
            raise Exception("Seconds has to be divisible by ticks")

        self.tick = tick
        self.seconds = seconds
    
    def create_db(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS intervals (
                interval INT PRIMARY KEY,
                dict TEXT NOT NULL
            )
        ''')

        moves = str({
            'rt': 5,
            'rm': 5, 
            'rb': 5, 
            'mt': 5, 
            'mb': 5, 
            'lt': 5, 
            'lm': 5, 
            'lb': 5
        })
        
        # Initialize the database at every interval
        length = int(self.seconds / self.tick)
        for i in range(1, length): 
            self.cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (i, moves))