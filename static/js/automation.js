document.addEventListener('DOMContentLoaded', function() {
    const taskInput = document.getElementById('taskInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const executeBtn = document.getElementById('executeBtn');
    const statusOutput = document.getElementById('statusOutput');

    analyzeBtn.addEventListener('click', async () => {
        const task = taskInput.value;
        if (!task) {
            addStatus('Error:', 'Please describe a task first');
            return;
        }

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task })
            });
            const data = await response.json();
            addStatus('Analysis:', data.analysis);
        } catch (error) {
            addStatus('Error:', error.message);
        }
    });

    executeBtn.addEventListener('click', async () => {
        const task = taskInput.value;
        if (!task) {
            addStatus('Error:', 'Please describe a task first');
            return;
        }

        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ task })
            });
            const data = await response.json();
            addStatus('Execution Plan:', data.plan);
        } catch (error) {
            addStatus('Error:', error.message);
        }
    });

    function addStatus(title, message) {
        const div = document.createElement('div');
        div.className = 'alert alert-info';
        div.innerHTML = `<strong>${title}</strong> ${message}`;
        statusOutput.prepend(div);
    }
});
