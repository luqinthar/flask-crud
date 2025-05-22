from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB_PATH = '/data/todo.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        conn.execute('CREATE TABLE todos (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL)')
        conn.commit()
        conn.close()

@app.route('/todos', methods=['GET'])
def list_todos():
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    conn.close()
    return jsonify([dict(row) for row in todos])

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json.get('task')
    if not task:
        return jsonify({'error': 'Task is required'}), 400
    conn = get_db_connection()
    conn.execute('INSERT INTO todos (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo added'}), 201

@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM todos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo deleted'})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
