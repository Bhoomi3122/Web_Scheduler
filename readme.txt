Task Management Web Application

Introduction ->

This project is a Task Management Web Application built as the final capstone project for CS50 Web Development using Python and JavaScript. The application allows users to create, manage, and track their schedules efficiently with features like task completion tracking, automatic schedule updates, and a dedicated completed schedules section. It provides a simple yet powerful user experience for managing tasks in an organized way.


Pages & Functionalities ->

1. Active Schedules Page

Displays all ongoing schedules.

Users can see progress bars indicating task completion levels.

Pending tasks are shown at the top, while completed tasks move down automatically.

2. Completed Schedules Page

Lists all schedules that have been fully completed.

Allows users to view and review past schedules.

Completed schedules are automatically moved here once all tasks in a schedule are marked as completed.

3. Add Schedule Page

Users can create new schedules.

Each schedule requires a name and at least one task.

Tasks include a task name, description, start time, and end time.

4. View Schedule Page

Shows a detailed view of a selected schedule.

Tasks are arranged automatically based on their start time.

Provides task controls (Edit, Delete, Mark as Completed).

Includes a dynamically updating progress bar reflecting task completion status.

5. Edit Task Page

Allows users to update task details with a pre-filled form.

Changes are saved and reflected immediately in the schedule.


Features & Functionalities ->

User Signup & Login: Secure authentication system.

Create New Schedule: Users can create a schedule with multiple tasks.

View Active Schedules: Displays all ongoing schedules in an organized way.

View Schedule Details: Expands a schedule to show its tasks and status.

Mark Task as Completed: Updates task status and progress bar dynamically.

Edit Task: Modify task details including name, description, and time.

Delete Task: Removes a task with a confirmation alert.

Auto-Completion of Schedules: If all tasks are completed, the schedule moves to the Completed Schedules section.

Auto-Deletion of Schedules: If all tasks are deleted, the schedule is automatically removed.

Completed Schedule Section: Stores and displays fully completed schedules.


Tech Stack ->

Frontend: HTML, CSS, JavaScript (Vanilla + Fetch API)

Backend: Django (Python-based framework)

Database: SQLite (for storing user schedules and tasks)

Authentication: Django’s built-in user authentication

UI Design: Responsive design for desktop and mobile users

 
Uniqueness & Complexity ->

Task-Based Dynamic Sorting: Tasks within a schedule are automatically arranged based on their start time, making it easier to follow a timeline.

Real-Time Progress Bar: As tasks are completed, the progress bar updates dynamically to reflect completion.

Automatic Schedule Handling:

Completed schedules move automatically to the Completed Schedules section.

Deleting all tasks in a schedule leads to automatic schedule deletion.

User-Friendly Interface: Minimalistic design for effortless task tracking.

Multiple Features in One Application: Unlike existing apps focusing only on simple task tracking, this project offers a complete task scheduling solution.


Applications & Impact ->

Personal Productivity: Helps individuals manage their time efficiently.

Work & Team Coordination: Can be used by small teams to assign tasks and track progress.

Academic Use: Students can use it to schedule study sessions and assignments.

Freelancers & Entrepreneurs: Ideal for tracking project milestones and deadlines.

