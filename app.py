import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from flask import Flask, render_template, request

app = Flask(__name__)

class Student:
    extracurricular_scores = {
        "1 club": 70,
        "2 clubs": 75,
        "3 clubs": 80,
        "4 clubs": 85
    }
    def __init__(self, name, mis, attendance, extracurricular_marks, academic_marks):
        self.mis = mis
        self.name = name
        self.attendance = attendance
        self.extracurricular_marks = extracurricular_marks
        self.academic_marks = academic_marks * 10
        self.overall_progress = 0
        self.rank = 0
        
    def convert_extracurricular_marks(self):
        self.extracurricular_marks = self.extracurricular_scores.get(self.extracurricular_marks, 0)
    
    def calculate_overall_progress(self):
        self.convert_extracurricular_marks()
        attendance_weight = 0.3
        extracurricular_weight = 0.3
        academic_weight = 0.4

        attendance_progress = self.attendance * attendance_weight
        extracurricular_progress = float(self.extracurricular_marks) * extracurricular_weight
        academic_progress = self.academic_marks * academic_weight

        self.overall_progress = attendance_progress + extracurricular_progress + academic_progress
         
# Read student data from Excel file
df = pd.read_csv('student_data.csv')

# Create Student instances and populate the student list
students = []
for _, row in df.iterrows():
    name = row['Name']
    mis = row['MIS']
    attendance = row['Attendance']
    extracurricular_marks = row['Extracurricular Marks']
    academic_marks = row['Academic Marks']
    student = Student(name, mis, attendance, extracurricular_marks, academic_marks)
    students.append(student)

# Calculate overall progress for each student
for student in students:
    student.calculate_overall_progress()

# Sort students based on overall progress in descending order
students.sort(key=lambda x: x.overall_progress, reverse=True)

# Assign ranks to students
for i, student in enumerate(students):
    student.rank = i + 1

@app.route('/', methods=['GET', 'POST'])
def menu():
    
    if request.method == 'POST':
        student_mis = request.form['mis']
        choice = request.form['choice']

        if choice == "1":
            for student in students:
               #if student.mis.lower() == student_mis.lower():
               if str(student.mis) == str(student_mis):
                     if student.rank <= 5:
                        rank_message = f"Congratulations! Your rank is {student.rank}!"
                        top_students = students[:5]  # Get the top 5 students
                        student_scores = [s.overall_progress for s in top_students]  # Overall progress scores of top 5 students
                        student_labels = [s.name for s in top_students]  # Names of top 5 students

                        # Append the current student's score and label to the lists
                        student_scores.append(student.overall_progress)
                        student_labels.append(student.name)

                        # Create a figure and axes
                        fig, ax = plt.subplots()

                        # Plot the bar chart
                        ax.bar(student_labels, student_scores)

                        # Set labels and title
                        ax.set_xlabel("Student")
                        ax.set_ylabel("Overall Progress")
                        ax.set_title(f"Comparison of your Overall Progress with Top 5 Students")

                        # Save the figure to a BytesIO object
                        image_stream = io.BytesIO()
                        plt.savefig(image_stream, format='png')
                        image_stream.seek(0)

                        # Generate a base64 encoded string from the image stream
                        encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

                        # Close the figure
                        plt.close()
                        #rank_message = f"Congratulations! Your rank is {student.rank}!"
                        return render_template('index.html',rank_message=rank_message, student=student,student_rank_graph_image=encoded_image)
                     else:
                         rank_message = f"Your rank is {student.rank}"
                         return render_template('index.html', rank_message=rank_message, student=student)

            return render_template('index.html', error_message="Student not found!")

        elif choice == "2":
            for student in students:
                #if student.mis.lower() == student_mis.lower():
                if str(student.mis) == str(student_mis):
                    attendance = student.attendance
                    extracurricular_marks = student.extracurricular_marks
                    academic_marks = student.academic_marks

                    # Plot the graph
                    labels = ["Attendance", "Extracurricular Marks", "Academic Marks"]
                    values = [attendance, extracurricular_marks, academic_marks]

                    # Create a figure and axes
                    fig, ax = plt.subplots()

                    # Plot the bar chart
                    ax.bar(labels, values)

                    # Set labels and title
                    ax.set_xlabel("Category")
                    ax.set_ylabel("Score")
                    ax.set_title(f"Scores for {student_mis}")

                    # Save the figure to a BytesIO object
                    image_stream = io.BytesIO()
                    plt.savefig(image_stream, format='png')
                    image_stream.seek(0)

                    # Generate a base64 encoded string from the image stream
                    encoded_image = base64.b64encode(image_stream.getvalue()).decode('utf-8')

                    # Close the figure
                    plt.close()

                    return render_template('index.html', graph_image=encoded_image)

            return render_template('index.html', error_message="Student not found!")

        elif choice == "3":
            branch = request.form['branch']

            # Get career options based on the selected branch
            if branch == "Computer Engineering":
                career_options = [
                    {"name": "Software Developer"},
                    {"name": "Data Scientist"},
                    {"name": "Computer Network Architect"},
                    {"name": "Database Administrator"},
                    {"name": "Blockchain Developer/Engineer"},
                    {"name": "Machine Learning Engineer"},
                    {"name": "System Administrator"}
                    
                ]
            elif branch == "E&TC Engineering":
                career_options = [
                    {"name": "Design Engineer"},
                    {"name": "ASCI Engineer"},
                    {"name": "Telecom Engineer"},
                    {"name": "Network Planning Engineer"},
                    {"name": "Embedded Engineer"}
                ]
            elif branch == "Electrical Engineering":
                career_options = [
                    {"name": "Power Engineer"},
                    {"name": "Control Systems Engineer"},
                    {"name": "Control Systems Engineer"},
                    {"name": "Control Systems Engineer"},
                    {"name": "Electrical Design Engineer"}
                ]
            elif branch == "Mechanical Engineering":
                career_options = [
                    {"name": "CAD technician"},
                    {"name": "Automotive Engineer"},
                    {"name": "Maintenance engineer"},
                    {"name": "Aerospace engineer"}
                ]
            elif branch == "Production Engineering":
                career_options = [
                    {"name": "Field engineer"},
                    {"name": "Project engineer"},
                    {"name": "Operations analyst"},
                    {"name": "Industrial engineer"}
                ]
            elif branch == "Metallurgy Engineering":
                career_options = [
                    {"name": "Mechanical Engineer"},
                    {"name": "Automotive Engineer"},
                    {"name": "Manufacturing Engineer"}
                ]
            else:
                career_options = []

            return render_template('index.html', career_options=career_options)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001)


