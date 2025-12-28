import sqlite3
import os


class DB_Manager:
    def __init__(self, database):
        self.database = database
        
    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS videogames (
                          id INTEGER PRIMARY KEY,
                          name TEXT,
                          platform TEXT,
                          year_of_release INTEGER,
                          genre TEXT,
                          publisher TEXT,
                          critic_score REAL,
                          critic_count INTEGER,
                          user_score REAL,
                          developer TEXT,
                          rating TEXT
                        )''') 

            conn.commit()

    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        
    def random_game(self):
        sql = ''' 
            SELECT * FROM videogames ORDER BY RANDOM() LIMIT 1'''
        return self.__select_data(sql)
        
    def find_game_by_name(self, name):
        sql = ''' 
            SELECT * FROM videogames WHERE name LIKE ?'''
        name_pattern = f'%{name}%'
        return self.__select_data(sql, (name_pattern,))
            