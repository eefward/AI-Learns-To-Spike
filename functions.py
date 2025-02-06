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
        self.con = sqlite3.connect("moves.db")
        self.cur = self.con.cursor()
        self.length = int(seconds // tick)
        self.lowerbound = min_probability_limit
        self.upperbound = max_probability_limit
        self.base = base
        self.points = base * 9

        # Initialize database
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS intervals (
                interval INT PRIMARY KEY,
                dict TEXT NOT NULL
            )
        ''')


    def create_rows(self) -> None:
        moves = str({
            'rt': self.base, #right top
            'rm':self. base, #right middle
            'rb': self.base, #right bottom
            'mt': self.base, #middle top
            'mb': self.base, #middle bottom
            'lt': self.base, #left top
            'lm': self.base, #left middle
            'lb': self.base, #left bottom
            'n': self.base #no move
        })

        for i in range(1, self.length + 1): 
            self.cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (i, moves))
        
        self.con.commit()


    
    def delete_db(self) -> None:
        self.cur.execute("DROP TABLE intervals") # Self explanatory
        self.con.commit()


    def get_db(self, interval: int) -> dict:
        d = self.cur.execute("SELECT dict FROM intervals WHERE interval = ?", (interval,)).fetchone()
        if not d:
            raise Exception(f"Nothing at interval {interval}")

        return ast.literal_eval(d[0]) # The entire dictionary at that interval
    

    def learn(self, action: list) -> None: # ex: [('good', 'lr', .2) * self.length]
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
    

    def print_db(self) -> None:
            data = self.cur.execute("SELECT * FROM intervals").fetchall()
            for interval in data:
                print(interval) # Prints the database in interval


    def random_move(self, i: int) -> str:
        probability = self.get_db(i)

        while True:
            for move in probability:
                rand = random.randint(1, self.points) # Random number from 1 to total points
                if probability[move] >= rand: # Idk if this is too effective
                    return move
                
'''
db = DB(.1, 10, 5.0, .1, 10)

db.print_db()
db.delete_db()
'''
