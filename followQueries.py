from db.database import *

def is_followed(follower_id, following_id):
    db = ScorpDb()
    conn = db.open_connection()
    cursor = conn.cursor()
    sql = "select * from follow where follower_id = ? and following_id = ?"
    followed = cursor.execute(sql, (follower_id,following_id,)).fetchone()
    
    return followed is not None

def main():
    isFollowed = is_followed(2, 4)
    print("is followed :", isFollowed)

if __name__ == "__main__":
    main()
