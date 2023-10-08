import asyncpg

DATABASE = {
    'user': 'YOUR USERNAME',
    'password': 'YOUR PASSWORD',
    'host': 'localhost',
    'port': '5432',
    'database': 'YOUR DATABASE'
}


async def get_conn():
    return await asyncpg.connect(**DATABASE)
