# 🎓 Student Grade Management System

> **End-to-End Data Analytics & Management Project** | Python · pandas · MySQL · Power BI · Gamma  
> Prepared by **Rahul Pandit** | MS Information Systems | Texas Tech University, Rawls College of Business | 2026

---

## 📌 Overview

The **Student Grade Management System** is a complete, Python-based academic data management solution designed for instructors managing multi-subject grade data. The system covers the full analytics lifecycle — from loading and cleaning raw student data, running SQL queries for insights, building an interactive Power BI dashboard, generating a professional report, and presenting results via a Gamma-powered presentation.

**Key capabilities at a glance:**
- Load student datasets in Python and perform Exploratory Data Analysis (EDA)
- Clean and normalize raw grade data (handle missing values, outliers, type mismatches)
- Run SQL queries on PostgreSQL / MySQL / SQL Server for grade analytics
- Build an interactive Power BI dashboard with KPI cards, charts, and filters
- Auto-generate a structured grade report (PDF / Word)
- Create a recruiter-ready presentation using Gamma AI

---

## 📂 Dataset

| Property | Detail |
|---|---|
| **Domain** | Academic / Education |
| **Records** | 100+ student records across multiple subjects |
| **Subjects** | ISQS 6335 · Business Scripting · Machine Learning (multi-subject support) |
| **Date Range** | Academic Year 2025–2026 |
| **Format** | CSV (raw input) · grade_summary_[Subject].csv (processed output) |

### Key Fields

| Field | Type | Description |
|---|---|---|
| `Student_ID` | Integer | Unique numeric student identifier (Roll Number) |
| `Student_Name` | String | Full name of the student |
| `Subject` | String | Subject / course name |
| `Midterm_1` | Float | First midterm exam score (0–100) |
| `Midterm_2` | Float | Second midterm exam score (0–100) |
| `Final_Exam` | Float | Final examination score (0–100) |
| `Missing_Classes` | Integer | Number of classes the student was absent from |
| `AttendanceScore` | Float | Calculated score based on absence vs. threshold |
| `TotalScore` | Float | Weighted composite score (Midterm 1: 30% · Midterm 2: 30% · Final: 40% · Attendance) |
| `LetterGrade` | String | Final letter grade: A / B / C / D / F |

---

## 🛠️ Tools & Technologies

| Tool / Technology | Purpose |
|---|---|
| **Python 3.x** | Core scripting, data loading, EDA, grade calculations |
| **pandas** | DataFrame operations, statistical summaries, data cleaning |
| **NumPy** | Array-level computations, statistical calculations |
| **matplotlib** | Score distribution histograms, letter grade pie charts |
| **PostgreSQL / MySQL / SQL Server** | SQL queries for grade analytics and aggregation |
| **Power BI Desktop** | Interactive KPI dashboard with year/subject filters |
| **Gamma** | AI-powered professional presentation from report content |
| **CSV** | Input data format and final export format |

---

## 🔄 Steps / Workflow

### Step 1 — Load Dataset in Python

```python
import pandas as pd

# Load raw student scores from CSV
df = pd.read_csv("student_scores.csv")
print(df.shape)
print(df.head())
```

- Loaded raw CSV containing student IDs, names, exam scores, and attendance records
- Confirmed row count, column types, and initial data structure
- Identified subjects present in the dataset for multi-subject processing

---

### Step 2 — Exploratory Data Analysis (EDA)

```python
# Basic EDA
print(df.describe())
print(df.isnull().sum())
print(df['LetterGrade'].value_counts())
```

- Computed descriptive statistics: mean, median, std deviation, min/max per exam component
- Checked for null values, duplicate student IDs, and out-of-range scores
- Analyzed score distributions and grade frequency across subjects
- Identified high-performing and low-performing student segments

---

### Step 3 — Data Cleaning

```python
# Fill missing scores, fix data types, remove duplicates
df['Midterm_1'].fillna(df['Midterm_1'].median(), inplace=True)
df['Student_ID'] = df['Student_ID'].astype(int)
df.drop_duplicates(subset='Student_ID', inplace=True)
```

- Handled missing exam scores using subject-level median imputation
- Corrected data type mismatches (scores stored as strings → float)
- Standardized student name formatting (strip whitespace, title case)
- Flagged and reviewed outlier scores below 30 or above 100

---

### Step 4 — Calculated Fields (Python)

```python
# Weighted Total Score
def calculate_total(row, threshold, total_classes):
    weighted = (row['Midterm_1'] * 0.30 +
                row['Midterm_2'] * 0.30 +
                row['Final_Exam'] * 0.40)
    excess = max(0, row['Missing_Classes'] - threshold)
    penalty = (excess / total_classes) * 100
    return max(0, weighted - penalty)

# Letter Grade Assignment
def assign_grade(score):
    if score >= 90: return 'A'
    elif score >= 80: return 'B'
    elif score >= 70: return 'C'
    elif score >= 60: return 'D'
    else: return 'F'

df['TotalScore'] = df.apply(lambda r: calculate_total(r, 6, 32), axis=1)
df['LetterGrade'] = df['TotalScore'].apply(assign_grade)
```

