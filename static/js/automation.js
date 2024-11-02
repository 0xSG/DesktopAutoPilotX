document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('taskForm');
    const executionLog = document.getElementById('executionLog');
    
    function addLogEntry(message, type = 'info') {
        const entry = document.createElement('div');
        entry.className = `log-entry text-${type} mb-2`;
        entry.textContent = `${new Date().toLocaleTimeString()}: ${message}`;
        executionLog.appendChild(entry);
        executionLog.scrollTop = executionLog.scrollHeight;
    }
    
    taskForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(taskForm);
        try {
            const response = await fetch('/task/create', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Task creation failed');
            }
            
            const result = await response.json();
            addLogEntry(`Task created: ${result.task_id}`, 'success');
            
            // Start monitoring task progress
            monitorTask(result.task_id);
        } catch (error) {
            addLogEntry(`Error: ${error.message}`, 'danger');
        }
    });
    
    async function monitorTask(taskId) {
        try {
            const response = await fetch(`/task/${taskId}/status`);
            const status = await response.json();
            
            addLogEntry(status.message);
            
            if (status.screenshot) {
                updateScreenshot(status.screenshot);
            }
            
            if (status.status !== 'completed' && status.status !== 'failed') {
                setTimeout(() => monitorTask(taskId), 1000);
            }
        } catch (error) {
            addLogEntry(`Monitoring error: ${error.message}`, 'danger');
        }
    }
    
    function updateScreenshot(screenshotUrl) {
        const screenshotDiv = document.getElementById('screenshot');
        screenshotDiv.innerHTML = `<img src="${screenshotUrl}" class="img-fluid" alt="Current screen">`;
    }
});
