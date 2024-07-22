from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection configuration
db_config = {
    'user': 'root',
    'password': '',  # Add your MySQL password if you have one
    'host': 'localhost',
    'database': 'testimonials_db'
}

# Initialize database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, testimonial FROM testimonials")
    testimonials = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', testimonials=testimonials)

@app.route('/leave-review')
def leave_review():
    return render_template('review.html')

@app.route('/submit_testimonial', methods=['POST'])
def submit_testimonial():
    name = request.form['name']
    testimonial = request.form['testimonial']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO testimonials (name, testimonial) VALUES (%s, %s)', (name, testimonial))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/')

# Add routes for additional pages
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery-volunteer.html')

@app.route('/talkshow')
def talkshow():
    return render_template('talkshow.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
