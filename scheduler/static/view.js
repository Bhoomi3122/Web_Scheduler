document.addEventListener("DOMContentLoaded", () => {
    const chevronButtons = document.querySelectorAll(".chevron-btn");

    chevronButtons.forEach(button => {
        button.addEventListener("click", () => {
            const taskId = button.getAttribute("data-task-id");
            const detailsElement = document.getElementById(`details-${taskId}`);

            if (detailsElement.classList.contains("show")) {
                detailsElement.style.height = `${detailsElement.scrollHeight}px`;
                requestAnimationFrame(() => {
                    detailsElement.style.height = '0';
                });
                detailsElement.classList.remove("show");
                button.innerHTML = '<i class="bi bi-chevron-down"></i>';
            } else {
                detailsElement.style.height = '0';
                detailsElement.classList.add("show");
                requestAnimationFrame(() => {
                    detailsElement.style.height = `${detailsElement.scrollHeight}px`;
                });
                button.innerHTML = '<i class="bi bi-chevron-up"></i>';

                detailsElement.addEventListener("transitionend", () => {
                    if (detailsElement.classList.contains("show")) {
                        detailsElement.style.height = 'auto';
                    }
                }, { once: true });
            }
        });
    });
});