---

### Step 5 — SQL Queries (PostgreSQL / MySQL / SQL Server)

```sql
-- Average TotalScore per Subject
SELECT Subject, ROUND(AVG(TotalScore), 2) AS AvgScore
FROM grade_summary
GROUP BY Subject
ORDER BY AvgScore DESC;

-- Top 10 Students by TotalScore
SELECT Student_ID, Student_Name, Subject, TotalScore, LetterGrade
FROM grade_summary
ORDER BY TotalScore DESC
LIMIT 10;

-- Grade Distribution per Subject
SELECT Subject, LetterGrade, COUNT(*) AS StudentCount,
       ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Subject), 1) AS Percentage
FROM grade_summary
GROUP BY Subject, LetterGrade
ORDER BY Subject, LetterGrade;

-- Students enrolled in Multiple Subjects
SELECT Student_ID, Student_Name, COUNT(DISTINCT Subject) AS SubjectCount,
       ROUND(AVG(TotalScore), 2) AS CrossSubjectAvg
FROM grade_summary
GROUP BY Student_ID, Student_Name
HAVING COUNT(DISTINCT Subject) > 1
ORDER BY CrossSubjectAvg DESC;

-- Students at Risk (TotalScore < 70)
SELECT Student_ID, Student_Name, Subject, TotalScore, LetterGrade
FROM grade_summary
WHERE TotalScore < 70
ORDER BY TotalScore ASC;
```

---

### Step 6 — Visualizations (Python — matplotlib)

```python
import matplotlib.pyplot as plt

# Score Distribution Histogram
plt.figure(figsize=(10, 5))
for subject, group in df.groupby('Subject'):
    plt.hist(group['TotalScore'], bins=10, alpha=0.7, label=subject)
plt.xlabel('Total Score')
plt.ylabel('Number of Students')
plt.title('Score Distribution by Subject')
plt.legend()
plt.tight_layout()
plt.savefig('score_distribution.png')
plt.show()

# Letter Grade Pie Chart
grade_counts = df['LetterGrade'].value_counts()
plt.figure(figsize=(7, 7))
plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%',
        colors=['#2563EB','#10B981','#F59E0B','#F97316','#EF4444'])
plt.title('Letter Grade Distribution')
plt.savefig('grade_distribution.png')
plt.show()
```

---

### Step 7 — Power BI Dashboard

- Connected Power BI Desktop to the processed `grade_summary.csv`
- Built **6 interactive visuals**:
  - 📊 KPI Cards — Total Students · Class Average · Highest Score · Lowest Score
  - 📈 TotalScore Distribution (Histogram / Bar Chart)
  - 🥧 Letter Grade Distribution Pie Chart
  - 📋 Student-Level Table with search and filter
  - 🔢 Subject Comparison (Avg Score by Subject)
  - ⚠️ At-Risk Students Panel (TotalScore < 70)
- Added **Subject** and **Grade** slicers for dynamic filtering
- Applied a clean, professional dark-and-blue color theme
- Exported `.pbix` file for sharing and `.pdf` for static distribution

---

### Step 8 — Report Generation

- Exported processed grade data to `grade_summary_[Subject].csv` per subject
- Generated a structured **User Manual / Project Report** (PDF) containing:
  - System overview and workflow diagram
  - Use case table
  - Step-by-step instructions with terminal output examples
  - Summary statistics for each subject
  - Major functions and data structures documentation
- Report prepared in Python (ReportLab) with professional header/footer

---

### Step 9 — Presentation (Gamma AI)

