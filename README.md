
# Smart Study Planner & Performance Tracker

A menu-driven Python application that helps college students organize academic tasks, rank them by priority, plan study time, and track progress.

**Bennett University | School of Computer Science Engineering and Technology**
**Course:** Computational Thinking and Programming (2026CSAE100) | **Batch/Section:** B35 / S18

## Description

Students often juggle several subjects, assignments, tests and study targets, and it is hard to decide what to study first. This project turns task details (subject, deadline, difficulty, estimated hours) into a ranked, time-bounded study plan and a short performance summary.

### Features
- **Task manager:** add and view academic tasks
- **Input validation:** checks text, date format (`YYYY-MM-DD`) and numeric ranges
- **Priority engine:** weighted scoring from deadline, difficulty and remaining work
- **Schedule generator:** allocates your available study hours to the highest-priority pending tasks
- **Progress tracker:** update the completion percentage of any task
- **Performance summary:** total, completed and pending tasks, average progress, planned and remaining hours, and the highest-priority task
- **Persistent storage:** all data is saved to a local JSON file

### Priority formula
```
Priority = 0.40 × Deadline Score + 0.30 × Difficulty Score + 0.30 × Remaining Work Score
```
- **Deadline score:** starts at 100 and drops 10 points per day remaining (bounded 0–100)
- **Difficulty score:** difficulty (1–5) × 20
- **Remaining work score:** 100 − progress %

A higher score means the task needs attention sooner.

## Technologies Used

- **Language:** Python 3
- **Standard-library modules:** `json`, `datetime`, `pathlib`
- **Data storage:** JSON file (`study_data.json`)
- **Concepts applied:** classes and objects (`StudyTask`, `StudyPlanner`), functions, lists and dictionaries, conditionals and loops, file handling, exception handling

No external packages or internet connection are required.

## How to Run

1. **Install Python 3** (3.8 or later) from [python.org](https://www.python.org/downloads/). Check with:
   ```
   python --version
   ```
2. **Download the project.** Click **Code → Download ZIP** on this repository and extract it, or clone it:
   ```
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
   cd YOUR-REPO
   ```
3. **Run the program** from the project folder:
   ```
   python smart_study_planner.py
   ```
   (On some systems use `python3 smart_study_planner.py`.)
4. **Use the menu:**
   ```
   1. Add task
   2. View tasks
   3. Generate study schedule
   4. Update progress
   5. Performance summary
   6. Save and exit
   ```
   Enter a number from 1 to 6. Choose **6** to save and exit.

### Example workflow
Add a task → view the ranked tasks → generate a schedule for today's available hours → update progress after studying → check the performance summary.

## Project Structure

```
├── smart_study_planner.py   # Main program source code
├── study_data.json          # Task data (sample data, updated by the app)
└── README.md                # Project documentation
```

## Team

| Name | Roll No. | Contribution |
|---|---|---|
| Saksham Jain | S26CSEU1219 | Coordination, core logic, priority algorithm, integration, input/menu, validation, data structures |
| Nameh Malik | S26CSEU1228 | Flowchart, screenshots, presentation, review, schedule generation, testing, debugging |
| Mohin Gupta | S26CSEU1235 | File handling, performance summary, documentation |

## Limitations and Future Improvements

- Currently a local command-line app with no cross-device sync
- Priority weights are rule-based and fixed
- Study-hour estimates are entered manually

Planned: Tkinter graphical interface, weekly progress charts, recurring tasks, and CSV/PDF export.
