from db.database import *

def get_user(user_id):
    db = ScorpDb()
    conn = db.open_connection()
    cursor = conn.cursor()
    
    sql = "select * from user where id = ?"
    user = cursor.execute(sql, (user_id,)).fetchone()
    
    if user is not None:
        return User(**user)
    
    return user

def main():
    user = get_user(12)
    print(user)

if __name__ == "__main__":
    main()
