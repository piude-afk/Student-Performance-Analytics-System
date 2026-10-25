import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# File names
DEPARTMENTS_FILE = "departments.csv"
STUDENTS_FILE = "students.csv"
SUBJECTS_FILE = "subjects.csv"
MARKS_FILE = "marks.csv"


# --------------------------------------------------
# 1. LOAD CSV FILES
# --------------------------------------------------

def load_data():
    departments = pd.read_csv(DEPARTMENTS_FILE)
    students = pd.read_csv(STUDENTS_FILE)
    subjects = pd.read_csv(SUBJECTS_FILE)
    marks = pd.read_csv(MARKS_FILE)

    required_columns = {
        "departments": {"department_id", "department_name"},
        "students": {"student_id", "student_name", "department_id"},
        "subjects": {"subject_id", "subject_name"},
        "marks": {"student_id", "subject_id", "marks"}
    }

    tables = {
        "departments": departments,
        "students": students,
        "subjects": subjects,
        "marks": marks
    }

    for name, required in required_columns.items():
        missing = required - set(tables[name].columns)
        if missing:
            raise ValueError(
                f"{name}.csv is missing columns: {missing}"
            )

    # Convert IDs to a consistent type
    for column in ["student_id", "subject_id"]:
        marks[column] = pd.to_numeric(
            marks[column], errors="raise"
        ).astype(int)

    students["student_id"] = pd.to_numeric(
        students["student_id"], errors="raise"
    ).astype(int)

    subjects["subject_id"] = pd.to_numeric(
        subjects["subject_id"], errors="raise"
    ).astype(int)

    departments["department_id"] = pd.to_numeric(
        departments["department_id"], errors="raise"
    ).astype(int)

    students["department_id"] = pd.to_numeric(
        students["department_id"], errors="raise"
    ).astype(int)

    marks["marks"] = pd.to_numeric(
        marks["marks"], errors="coerce"
    )

    return departments, students, subjects, marks


# --------------------------------------------------
# 2. SAVE MARKS
# --------------------------------------------------

def save_marks(marks):
    marks.to_csv(MARKS_FILE, index=False)
    print("Marks saved successfully!")


# --------------------------------------------------
# 3. INPUT VALIDATION
# --------------------------------------------------

def get_number(message):
    while True:
        value = input(message).strip()

        if not value.isdigit():
            print("Please enter numbers only.")
            continue

        return int(value)


def get_student_id(students):
    while True:
        student_id = get_number("Enter student ID: ")

        if student_id in students["student_id"].values:
            return student_id

        print("Student ID does not exist. Try again.")


def get_subject_id(subjects):
    while True:
        subject_id = get_number("Enter subject ID: ")

        if subject_id in subjects["subject_id"].values:
            return subject_id

        print("Subject ID does not exist. Try again.")


def get_marks():
    while True:
        value = input("Enter marks (0-100): ").strip()

        try:
            mark = float(value)

            if not np.isfinite(mark):
                print("Enter a valid number.")
            elif 0 <= mark <= 100:
                return mark
            else:
                print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# --------------------------------------------------
# 4. PREPARE STUDENT REPORT
# --------------------------------------------------

def create_report(departments, students, subjects, marks):
    data = marks.merge(students, on="student_id")
    data = data.merge(departments, on="department_id")
    data = data.merge(subjects, on="subject_id")

    # One row per student and one column per subject
    report = data.pivot_table(
        index=[
            "student_id",
            "student_name",
            "department_name"
        ],
        columns="subject_name",
        values="marks",
        aggfunc="mean"
    ).reset_index()

    subject_columns = [
        col for col in report.columns
        if col not in [
            "student_id", "student_name", "department_name"
        ]
    ]

    # Calculate total and percentage
    report["total"] = report[subject_columns].sum(
        axis=1, min_count=len(subject_columns)
    )

    report["percentage"] = (
        report["total"] / (len(subject_columns) * 100)
    ) * 100

    # Grade calculation
    conditions = [
        report["percentage"] >= 90,
        report["percentage"] >= 80,
        report["percentage"] >= 70,
        report["percentage"] >= 60,
        report["percentage"] >= 40
    ]

    report["grade"] = np.select(
        conditions,
        ["A+", "A", "B", "C", "D"],
        default="F"
    )

    # Pass only if every subject has marks >= 40
    report["status"] = np.where(
        report[subject_columns].ge(40).all(axis=1)
        & report[subject_columns].notna().all(axis=1),
        "PASS",
        "FAIL"
    )

    report["rank"] = report["total"].rank(
        ascending=False, method="min"
    ).astype("Int64")

    return report, subject_columns, data


# --------------------------------------------------
# 5. ADD OR UPDATE MARKS
# --------------------------------------------------

def add_update_marks(students, subjects, marks):
    student_id = get_student_id(students)
    subject_id = get_subject_id(subjects)
    mark = get_marks()

    # Check whether a record already exists
    condition = (
        (marks["student_id"] == student_id)
        & (marks["subject_id"] == subject_id)
    )

    if condition.any():
        marks.loc[condition, "marks"] = mark
        print("Existing marks updated successfully!")
    else:
        new_row = pd.DataFrame([{
            "student_id": student_id,
            "subject_id": subject_id,
            "marks": mark
        }])

        marks = pd.concat(
            [marks, new_row], ignore_index=True
        )
        print("New marks added successfully!")

    save_marks(marks)
    return marks


# --------------------------------------------------
# 6. VIEW STUDENT REPORT
# --------------------------------------------------

