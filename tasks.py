import sqlite3
from typing import List, Optional, Tuple


DB_PATH = "database.db"


def get_conn():
return sqlite3.connect(DB_PATH, check_same_thread=False)




def add_task(creator: str, direction: str, source_text: str, reference_translation: str | None, target_lang: str) -> int:
conn = get_conn()
cur = conn.cursor()
cur.execute(
"""
INSERT INTO tasks (creator, direction, source_text, reference_translation, target_lang)
VALUES (?, ?, ?, ?, ?)
""",
(creator, direction, source_text.strip(), (reference_translation or '').strip() or None, target_lang),
)
conn.commit()
task_id = cur.lastrowid
conn.close()
return task_id




def list_tasks() -> List[Tuple[int, str, str]]:
conn = get_conn()
cur = conn.cursor()
cur.execute("SELECT id, direction, substr(source_text,1,120) FROM tasks ORDER BY id DESC")
rows = cur.fetchall()
conn.close()
return rows




def get_task(task_id: int) -> Optional[tuple]:
conn = get_conn()
cur = conn.cursor()
cur.execute(
"SELECT id, direction, source_text, reference_translation, target_lang FROM tasks WHERE id = ?",
(task_id,),
)
row = cur.fetchone()
conn.close()
return row




def store_submission(username: str, task_id: int | None, source_text: str, mt_text: str, user_edit: str, points: int, time_spent_sec: float):
conn = get_conn()
cur = conn.cursor()
cur.execute(
"""
INSERT INTO submissions (username, task_id, source_text, mt_text, user_edit, points, time_spent_sec)
VALUES (?, ?, ?, ?, ?, ?, ?)
""",
(username, task_id, source_text, mt_text, user_edit, int(points), float(time_spent_sec)),
)
conn.commit()
conn.close()