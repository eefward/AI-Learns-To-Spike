import ast
import sqlite3
import random


class DB:
    def __init__(self, lowerbound: float, upperbound: float, starting: float, tick: float, seconds: float) -> None:
        # Handle cases that don't make sense
        if seconds % tick != 0:
            raise Exception("Seconds has to be divisible by ticks")
        elif tick < 0 and seconds < tick:
            raise Exception("Invalid ticks/seconds")
        elif lowerbound < 0 and upperbound < lowerbound and not (lowerbound < starting < upperbound):
            raise Exception("Invalid bounds")
        
        # Initialize variables
        self.con = sqlite3.connect(f"moves.db")
        self.cur = self.con.cursor()
        self.length = int(seconds // tick)
        self.points = starting * 8

        # Initialize database
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS intervals (
                interval INT PRIMARY KEY,
                dict TEXT NOT NULL
            )
        ''')

        moves = str({
            'rt': starting,
            'rm': starting, 
            'rb': starting, 
            'mt': starting, 
            'mb': starting, 
            'lt': starting, 
            'lm': starting, 
            'lb': starting
        })

        for i in range(1, self.length + 1): 
            self.cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (i, moves))
        
        self.con.commit()


    def get_db(self, i: int) -> dict:
        d = self.cur.execute("SELECT dict FROM intervals WHERE interval = ?", (i,)).fetchone()
        if not d:
            raise Exception(f"Nothing at interval {i}")

        return ast.literal_eval(d[0])
    

    def learn(self, action: list) -> None:
        for i in range(1, self.length + 1):
            probability = self.get_db(i)

            judgement, move, points = action[i]
            chance = probability[move]
            if judgement == 'good' and chance < 10:
                if chance + points > 10:
                    self.points += 10 - chance
                    probability[move] = 10
                else: 
                    probability[move] += points
                    self.points += points
            elif judgement == 'bad' and chance > 1:
                if chance - points < 1:
                    self.points -= chance - 1
                    probability[move] = 1
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
