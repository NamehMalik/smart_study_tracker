"""
SMART STUDY PLANNER & PERFORMANCE TRACKER
Bennett University | Computational Thinking and Programming
Course: 2026CSAE100

Run: python smart_study_planner.py
Data is stored locally in study_data.json.
"""

import json
from datetime import date, datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("study_data.json")


class StudyTask:
    """Represents one academic task and its current progress."""

    def __init__(self, subject, task_name, deadline, difficulty,
                 target_score, estimated_hours, progress=0):
        self.subject = subject.strip()
        self.task_name = task_name.strip()
        self.deadline = deadline
        self.difficulty = int(difficulty)
        self.target_score = float(target_score)
        self.estimated_hours = float(estimated_hours)
        self.progress = float(progress)

    def remaining_hours(self):
        return self.estimated_hours * (100 - self.progress) / 100

    def is_complete(self):
        return self.progress >= 100

    def days_left(self):
        due = datetime.strptime(self.deadline, "%Y-%m-%d").date()
        return (due - date.today()).days

    def priority_score(self):
        # Deadline urgency, difficulty and remaining work are normalized to 0–100.
        deadline_score = max(0, min(100, 100 - max(self.days_left(), 0) * 10))
        difficulty_score = self.difficulty * 20
        remaining_work_score = 100 - self.progress
        return (0.40 * deadline_score
                + 0.30 * difficulty_score
                + 0.30 * remaining_work_score)

    def to_dict(self):
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class StudyPlanner:
    """Coordinates task management, scheduling, persistence and reporting."""

    def __init__(self):
        self.tasks = []
        self.load_data()

    def load_data(self):
        try:
            if DATA_FILE.exists():
                with DATA_FILE.open("r", encoding="utf-8") as file:
                    records = json.load(file)
                self.tasks = [StudyTask.from_dict(item) for item in records]
        except (json.JSONDecodeError, TypeError, KeyError, ValueError) as error:
            print("Saved data could not be read:", error)
            self.tasks = []

    def save_data(self):
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks],
                      file, indent=4)
        print("Data saved successfully.")

    def add_task(self):
        try:
            subject = input("Subject: ").strip()
            task_name = input("Task/topic: ").strip()
            if not subject or not task_name:
                raise ValueError("Subject and task name cannot be empty.")

            deadline = input("Deadline (YYYY-MM-DD): ").strip()
            datetime.strptime(deadline, "%Y-%m-%d")

            difficulty = int(input("Difficulty (1-5): "))
            if not 1 <= difficulty <= 5:
                raise ValueError("Difficulty must be between 1 and 5.")

            target = float(input("Target score (0-100): "))
            hours = float(input("Estimated total study hours: "))
            if not 0 <= target <= 100 or hours <= 0:
                raise ValueError("Target must be 0-100 and hours must be positive.")

            task = StudyTask(subject, task_name, deadline, difficulty,
                             target, hours)
            self.tasks.append(task)
            self.save_data()
            print("Task added.")
        except ValueError as error:
            print("Invalid input:", error)

    def show_tasks(self):
        if not self.tasks:
            print("No tasks found. Add a task first.")
            return
        print("\n{:<4} {:<18} {:<22} {:>8} {:>9}".format(
            "No.", "Subject", "Task", "Progress", "Priority"))
        print("-" * 67)
        for index, task in enumerate(self.tasks, start=1):
            priority = task.priority_score()
            level = "HIGH" if priority >= 65 else "MEDIUM" if priority >= 40 else "LOW"
            print("{:<4} {:<18} {:<22} {:>7.1f}% {:>8.1f}".format(
                index, task.subject[:18], task.task_name[:22],
                task.progress, priority), level)

    def generate_schedule(self):
        pending = [task for task in self.tasks if not task.is_complete()]
        if not pending:
            print("There are no pending tasks.")
            return

        try:
            available = float(input("Available study hours today: "))
            if available < 0:
                raise ValueError("Available hours cannot be negative.")
        except ValueError as error:
            print("Invalid input:", error)
            return

        if available == 0:
            print("No time allocated. Enter more than zero hours to plan.")
            return

        ranked = sorted(pending, key=lambda item: item.priority_score(),
                        reverse=True)
        print("\nTODAY'S PRIORITY-BASED STUDY PLAN")
        print("-" * 55)
        for task in ranked:
            if available <= 0:
                break
            allocation = min(task.remaining_hours(), available)
            if allocation > 0:
                print(f"{task.subject} – {task.task_name}: "
                      f"{allocation:.2f} hour(s) | "
                      f"Priority {task.priority_score():.1f}")
                available -= allocation
        print(f"Unallocated time: {available:.2f} hour(s)")

    def update_progress(self):
        self.show_tasks()
        if not self.tasks:
            return
        try:
            number = int(input("Task number to update: "))
            if not 1 <= number <= len(self.tasks):
                raise ValueError("Select a task number shown above.")
            progress = float(input("New progress (0-100): "))
            if not 0 <= progress <= 100:
                raise ValueError("Progress must be between 0 and 100.")
            self.tasks[number - 1].progress = progress
            self.save_data()
            print("Progress updated.")
        except ValueError as error:
            print("Invalid input:", error)

    def performance_summary(self):
        total = len(self.tasks)
        completed = sum(task.is_complete() for task in self.tasks)
        pending = total - completed
        average = (sum(task.progress for task in self.tasks) / total
                   if total else 0)
        planned_hours = sum(task.estimated_hours for task in self.tasks)
        remaining_hours = sum(task.remaining_hours() for task in self.tasks)

        print("\nPERFORMANCE SUMMARY")
        print("-" * 35)
        print(f"Total tasks       : {total}")
        print(f"Completed tasks   : {completed}")
        print(f"Pending tasks     : {pending}")
        print(f"Average progress : {average:.1f}%")
        print(f"Planned hours     : {planned_hours:.1f}")
        print(f"Remaining hours   : {remaining_hours:.1f}")
        if total:
            print("Highest priority  :",
                  max(self.tasks, key=lambda item: item.priority_score()).task_name)

    def run(self):
        while True:
            print("\nSMART STUDY PLANNER")
            print("1. Add task")
            print("2. View tasks")
            print("3. Generate study schedule")
            print("4. Update progress")
            print("5. Performance summary")
            print("6. Save and exit")
            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.show_tasks()
            elif choice == "3":
                self.generate_schedule()
            elif choice == "4":
                self.update_progress()
            elif choice == "5":
                self.performance_summary()
            elif choice == "6":
                self.save_data()
                print("Thank you for using Smart Study Planner.")
                break
            else:
                print("Invalid menu choice. Please enter 1-6.")


if __name__ == "__main__":
    StudyPlanner().run()
