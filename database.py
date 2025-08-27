import aiosqlite
from config import DB_NAME

async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY, 
            question_index INTEGER,
            current_score INTEGER DEFAULT 0
        )''')
        
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        await db.commit()

async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT OR REPLACE INTO quiz_state (user_id, question_index, current_score) VALUES (?, ?, COALESCE((SELECT current_score FROM quiz_state WHERE user_id = ?), 0))',
            (user_id, index, user_id)
        )
        await db.commit()

async def get_user_score(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT current_score FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result else 0

async def update_user_score(user_id, score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'UPDATE quiz_state SET current_score = ? WHERE user_id = ?',
            (score, user_id)
        )
        await db.commit()

async def save_quiz_result(user_id, username, score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            'INSERT INTO quiz_results (user_id, username, score) VALUES (?, ?, ?)',
            (user_id, username, score)
        )
        await db.commit()

async def get_user_stats(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            'SELECT score FROM quiz_results WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1',
            (user_id,)
        ) as cursor:
            last_score = await cursor.fetchone()
        
        async with db.execute(
            'SELECT COUNT(*) FROM quiz_results WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            total_attempts = await cursor.fetchone()
        
        async with db.execute(
            'SELECT MAX(score) FROM quiz_results WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            best_score = await cursor.fetchone()
        
        return {
            'last_score': last_score[0] if last_score else 0,
            'total_attempts': total_attempts[0] if total_attempts else 0,
            'best_score': best_score[0] if best_score else 0
        }