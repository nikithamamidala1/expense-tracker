from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Routes ---
@app.route('/')
def index():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = c.fetchall()
    conn.close()

    total = sum([expense[2] for expense in expenses])
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
                  (title, amount, category, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_expense.html')

@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
