import sqlite3 as sql

conn = sql.connect('database.db')
print("Opened database successfully")

# if not conn.execute(tb_exists).fetchone():
#     conn.execute(tb_create)
conn.execute('CREATE TABLE IF NOT EXISTS sentiment_analysis (review TEXT, prediction TEXT)')
print("Table created successfully")
cur = conn.cursor()
columns = [i[1] for i in cur.execute('PRAGMA table_info(sentiment_analysis)')]
print(columns)

if 'feedback' not in columns:
    conn.execute('ALTER TABLE sentiment_analysis ADD COLUMN feedback TEXT')
else:
    print("it is there")    
conn.close()