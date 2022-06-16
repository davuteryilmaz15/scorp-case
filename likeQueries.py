from db.database import *

def is_liked(user_id, post_id):
    db = ScorpDb()
    conn = db.open_connection()
    cursor = conn.cursor()
    sql = "select * from like where user_id = ? and post_id = ?"
    liked = cursor.execute(sql, (user_id,post_id,)).fetchone()
    
    return liked is not None

def main():
    isLiked = is_liked(1, 2)
    print(isLiked)

if __name__ == "__main__":
    main()
