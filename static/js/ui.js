// Shared UI functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // Settings Modal Functionality
    const settingsModal = document.getElementById('settingsModal');
    if (settingsModal) {
        // Temperature range input handlers
        const llavaTemp = document.getElementById('llavaTemp');
        const llavaTempValue = document.getElementById('llavaTempValue');
        const llamaTemp = document.getElementById('llamaTemp');
        const llamaTempValue = document.getElementById('llamaTempValue');

        if (llavaTemp && llavaTempValue) {
            llavaTemp.addEventListener('input', (e) => {
                llavaTempValue.textContent = e.target.value;
            });
        }

        if (llamaTemp && llamaTempValue) {
            llamaTemp.addEventListener('input', (e) => {
                llamaTempValue.textContent = e.target.value;
            });
        }

        // Save settings button handler
        const saveButton = document.getElementById('saveSettings');
        if (saveButton) {
            saveButton.addEventListener('click', async () => {
                const settings = {
                    llava: {
                        temperature: parseFloat(llavaTemp.value),
                        max_tokens: parseInt(document.getElementById('llavaTokens').value)
                    },
                    llama2: {
                        temperature: parseFloat(llamaTemp.value),
                        max_tokens: parseInt(document.getElementById('llamaTokens').value)
                    }
                };

                try {
                    const response = await fetch('/settings/update', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(settings)
                    });

                    if (response.ok) {
                        const result = await response.json();
                        const modal = bootstrap.Modal.getInstance(settingsModal);
                        modal.hide();
                        
                        // Show success message
                        const alert = document.createElement('div');
                        alert.className = 'alert alert-success';
                        alert.textContent = 'Settings saved successfully';
                        document.querySelector('main').insertBefore(alert, document.querySelector('main').firstChild);
                        
                        // Auto-hide alert
                        setTimeout(() => {
                            alert.style.opacity = '0';
                            setTimeout(() => alert.remove(), 500);
                        }, 5000);
                    } else {
                        throw new Error('Failed to save settings');
                    }
                } catch (error) {
                    console.error('Error saving settings:', error);
                    const alert = document.createElement('div');
                    alert.className = 'alert alert-danger';
                    alert.textContent = 'Failed to save settings';
                    document.querySelector('main').insertBefore(alert, document.querySelector('main').firstChild);
                }
            });
        }

        // Update model status indicators
        async function updateModelStatus() {
            try {
                const response = await fetch('/health');
                const status = await response.json();

                const llavaStatus = document.getElementById('llavaStatus');
                const llamaStatus = document.getElementById('llamaStatus');

                if (status.ollama_service) {
                    llavaStatus.className = 'badge bg-success';
                    llavaStatus.textContent = 'Connected';
                    llamaStatus.className = 'badge bg-success';
                    llamaStatus.textContent = 'Connected';
                } else {
                    llavaStatus.className = 'badge bg-danger';
                    llavaStatus.textContent = 'Disconnected';
                    llamaStatus.className = 'badge bg-danger';
                    llamaStatus.textContent = 'Disconnected';
                }
            } catch (error) {
                console.error('Error updating model status:', error);
            }
        }

        // Update status when modal is shown
        settingsModal.addEventListener('show.bs.modal', updateModelStatus);
    }
});
