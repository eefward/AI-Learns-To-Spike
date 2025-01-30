import ast
import sqlite3
import random


class DB:
    def __init__(self, tick: float, seconds: float) -> None:
        self.con = sqlite3.connect("moves.db")
        self.cur = self.con.cursor()

        if (seconds % tick != 0):
            raise Exception("Seconds has to be divisible by ticks")
        elif (tick < 0 or seconds < 0):
            raise Exception("Cannot be negative")
        
        self.tick = tick
        self.seconds = seconds
        self.length = int(seconds / tick)
        self._points = 0


    def create_db(self) -> None:
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS intervals (
                interval INT PRIMARY KEY,
                dict TEXT NOT NULL
            )
        ''')

        self._points = 40
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
        for i in range(1, self.length): 
            self.cur.execute("INSERT INTO intervals (interval, dict) VALUES (?, ?)", (i, moves))
        
        self.con.commit()


    def get_db(self, i: int) -> dict:
        d = self.cur.execute("SELECT dict FROM intervals WHERE interval = ?", (i + 1,)).fetchone()
        if not d:
            raise Exception("Nothing in database")

        return ast.literal_eval(dict[0])
    

    def learn(self, action: list) -> None:
        for i in range(self.length):
            probability = self.get_db(i)

            judgement, move, points = action[i]
            chance = probability[move]
            if judgement == 'good' and chance < 10:
                if chance + points > 10:
                    self._points += 10 - chance
                    probability[move] = 10
                else: 
                    probability[move] += points
                    self._points += points
            elif judgement == 'bad' and chance > 1:
                if chance - points < 1:
                    self._points -= chance - 1
                    probability[move] = 1
                else:
                    probability[move] -= points
                    self._points -= points
            
            self.cur.execute("UPDATE intervals SET dict = ? WHERE interval = ?", (str(probability), i + 1))
        
        self.con.commit()
    

    def random_move(self, i: int) -> str:
        probability = self.get_db(i)

        while True:
            for move in probability:
                rand = random.randint(1, self._points) # Random number from 1 to total points
                if probability[move] >= rand: # Idk if this is too effective
                    return move
