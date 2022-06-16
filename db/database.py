from abc import abstractmethod
import sqlite3
import time
from sqlite3 import Error

class User():
    def __init__(self,id,username,email,full_name,profile_picture,bio,created_at):
        self.id = id
        self.username = username
        self.email = email
        self.full_name = full_name
        self.profile_picture = profile_picture
        self.bio = bio
        self.created_at = created_at
        self.followed = False
        
    def __repr__(self) -> str:
        return repr((self.id, self.username, self.email, self.full_name, self.followed, self.created_at))

class Post():
    def __init__(self,id,description,user_id,image,created_at):
        self.id = id
        self.description = description
        self.user_id = user_id
        self.image = image
        self.created_at = created_at
        self.owner = None
        self.liked = False
        
    def __repr__(self) -> str:
        return repr((self.id, self.description, self.owner, self.liked, self.created_at))

class Like():
    def __init__(self,id,post_id,user_id,created_at):
        self.id = id
        self.post_id = post_id
        self.user_id = user_id
        self.created_at = created_at
        
    def __repr__(self) -> str:
        return repr((self.id, self.post_id, self.user_id, self.created_at))

class Follow():
    def __init__(self,follower_id,following_id,created_at):
        self.follower_id = follower_id
        self.following_id = following_id
        self.created_at = created_at
        
    def __repr__(self) -> str:
        return repr((self.follower_id, self.following_id, self.created_at))

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Database():
    def __init__(self, db) -> None:
        self.db = db
        self.open_connection()
    
    def open_connection(self):
        self.connection = sqlite3.connect(self.db)
        self.connection.row_factory = dict_factory

        return self.connection

    def close_connection(self):
        self.connection.close()

    @abstractmethod
    def initialize_tables(self):
        pass
    
    @abstractmethod
    def seed(self):
        pass

class ScorpDb(Database):
    def __init__(self) -> None:
        super().__init__("./db/scorp.db")

    def get_users(self):
        pass

    def initialize_tables(self):
        sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        email text,
                                        full_name text,
                                        profile_picture text,
                                        bio text,
                                        created_at integer
                                    ); """
        sql_create_post_table = """ CREATE TABLE IF NOT EXISTS post (
                                        id integer PRIMARY KEY,
                                        description text NOT NULL,
                                        user_id integer,
                                        image text,
                                        created_at integer,
                                        FOREIGN KEY (user_id) REFERENCES user (id)
                                    ); """
        sql_create_like_table = """ CREATE TABLE IF NOT EXISTS like (
                                        id integer PRIMARY KEY,
                                        post_id integer,
                                        user_id integer,
                                        created_at integer,
                                        FOREIGN KEY (post_id) REFERENCES post (id),
                                        FOREIGN KEY (user_id) REFERENCES user (id)
                                    ); """
        sql_create_follow_table = """ CREATE TABLE IF NOT EXISTS follow (
                                        follower_id integer,
                                        following_id integer,
                                        created_at integer,
                                        FOREIGN KEY (follower_id) REFERENCES user (id),
                                        FOREIGN KEY (following_id) REFERENCES user (id)
                                    ); """
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql_create_user_table)
            self.cursor.execute(sql_create_post_table)
            self.cursor.execute(sql_create_like_table)
            self.cursor.execute(sql_create_follow_table)
        except Error as e:
            print(e)

    def seed(self):
        try:
            self.cursor = self.connection.cursor()

            created_at = int(round(time.time()))

            #if there is a record in table then do not execute insert querys
            users = self.cursor.execute("select 1 from user limit 1").fetchall()
            if len(users) > 0:
                return

            sql_insert_user_table = """
                insert into user (username,email,full_name,profile_picture,bio,created_at)
                values (?,?,?,?,?,?)
                """
            self.cursor.execute(sql_insert_user_table, ("davut", "davut@eryil.maz", "Davut Eryilmaz", "davut.png", "davut eryilmaz 1995 diyarbakir dogumlu", created_at))
            self.cursor.execute(sql_insert_user_table, ("ali", "ali@eryil.maz", "Ali Demir", "ali.png", "ali eryilmaz 1995 diyarbakir dogumlu", created_at))
            self.cursor.execute(sql_insert_user_table, ("veli", "veli@eryil.maz", "Veli Kaan", "veli.png", "veli eryilmaz 1995 diyarbakir dogumlu", created_at))
            self.cursor.execute(sql_insert_user_table, ("can", "can@eryil.maz", "Can Ceylan", "can.png", "can eryilmaz 1995 diyarbakir dogumlu", created_at))

            sql_insert_post_table = """
                insert into post (description,user_id,image,created_at)
                values (?,?,?,?)
                """
            self.cursor.execute(sql_insert_post_table, ("test post 1", 1, "post1.png", created_at))
            self.cursor.execute(sql_insert_post_table, ("test post 2", 1, "post2.png", created_at))
            self.cursor.execute(sql_insert_post_table, ("test post 3", 2, "post3.png", created_at+3))
            self.cursor.execute(sql_insert_post_table, ("test post 4", 3, "post4.png", created_at+4))

            sql_insert_like_table = """
                insert into like (post_id,user_id,created_at)
                values (?,?,?)
            """
            self.cursor.execute(sql_insert_like_table, (1,2,created_at))
            self.cursor.execute(sql_insert_like_table, (1,3,created_at))
            self.cursor.execute(sql_insert_like_table, (2,3,created_at))
            self.cursor.execute(sql_insert_like_table, (3,1,created_at))

            sql_insert_follow_table = """
                insert into follow (follower_id,following_id,created_at)
                values (?,?,?)
            """
            self.cursor.execute(sql_insert_follow_table, (1,2,created_at))
            self.cursor.execute(sql_insert_follow_table, (2,1,created_at))
            self.cursor.execute(sql_insert_follow_table, (2,3,created_at))
            self.cursor.execute(sql_insert_follow_table, (3,4,created_at))

            self.connection.commit()
        except Error as e:
            print(e)

def main():
    db = ScorpDb()
    db.initialize_tables()
    db.seed()
    db.close_connection()

if __name__ == "__main__":
    main()
