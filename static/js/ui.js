document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 300);
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
                updateRangeBackground(llavaTemp);
            });
            updateRangeBackground(llavaTemp);
        }

        if (llamaTemp && llamaTempValue) {
            llamaTemp.addEventListener('input', (e) => {
                llamaTempValue.textContent = e.target.value;
                updateRangeBackground(llamaTemp);
            });
            updateRangeBackground(llamaTemp);
        }

        // Save settings button handler
        const saveButton = document.getElementById('saveSettings');
        if (saveButton) {
            saveButton.addEventListener('click', async () => {
                // Show loading state
                saveButton.disabled = true;
                const originalText = saveButton.innerHTML;
                saveButton.innerHTML = '<div class="loading-spinner"></div>';

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
                        
                        showNotification('Settings saved successfully', 'success');
                    } else {
                        throw new Error('Failed to save settings');
                    }
                } catch (error) {
                    console.error('Error saving settings:', error);
                    showNotification('Failed to save settings', 'danger');
                } finally {
                    // Reset button state
                    saveButton.disabled = false;
                    saveButton.innerHTML = originalText;
                }
            });
        }

        // Update model status indicators
        async function updateModelStatus() {
            try {
                const response = await fetch('/health');
                const status = await response.json();

                updateStatusBadge('llavaStatus', status.ollama_service);
                updateStatusBadge('llamaStatus', status.ollama_service);
            } catch (error) {
                console.error('Error updating model status:', error);
            }
        }

        // Update status when modal is shown
        settingsModal.addEventListener('show.bs.modal', updateModelStatus);
    }
});

// Helper Functions
function updateRangeBackground(rangeInput) {
    const value = (rangeInput.value - rangeInput.min) / (rangeInput.max - rangeInput.min) * 100;
    rangeInput.style.background = `linear-gradient(90deg, var(--apple-primary) ${value}%, var(--apple-border) ${value}%)`;
}

function updateStatusBadge(elementId, isConnected) {
    const badge = document.getElementById(elementId);
    if (badge) {
        badge.className = `badge ${isConnected ? 'bg-success' : 'bg-danger'}`;
        badge.textContent = isConnected ? 'Connected' : 'Disconnected';
    }
}

function showNotification(message, type) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.querySelector('main').insertBefore(alert, document.querySelector('main').firstChild);
    
    setTimeout(() => {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 300);
    }, 5000);
}
