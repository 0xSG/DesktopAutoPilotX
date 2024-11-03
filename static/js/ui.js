document.addEventListener('DOMContentLoaded', function() {
    // Load saved settings
    loadSettings();
    
    // Initialize theme
    initializeTheme();
    
    // Settings Modal Functionality
    const settingsModal = document.getElementById('settingsModal');
    if (settingsModal) {
        // Theme mode handler
        const themeModeSelect = document.getElementById('themeMode');
        if (themeModeSelect) {
            themeModeSelect.addEventListener('change', (e) => {
                applyTheme(e.target.value);
            });
        }

        // Save settings button handler
        const saveButton = document.getElementById('saveSettings');
        if (saveButton) {
            saveButton.addEventListener('click', async () => {
                // Show loading state
                saveButton.disabled = true;
                const originalText = saveButton.innerHTML;
                saveButton.innerHTML = '<div class="loading-spinner"></div>';

                try {
                    const settings = {
                        theme: themeModeSelect.value,
                        models: {
                            vision: document.getElementById('visionModel').value,
                            reasoning: document.getElementById('reasoningModel').value
                        }
                    };

                    // Save to localStorage
                    localStorage.setItem('appSettings', JSON.stringify(settings));

                    // Update theme immediately
                    applyTheme(settings.theme);

                    // Close modal
                    const modal = bootstrap.Modal.getInstance(settingsModal);
                    modal.hide();
                    
                    showNotification('Settings saved successfully', 'success');
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

        // Update model status indicators and populate model lists
        async function updateModelStatus() {
            try {
                const [healthResponse, modelsResponse] = await Promise.all([
                    fetch('/health'),
                    fetch('/api/models/list')
                ]);

                const health = await healthResponse.json();
                const models = await modelsResponse.json();

                // Update status badges
                updateStatusBadge('visionStatus', health.ollama_service);
                updateStatusBadge('reasoningStatus', health.ollama_service);

                // Populate model dropdowns
                const visionSelect = document.getElementById('visionModel');
                const reasoningSelect = document.getElementById('reasoningModel');

                if (visionSelect && models.vision) {
                    populateModelSelect(visionSelect, models.vision);
                }
                if (reasoningSelect && models.reasoning) {
                    populateModelSelect(reasoningSelect, models.reasoning);
                }
            } catch (error) {
                console.error('Error updating model status:', error);
                showNotification('Failed to fetch model information', 'danger');
            }
        }

        // Update status when modal is shown
        settingsModal.addEventListener('show.bs.modal', updateModelStatus);
    }
});

// Theme Management
function initializeTheme() {
    const savedSettings = getSavedSettings();
    if (savedSettings && savedSettings.theme) {
        applyTheme(savedSettings.theme);
        document.getElementById('themeMode').value = savedSettings.theme;
    } else {
        // Default to system theme
        applyTheme('system');
    }
}

function applyTheme(mode) {
    const html = document.documentElement;
    
    if (mode === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        html.setAttribute('data-bs-theme', prefersDark ? 'dark' : 'light');
    } else {
        html.setAttribute('data-bs-theme', mode);
    }
}

// Helper Functions
function getSavedSettings() {
    try {
        return JSON.parse(localStorage.getItem('appSettings'));
    } catch {
        return null;
    }
}

function loadSettings() {
    const settings = getSavedSettings();
    if (settings) {
        // Apply theme
        if (settings.theme) {
            document.getElementById('themeMode').value = settings.theme;
            applyTheme(settings.theme);
        }

        // Apply model selections when dropdowns are available
        if (settings.models) {
            const visionSelect = document.getElementById('visionModel');
            const reasoningSelect = document.getElementById('reasoningModel');

            if (visionSelect && settings.models.vision) {
                visionSelect.value = settings.models.vision;
            }
            if (reasoningSelect && settings.models.reasoning) {
                reasoningSelect.value = settings.models.reasoning;
            }
        }
    }
}

function updateStatusBadge(elementId, isConnected) {
    const badge = document.getElementById(elementId);
    if (badge) {
        badge.className = `badge ${isConnected ? 'bg-success' : 'bg-danger'}`;
        badge.textContent = isConnected ? 'Connected' : 'Disconnected';
    }
}

function populateModelSelect(select, models) {
    select.innerHTML = '';
    models.forEach(model => {
        const option = document.createElement('option');
        option.value = model.id;
        option.textContent = `${model.name} - ${model.description}`;
        select.appendChild(option);
    });
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

// System theme change listener
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    const savedSettings = getSavedSettings();
    if (savedSettings && savedSettings.theme === 'system') {
        applyTheme('system');
    }
});
