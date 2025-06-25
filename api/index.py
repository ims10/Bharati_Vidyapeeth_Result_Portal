from flask import Flask, render_template, request, session, redirect
import pandas as pd
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key

def load_data():
    return pd.read_excel("students.xlsx")

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/result', methods=['POST'])
def result():
    prn = request.form['prn'].strip()
    df = load_data()

    student_row = df[df['PRN'].astype(str) == prn]

    if not student_row.empty:
        student = student_row.iloc[0]
        subject_names = [
            "Data Warehousing and Mining",
            "Web Programming (PHP)",
            "Software Project Management",
            "Knowledge Management",
            "Lab on Programming with Project",
            "Lab on Data Visualization",
            "Digital Marketing",
            "Indian Culture"
        ]
        marks = [int(student[f'Sub{i}']) for i in range(1, 9)]
        credits = list(map(int, str(student['Credits']).split(',')))
        grades = str(student['Grade']).split(',')
        gradepoints = list(map(int, str(student['GradePoints']).split(',')))

        subjects = []
        for i in range(8):
            subjects.append({
                'name': str(subject_names[i]),
                'marks': int(marks[i]),
                'credit': int(credits[i]),
                'grade': str(grades[i]),
                'gradepoint': int(gradepoints[i])
            })

        total_credits = sum(credits)
        weighted_score = sum(c * g for c, g in zip(credits, gradepoints))
        sgpa = round(weighted_score / total_credits, 2) if total_credits else 0.0

        session['student_data'] = {
            'prn': str(prn),
            'name': str(student['Name']),
            'semester': str(student['Semester']),
            'subjects': subjects,
            'sgpa': float(sgpa)
        }

        return render_template('result.html', student=session['student_data'], year=datetime.datetime.now().year)

    return "PRN not found. Please try again."

@app.route('/popup')
def popup():
    return render_template('popup.html')

if __name__ == '__main__':
    app.run(debug=True)
