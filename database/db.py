from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = 'data.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symptom TEXT NOT NULL,
                characteristic TEXT NOT NULL,
                synonyms TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def db():
    with get_db() as conn:
        items = conn.execute('SELECT * FROM item').fetchall()
    return render_template('db.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    symptom = request.form.get('symptom')
    characteristic = request.form.get('characteristic')
    synonyms = request.form.get('synonyms')
    with get_db() as conn:
        conn.execute('INSERT INTO item (symptom, characteristic, synonyms) VALUES (?, ?, ?)',
                     (symptom, characteristic, synonyms))
        conn.commit()
    return redirect(url_for('db'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    with get_db() as conn:
        conn.execute('DELETE FROM item WHERE id = ?', (item_id,))
        conn.commit()
    return redirect(url_for('db'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    if request.method == 'POST':
        symptom = request.form.get('symptom')
        characteristic = request.form.get('characteristic')
        synonyms = request.form.get('synonyms')
        with get_db() as conn:
            conn.execute('UPDATE item SET symptom = ?, characteristic = ?, synonyms = ? WHERE id = ?',
                         (symptom, characteristic, synonyms, item_id))
            conn.commit()
        return redirect(url_for('db'))

    with get_db() as conn:
        item = conn.execute('SELECT * FROM item WHERE id = ?', (item_id,)).fetchone()
    return render_template('edit.html', item=item)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)