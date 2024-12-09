from flask import Flask, render_template, request, redirect, url_for, session, send_file
from fpdf import FPDF
import random

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

# Questions pool
questions = [
    "What is your full name?",
    "What is your date of birth?",
    "What is your ethnicity?",
    "Where are you from? (Origin)",
    "What is something you're grateful for today?",
    "What’s a small act of kindness you’ve done recently?",
    "What habit would you like to develop, and why?",
    "If you could live anywhere, where would it be, and what draws you to that place?",
    "What’s the best advice you’ve ever received?",
    "How do you deal with stress and pressure?",
    "What’s something you’ve learned about yourself recently?",
    "How do you define success?",
    "What does your ideal day look like?",
    "What’s your favorite way to spend your free time?",
    "Who or what has had the greatest influence on your life so far?",
    "What’s a goal you’re working towards right now?",
    "What do you value most in a friendship?",
    "What’s one thing you wish you could change about your routine?",
    "If you had an extra hour in your day, how would you spend it?",
    "What’s something you’re curious about right now?",
    "How do you typically make decisions?",
    "When was the last time you stepped out of your comfort zone?",
    "What do you think is your greatest strength?",
    "What’s something you struggle with but wish you were better at?"
]

# Helper functions
def initialize_session():
    if 'responses' not in session:
        session['responses'] = []
    if 'asked_questions' not in session:
        session['asked_questions'] = []
    if 'total_questions' not in session:
        session['total_questions'] = len(questions)
    if 'asked_count' not in session:
        session['asked_count'] = 0

def ask_random_question():
    available_questions = list(set(questions) - set(session['asked_questions']))
    if not available_questions:
        return None
    question = random.choice(available_questions)
    session['asked_questions'].append(question)
    session['asked_count'] += 1
    return question

@app.route('/')
def home():
    initialize_session()
    question = ask_random_question()
    if not question:
        return redirect(url_for('summary'))
    return render_template('index.html', question=question)

@app.route('/submit', methods=['POST'])
def submit_response():
    response = request.form.get('response')
    if response:
        session['responses'].append({
            'question': session['asked_questions'][-1],
            'response': response
        })
    return redirect(url_for('home'))

@app.route('/summary')
def summary():
    return render_template('summary.html', responses=session.get('responses', []))

@app.route('/download')
def download_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Character Portfolio", ln=True, align='C')

    responses = session.get('responses', [])
    for entry in responses:
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 10, f"Q: {entry['question']}\nA: {entry['response']}\n")
        pdf.ln(5)

    file_path = "character_portfolio.pdf"
    pdf.output(file_path)
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
