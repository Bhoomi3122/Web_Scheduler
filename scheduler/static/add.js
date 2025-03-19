document.addEventListener("DOMContentLoaded", () => {
    const addTaskBtn = document.getElementById("add-task-btn");
    const tasksContainer = document.getElementById("tasks-container");
    const taskCardsContainer = document.getElementById("task-cards-container");
    const scheduleForm = document.getElementById("add-schedule-form");

    let tasks = [];
    let taskIdCounter = 0;

    addTaskBtn.addEventListener("click", () => {
        const taskForm = document.createElement("div");
        taskForm.classList.add("task-form");

        taskForm.innerHTML = `
            <label>Task Name:</label>
            <input type="text" class="task-name" required>
            <label>Description:</label>
            <textarea class="task-description"></textarea>
            <label>Start Time:</label>
            <div class="time-picker">
                <input type="number" class="task-start-hour" min="1" max="12" required>
                <span>:</span>
                <input type="number" class="task-start-minute" min="0" max="59" required>
                <select class="task-start-period">
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                </select>
            </div>
            <label>End Time:</label>
            <div class="time-picker">
                <input type="number" class="task-end-hour" min="1" max="12" required>
                <span>:</span>
                <input type="number" class="task-end-minute" min="0" max="59" required>
                <select class="task-end-period">
                    <option value="AM">AM</option>
                    <option value="PM">PM</option>
                </select>
            </div>
            <button type="button" class="submit-task-btn">Submit Task</button>
        `;
        tasksContainer.appendChild(taskForm);
    });

    tasksContainer.addEventListener("click", (e) => {
        if (e.target.classList.contains("submit-task-btn")) {
            const taskForm = e.target.closest(".task-form");

            const taskName = taskForm.querySelector(".task-name").value;
            const description = taskForm.querySelector(".task-description").value;
            const startHour = taskForm.querySelector(".task-start-hour").value;
            const startMinute = taskForm.querySelector(".task-start-minute").value;
            const startPeriod = taskForm.querySelector(".task-start-period").value;
            const endHour = taskForm.querySelector(".task-end-hour").value;
            const endMinute = taskForm.querySelector(".task-end-minute").value;
            const endPeriod = taskForm.querySelector(".task-end-period").value;

            if (!taskName || !startHour || !startMinute || !endHour || !endMinute) {
                alert("Please fill out all required fields!");
                return;
            }

            const task = {
                name: taskName,
                description: description,
                start_time: `${startHour}:${startMinute} ${startPeriod}`,
                end_time: `${endHour}:${endMinute} ${endPeriod}`,
            };

            tasks.push(task);
            createTaskCard(task);
            taskForm.remove();
        }
    });

    function deleteTask(taskId) {
        tasks = tasks.filter((task) => task.id !== taskId);
        const taskCard = document.querySelector(`.task-card[data-id='${taskId}']`);
        if (taskCard) {
            taskCard.remove();
        }
    }

    function createTaskCard(task) {
        taskIdCounter++;
        const taskCard = document.createElement("div");
        taskCard.classList.add("card", "task-card");
        taskCard.setAttribute('data-id', taskIdCounter);

        taskCard.innerHTML = `
            <div class="card-body">
                <h5 class="card-title">${task.name}</h5>
                <p class="card-text"><strong>Start Time:</strong> ${task.start_time}</p>
                <p class="card-text"><strong>End Time:</strong> ${task.end_time}</p>
                <button type="button" class="btn">Delete Task</button>
            </div>
        `;

        const deleteButton = taskCard.querySelector("button");
        deleteButton.addEventListener("click", () => deleteTask(taskIdCounter));
        taskCardsContainer.appendChild(taskCard);
    }

    scheduleForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const scheduleTitle = document.getElementById("schedule-title").value;

        if (!scheduleTitle) {
            alert("Please provide a schedule title!");
            return;
        }

        fetch("/create-schedule/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
            body: JSON.stringify({
                schedule_title: scheduleTitle,
                tasks: tasks,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                window.location.href = `/view/${data.schedule_id}`;
            } else {
                alert("Failed to create schedule!");
            }
        })
        .catch(() => alert("An error occurred while creating the schedule."));
    });
});
