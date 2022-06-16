from ast import List
from db.database import *

def get_post_list(post_ids) -> dict:
    db = ScorpDb()
    conn = db.open_connection()
    cursor = conn.cursor()

    sql = "select * from post where id in ({seq})".format(seq=','.join(['?']*len(post_ids)))
    posts = cursor.execute(sql, post_ids).fetchall()
    return {Post(**post).id : Post(**post) for post in posts}

def get_post(post_id) -> Post:
    db = ScorpDb()
    conn = db.open_connection()
    cursor = conn.cursor()
    sql = "select * from post where id = ?"
    post = cursor.execute(sql, (post_id,)).fetchone()
    
    if post is not None:
        return Post(**post)

    return post

def main():
    post_list = get_post_list([1])
    print(post_list[2])

if __name__ == "__main__":
    main()
