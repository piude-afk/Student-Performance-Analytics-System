# Student Performance Analytics System

## Project Overview

The **Student Performance Analytics System** is a mini-project developed as part of the B.Tech Puja Vacation Project Assignment.

The project uses MySQL to store and manage student marks and Python libraries to analyse student performance, calculate grades, generate reports, and visualize results through charts.

MySQL and Python work separately in this project. Data is transferred from MySQL to Python using CSV files.

## Objectives

- Design a normalized database using MySQL.
- Store student, department, subject, and marks information.
- Perform SQL JOIN queries and create stored functions.
- Load and combine CSV files using Pandas.
- Analyse marks using Pandas and NumPy.
- Visualize results using Matplotlib.
- Build a menu-driven Python program with input validation and error handling.

## Technologies Used

- **Database:** MySQL 8.0.16 or later
- **Programming Language:** Python 3.9 or later
- **Libraries:** Pandas, NumPy, Matplotlib
- **Development Environment:** JupyterLab
- **Data Exchange:** CSV files

## Project Structure

```text
Student_Performance_Analytics/
│
├── project.sql
├── departments.csv
├── students.csv
├── subjects.csv
├── marks.csv
├── main.py
├── student_report.csv
├── charts/
│   ├── average_marks_per_subject.png
│   ├── grade_distribution.png
│   ├── marks_distribution_histogram.png
│   └── percentage_by_department_boxplot.png
├── Report.pdf
└── README.md
```

## Database Design

The MySQL database is named `student_analytics` and contains four tables:

1. **departments** — stores department information.
2. **students** — stores student details and department information.
3. **subjects** — stores subject information.
4. **marks** — stores marks obtained by students in different subjects.

The database uses primary keys, foreign keys, unique constraints, NOT NULL constraints, CHECK constraints, and default values where appropriate.

## Features

- Load and merge data from four CSV files.
- Clean duplicate records and handle missing marks.
- Calculate subject-wise mean, median, and standard deviation.
- Generate student totals, percentages, grades, PASS/FAIL status, and ranks.
- Display the top five students.
- Calculate pass/fail counts and department-wise average marks.
- Generate charts using Matplotlib.
- Add or update student marks.
- View individual student reports.
- Export student reports to CSV.

## Installation and Setup

### 1. Install the required Python libraries

Open a terminal in JupyterLab and run:

```bash
pip install pandas numpy matplotlib
```

### 2. Set up the MySQL database

1. Open MySQL Workbench.
2. Open `project.sql`.
3. Execute the SQL script.
4. Confirm that the database and tables have been created successfully.

### 3. Export the CSV files

Export the four MySQL tables into these files:

- `departments.csv`
- `students.csv`
- `subjects.csv`
- `marks.csv`

Place all four files in the same project directory as `main.py`.

### 4. Run the Python program

Open a terminal in the project directory and execute:

```bash
python main.py
```

Alternatively, in a Jupyter Notebook cell, use:

```python
%run main.py
```

Follow the menu displayed by the program.

## Application Menu

The program provides the following options:

1. Add or update marks
2. View student report
3. Show topper list
4. Show analysis
5. Show charts
6. Export report to CSV
0. Exit

## Charts and Analysis

The project generates four charts:

1. **Average Marks per Subject:** compares average marks across subjects.
2. **Grade Distribution:** shows the distribution of student grades.
3. **Marks Distribution Histogram:** displays the distribution of marks and the pass mark of 40.
4. **Percentage by Department:** compares student percentages across departments.

The charts are saved as PNG files in the `charts/` directory.

## Project Workflow

1. Create the database and tables in MySQL.
2. Insert sample data and execute SQL queries.
3. Export the database tables as CSV files.
4. Load and merge the CSV files using Pandas.
5. Clean and analyse the data using Pandas and NumPy.
6. Generate visualizations using Matplotlib.
7. Run the menu-driven Python program.
8. Export the student report and prepare the final project report.

## Learning Outcomes

Through this project, I practised relational database design, SQL queries, data cleaning, data analysis, data visualization, Python functions, input validation, and CSV file handling.

## Future Improvements

- Add attendance analysis and examine its relationship with marks.
- Identify students who may be at risk academically.
- Add semester-wise performance comparisons.
- Develop a graphical user interface for easier use.

## Author

**Name:** Piu De
**Project:** Student Performance Analytics System

