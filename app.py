from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados SQLite
def init_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY, name TEXT, price REAL, description TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add_product', methods=['POST'])

def add_product():
    name = request.form['name']
    price = request.form['price']
    description = request.form['description']

    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name, price, description) VALUES (?, ?, ?)', (name, price, description))
    conn.commit()
    conn.close()

    return redirect('/')

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        cursor.execute('UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?', (name, price, description, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
        product = cursor.fetchone()
        conn.close()
        return render_template('edit.html', product=product)

@app.route('/delete_product/<int:id>')
def delete_product(id):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
