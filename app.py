from flask import Flask, render_template, request, redirect, url_for, session, json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui_12345'  # Cambia esto en producción

# Cargar lecciones
with open('data/lessons.json', 'r', encoding='utf-8') as f:
    lessons = json.load(f)

# Contexto global para user
@app.context_processor
def inject_user():
    return {'user': session.get('user')}

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', lessons=lessons)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', 'Usuario').strip()
        if not username:
            username = 'Usuario'
            
        session['user'] = {
            'name': username,
            'joined': datetime.now().strftime('%Y-%m-%d'),
            'xp': 0,
            'streak': 1,
            'completed_lessons': []
        }
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/lesson/<int:lesson_id>')
def lesson_detail(lesson_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    if not lesson:
        return redirect(url_for('index'))
    
    return render_template('lesson_detail.html', lesson=lesson)

@app.route('/quiz/<int:lesson_id>', methods=['GET', 'POST'])
def quiz(lesson_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    if not lesson:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        score = 0
        for question in lesson['quiz']:
            if request.form.get(f'q{question["id"]}') == question['correct_answer']:
                score += 1
        
        # Actualizar progreso del usuario
        if lesson_id not in session['user']['completed_lessons']:
            session['user']['completed_lessons'].append(lesson_id)
            session['user']['xp'] += score * 10
            session.modified = True
        
        return render_template('quiz_result.html', 
                            lesson=lesson,
                            score=score,
                            total=len(lesson['quiz']))
    
    return render_template('quiz.html', lesson=lesson)

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    os.makedirs('static/images/lessons', exist_ok=True)
    app.run(debug=True)
