import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Read existing student data from CSV file
df = pd.read_csv('student_data.csv')

@app.route('/', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        name = request.form['name']
        mis = request.form['mis']
        attendance = request.form['attendance']
        academics = request.form['academics']
        extra = request.form['extra']

        # Create a new DataFrame with the submitted data
        new_data = pd.DataFrame({
            'Name': [name],
            'MIS': [mis],
            'Attendance': [attendance],
            'Academic Marks': [academics],
            'Extracurricular Marks': [extra]
        })

        # Append the new data to the existing DataFrame
        updated_df = pd.concat([df, new_data])

        # Save the updated DataFrame back to the CSV file
        updated_df.to_csv('student_data.csv', index=False)

        return render_template('firstPage.html', success_message='Login Successful!')

    return render_template('firstPage.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('http://127.0.0.1:5001')
def next_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)