def view_student_report(report):
    student_id = get_number("Enter student ID: ")

    result = report[report["student_id"] == student_id]

    if result.empty:
        print("Student not found.")
        return

    display_columns = [
        col for col in result.columns
        if col not in ["student_id"]
    ]

    print("\nSTUDENT REPORT")
    print(result[display_columns].to_string(index=False))


# --------------------------------------------------
# 7. SHOW TOPPER LIST
# --------------------------------------------------

def show_toppers(report):
    toppers = report.sort_values(
        ["total", "student_name"],
        ascending=[False, True]
    ).head(5)

    print("\nTOP 5 STUDENTS")
    print(
        toppers[
            ["student_id", "student_name",
             "total", "percentage", "grade", "rank"]
        ].to_string(index=False)
    )


# --------------------------------------------------
# 8. SHOW ANALYSIS
# --------------------------------------------------

def show_analysis(report, subject_columns, data):
    print("\nAVERAGE MARKS PER SUBJECT")
    print(data.groupby("subject_name")["marks"].mean())

    print("\nMEAN, MEDIAN AND STANDARD DEVIATION")
    for subject, group in data.groupby("subject_name"):
        values = group["marks"].dropna().to_numpy()

        if len(values) > 0:
            print(f"\n{subject}")
            print("Mean:", np.mean(values))
            print("Median:", np.median(values))
            print("Standard deviation:", np.std(values))

    print("\nPASS/FAIL COUNT")
    print(report["status"].value_counts())

    print("\nDEPARTMENT-WISE AVERAGE MARKS")
    print(
        data.groupby("department_name")["marks"]
        .mean().round(2)
    )

    print("\nTOP 5 STUDENTS")
    show_toppers(report)


# --------------------------------------------------
# 9. SHOW AND SAVE CHARTS
# --------------------------------------------------

def show_charts(report, subject_columns, data):
    # Bar chart
    subject_avg = data.groupby("subject_name")["marks"].mean()

    plt.figure(figsize=(9, 5))
    bars = plt.bar(subject_avg.index, subject_avg.values)

    for bar in bars:
        height = bar.get_height()
        if pd.notna(height):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                height,
                f"{height:.1f}",
                ha="center",
                va="bottom"
            )

    plt.title("Average Marks per Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("average_marks_per_subject.png", dpi=300)
    plt.show()
    plt.close()

    # Pie chart
    grade_counts = report["grade"].value_counts().sort_index()

    plt.figure(figsize=(7, 7))
    plt.pie(
        grade_counts.values,
        labels=grade_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Student Distribution")
    plt.tight_layout()
    plt.savefig("grade_distribution.png", dpi=300)
    plt.show()
    plt.close()

    # Histogram
    all_marks = data["marks"].dropna()

    plt.figure(figsize=(9, 5))
    plt.hist(all_marks, bins=10, edgecolor="black")
    plt.axvline(
        40, linestyle="--",
        label="Pass Mark = 40"
    )
    plt.title("Distribution of Marks")
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.savefig("marks_distribution_histogram.png", dpi=300)
    plt.show()
    plt.close()

    # Box plot of student percentage by department
    departments = report["department_name"].dropna().unique()

    percentage_data = [
        report.loc[
            report["department_name"] == department,
            "percentage"
        ].dropna()
        for department in departments
    ]

    plt.figure(figsize=(9, 5))
    plt.boxplot(percentage_data, labels=departments)
    plt.title("Student Percentage by Department")
    plt.xlabel("Department")
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("percentage_by_department_boxplot.png", dpi=300)
    plt.show()
    plt.close()

    print("All four charts have been saved as PNG files.")


# --------------------------------------------------
# 10. EXPORT REPORT TO CSV
# --------------------------------------------------

def export_report(report):
    filename = input(
        "Enter report filename (press Enter for student_report.csv): "
    ).strip()

    if not filename:
        filename = "student_report.csv"

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    report.to_csv(filename, index=False)
    print("Report exported to", filename)


# --------------------------------------------------
# 11. MAIN MENU
# --------------------------------------------------

def main():
    try:
        departments, students, subjects, marks = load_data()

    except FileNotFoundError as error:
        print("Error: CSV file not found:", error.filename)
        print("Keep all four CSV files beside main.py.")
        return

    except (ValueError, KeyError) as error:
        print("Error in CSV data:", error)
        return

    while True:
        print("\n========== STUDENT MARKS SYSTEM ==========")
        print("1. Add/update marks")
        print("2. View student report")
        print("3. Show topper list")
        print("4. Show analysis")
        print("5. Show charts")
        print("6. Export report to CSV")
        print("0. Exit")
        print("==========================================")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                marks = add_update_marks(
                    students, subjects, marks
                )

            elif choice == "2":
                report, _, _ = create_report(
                    departments, students, subjects, marks
                )
                view_student_report(report)

            elif choice == "3":
                report, _, _ = create_report(
                    departments, students, subjects, marks
                )
                show_toppers(report)

            elif choice == "4":
                report, subject_columns, data = create_report(
                    departments, students, subjects, marks
                )
                show_analysis(report, subject_columns, data)

            elif choice == "5":
                report, subject_columns, data = create_report(
                    departments, students, subjects, marks
                )
                show_charts(report, subject_columns, data)

            elif choice == "6":
                report, _, _ = create_report(
                    departments, students, subjects, marks
                )
                export_report(report)

            elif choice == "0":
                print("Program closed. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 0 to 6.")

        except FileNotFoundError as error:
            print("File not found:", error.filename)

        except PermissionError:
            print("Permission denied. Close the CSV file in Excel and try again.")

        except (ValueError, KeyError) as error:
            print("Could not process the data:", error)

        except Exception as error:
            print("An unexpected error occurred:", error)


if __name__ == "__main__":
    main()