- Created a **professional slide deck** using [Gamma](https://gamma.app) based on the project report
- Slides include: project overview · dataset summary · EDA findings · SQL insights ·
  Power BI dashboard screenshots · key results · conclusion
- Presentation exported as PDF and shareable Gamma link

---

## 📊 Power BI Dashboard

**Dashboard Title:** `Student Grade Analysis`

### Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  🎓  Student Grade Analysis Dashboard                            │
├────────────┬────────────┬────────────┬───────────────────────────┤
│ Students   │ Avg Score  │ Top Score  │ At-Risk Students          │
│  101       │  87.23     │ 100.00     │  5                        │
├────────────┴────────────┴────────────┤                           │
│ Score Distribution (Histogram)       │ Grade Distribution (Pie)  │
│                                      │                           │
├──────────────────────────────────────┴───────────────────────────┤
│ Student Performance Table                                         │
│ [Subject Slicer]  [Grade Slicer]  [Search by Student ID]         │
└──────────────────────────────────────────────────────────────────┘
```

### Sample Metrics

| KPI | Value |
|---|---|
| Total Students | 101 |
| Class Average (Combined) | 87.23 |
| Highest Score | 100.00 (Machine Learning) |
| Lowest Score | 66.50 (Business Scripting) |
| Students with Grade A | 40 (39.6%) |
| Students with Grade B | 45 (44.6%) |
| At-Risk (Score < 70) | 5 (5.0%) |
| Multi-Subject Students | 10 |

---

## 📈 Key Results & Insights

### 🏆 Academic Performance
- **87.23** combined average TotalScore across all subjects and students
- **84%** of students earned an A or B grade — strong overall class performance
- Machine Learning students averaged **91.75** vs. Business Scripting at **82.63** — a significant gap suggesting differences in difficulty or prior preparation

### ⚠️ At-Risk Students
- **5 students** scored below 70 (grade D or F) — identified for early intervention
- The lowest scoring student in Business Scripting scored **66.50** — below the C threshold
- All at-risk students showed elevated absences above the 6-class threshold

### 📅 Attendance Impact
- Attendance penalties disproportionately affected lower-quartile students
- Students with 0 missed classes averaged **91.2** vs. **78.4** for students exceeding the threshold
- The attendance scoring mechanism successfully differentiated engagement levels

### 🎯 Cross-Subject Insights
- **10 students** were enrolled in both subjects — their cross-subject averages ranged from **82.5 to 96.4**
- Strong positive correlation between performance in Business Scripting and Machine Learning among multi-enrolled students

---

## 📁 Project File Structure

```
student-grade-management/
│
├── README.md                              ← This file
│
├── data/
│   ├── ISQS_6335_student_scores.csv       ← Raw input data (Business Scripting)
│   ├── ML_student_scores.csv              ← Raw input data (Machine Learning)
│   ├── grade_summary_Business_Scripting.csv  ← Processed output
│   └── grade_summary_Machine_Learning.csv    ← Processed output
│
├── notebooks/
│   └── grade_analysis_EDA.ipynb           ← Python EDA + cleaning notebook
│
├── sql/
│   ├── create_tables.sql                  ← Schema setup
│   ├── grade_analytics.sql                ← All SQL query scripts
│   └── at_risk_students.sql               ← At-risk identification queries
│
├── visuals/
│   ├── score_distribution.png             ← Histogram exports
│   ├── grade_distribution_pie.png         ← Pie chart exports
│   └── dashboard_screenshot.png           ← Power BI screenshot
│
├── dashboard/
│   └── Student_Grade_Dashboard.pbix       ← Power BI workbook
│
├── report/
│   └── Student_Grade_Management_System_Manual.pdf  ← Full project report
│
└── presentation/
    └── Grade_Management_Gamma_Slides.pdf  ← Exported Gamma presentation
```

---

## ▶️ How to Run

### Prerequisites

```bash
pip install pandas numpy matplotlib
```

### Step 1 — Run the Python Grade System

```bash
python grade_management_system.py
```

Follow the on-screen menu:
```
1. Import existing processed grade summary
2. Start fresh and load/process new subject scores
3. Exit
```

### Step 2 — Load Data via CSV

```
Enter CSV filename: ISQS_6335_student_scores.csv
Enter subject name: Business Scripting
Enter total number of classes: 32
Enter allowed absences before penalty: 6
```

### Step 3 — View Analytics & Export

```
Main Menu:
3 → View summary statistics
4 → Plot score distribution histogram
5 → Plot letter grade pie chart
6 → Search student by Roll Number
7 → Export grade summaries to CSV
```

### Step 4 — Open in Power BI

```
1. Open Power BI Desktop
2. Get Data → Text/CSV → select grade_summary_[Subject].csv
3. Load all processed files
4. Open Student_Grade_Dashboard.pbix
   OR build from scratch using the exported CSVs
```

### Step 5 — Run SQL Queries

```sql
-- In PostgreSQL / MySQL / SQL Server:
-- 1. Create the grade_summary table
-- 2. Import the processed CSV
-- 3. Run queries from sql/grade_analytics.sql
```

---

## 🧠 Skills Demonstrated

| Category | Skills |
|---|---|
| **Python Programming** | Data loading, EDA, data cleaning, weighted score calculation, letter grade assignment, menu-driven CLI |
| **Data Cleaning** | Null handling, type correction, duplicate removal, outlier detection, string normalization |
| **SQL Analytics** | Aggregation, GROUP BY, HAVING, window functions (PARTITION BY), subqueries, multi-subject analysis |
| **Data Visualization** | Histograms, pie charts, multi-subject overlays using matplotlib |
| **Power BI** | Data import, KPI cards, interactive filters/slicers, bar/pie/table visuals, .pbix export |
| **Report Writing** | Structured PDF report (ReportLab) with TOC, tables, code blocks, visual callouts |
| **Presentation** | Gamma AI presentation with structured slides, visuals, and key insights |
| **Statistical Analysis** | Mean, median, std dev, IQR, percentile ranks, best/worst performer identification |

---

## 👤 Author

**Rahul Pandit**  
MS Information Systems | Texas Tech University, Rawls College of Business  
Course: ISQS 6335  
📅 2026

---

## 📄 License

This project was developed for academic purposes as part of the MS Information Systems program at Texas Tech University. Dataset and outputs are for educational and portfolio demonstration use only.

---

*⭐ If this project was helpful, consider starring the repository on GitHub!*
