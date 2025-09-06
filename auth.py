import sqlite3


def authenticate_user(username: str, password: str) -> Optional[str]:
conn = get_conn()
cur = conn.cursor()
cur.execute(
"SELECT role, password_hash FROM users WHERE username = ?",
(username,),
)
row = cur.fetchone()
conn.close()
if not row:
return None
role, pw_hash = row
return role if hash_password(password) == pw_hash else None




# ---------- Scores & Leaderboard ----------


def add_score(username: str, points: int):
conn = get_conn()
cur = conn.cursor()
cur.execute("UPDATE users SET score = score + ? WHERE username = ?", (points, username))
conn.commit()
conn.close()




def get_user_score(username: str) -> int:
conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT score FROM users WHERE username = ?", (username,))
row = cur.fetchone()
conn.close()
return int(row[0]) if row else 0




def get_leaderboard(limit: int = 20) -> List[tuple]:
conn = get_conn()
cur = conn.cursor()
cur.execute(
"SELECT username, score FROM users ORDER BY score DESC, username ASC LIMIT ?",
(limit,),
)
rows = cur.fetchall()
conn.close()
return rows