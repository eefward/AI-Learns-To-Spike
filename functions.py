import ast
import sqlite3
import random


class DB:
    def __init__(self, min_probability_limit: float, max_probability_limit: float, base: float, tick: float, seconds: float) -> None:
        # Handle cases that don't make sense
        if (seconds * 10) % (tick * 10) != 0:  # error in this, 5 % 0.1 == 0.1, floating point innaccuracy
            raise Exception("Seconds has to be divisible by ticks")
        elif tick < 0 and seconds < tick:
            raise Exception("Invalid ticks/seconds")
        elif min_probability_limit < 0 and max_probability_limit < min_probability_limit and not (min_probability_limit < base < max_probability_limit):
            raise Exception("Invalid bounds")
        
        # Initialize variables
        self.con = sqlite3.connect(f"moves.db")
        self.cur = self.con.cursor()
        self.length = int(seconds // tick)
        self.lowerbound = min_probability_limit
        self.upperbound = max_probability_limit
        self.points = base * 8

        # Initialize database
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS intervals (
                interval INT PRIMARY KEY,
                dict TEXT NOT NULL
            )
        ''')

        moves = str({
            'rt': base, #right top
            'rm': base, #right middle
            'rb': base, #right bottom
            'mt': base, #middle top
            'mb': base, #middle bottom
            'lt': base, #left top
            'lm': base, #left middle
            'lb': base, #left bottom
            'n': base #no move
        })

        for i in range(1, self.length + 1): 
            self.cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (i, moves))
        
        self.con.commit()

    
    def delete_db(self) -> None:
        self.cur.execute("DROP TABLE intervals")
        self.con.commit()


    def get_db(self, i: int) -> dict:
        d = self.cur.execute("SELECT dict FROM intervals WHERE interval = ?", (i,)).fetchone()
        if not d:
            raise Exception(f"Nothing at interval {i}")

        return ast.literal_eval(d[0])
    
    def print_db(self) -> None: # NEW I NEED IT
            self.cur.execute("SELECT * FROM intervals")
            rows = self.cur.fetchall()
            
            for row in rows:
                print(dict(row)) 

    def learn(self, action: list) -> None:
        for i in range(1, self.length + 1):
            probability = self.get_db(i)

            judgement, move, points = action[i]
            chance = probability[move]
            if judgement == 'good' and chance < self.upperbound:
                if chance + points > self.upperbound:
                    self.points += self.upperbound - chance
                    probability[move] = self.upperbound
                else: 
                    probability[move] += points
                    self.points += points
            elif judgement == 'bad' and chance > self.lowerbound:
                if chance - points < self.lowerbound:
                    self.points -= chance - self.lowerbound
                    probability[move] = self.lowerbound
                else:
                    probability[move] -= points
                    self.points -= points
            
            self.cur.execute("UPDATE intervals SET dict = ? WHERE interval = ?", (str(probability), i))
        
        self.con.commit()
    

    def random_move(self, i: int) -> str:
        probability = self.get_db(i)

        while True:
            for move in probability:
                rand = random.randint(1, self.points) # Random number from 1 to total points
                if probability[move] >= rand: # Idk if this is too effective
                    return move

'''
db = DB(.1, 10, 5.0, .1, 10)
for i in range(1, 41):
    print(db.random_move(i))

db.delete_db()
'''