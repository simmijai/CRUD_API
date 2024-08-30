from flask import Blueprint, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import os
from connection import get_connection

bp = Blueprint('student', __name__, url_prefix='/')

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM data")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html', data=data)

@bp.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        name = request.form.get('name')
        about = request.form.get('about')
        f = request.files.get('image')

        if f and f.filename:
            if allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(file_path)

                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO data (name, image, about) VALUES (%s, %s, %s)", (name, filename, about))
                connection.commit()
                cursor.close()
                connection.close()
                flash('Data inserted successfully!')
                return redirect(url_for('student.index'))
            else:
                flash('Invalid file type. Only JPG, JPEG, PNG, and GIF are allowed.')
        else:
            flash('No file selected.')

    return render_template('insert.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form.get('name')
        about = request.form.get('about')
        f = request.files.get('image')

        if f and f.filename:
            if allowed_file(f.filename):
                filename = secure_filename(f.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                f.save(file_path)
                cursor.execute("UPDATE data SET name=%s, image=%s, about=%s WHERE id=%s", (name, filename, about, id))
            else:
                flash('Invalid file type. Only JPG, JPEG, PNG, and GIF are allowed.')
        else:
            cursor.execute("UPDATE data SET name=%s, about=%s WHERE id=%s", (name, about, id))
        
        connection.commit()
        cursor.close()
        connection.close()
        flash('Data updated successfully!')
        return redirect(url_for('student.index'))

    cursor.execute("SELECT * FROM data WHERE id=%s", (id,))
    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return render_template('edit.html', data=data)

@bp.route('/delete/<int:id>')
def delete(id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM data WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()
    flash('Data deleted successfully!')
    return redirect(url_for('student.index'))


