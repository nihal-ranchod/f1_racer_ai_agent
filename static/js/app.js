// F1 Racer AI Agent - Core JavaScript Functions with Toast Notifications

// Toast notification system
function showToast(title, message, type = 'info', duration = 5000) {
    const toastContainer = document.getElementById('toastContainer');
    const toastId = 'toast-' + Date.now();
    
    const iconMap = {
        'success': 'fas fa-check-circle',
        'info': 'fas fa-info-circle', 
        'warning': 'fas fa-exclamation-triangle',
        'danger': 'fas fa-times-circle'
    };
    
    const toast = document.createElement('div');
    toast.className = `f1-toast ${type}`;
    toast.id = toastId;
    toast.innerHTML = `
        <div class="f1-toast-header">
            <i class="f1-toast-icon ${iconMap[type]}"></i>
            <span class="f1-toast-title">${title}</span>
            <button class="f1-toast-close" onclick="removeToast('${toastId}')">&times;</button>
        </div>
        <div class="f1-toast-body">${message}</div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto-remove after duration
    setTimeout(() => removeToast(toastId), duration);
}

function removeToast(toastId) {
    const toast = document.getElementById(toastId);
    if (toast) {
        toast.style.animation = 'toastSlideOut 0.5s ease-out';
        setTimeout(() => {
            if (toast && toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 500);
    }
}

// Add slide out animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes toastSlideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Utility functions
function formatTimestamp(timestamp) {
    return new Date(timestamp).toLocaleString();
}

// API helper functions
async function makeApiRequest(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!result.success && result.error) {
            throw new Error(result.error);
        }
        
        return result;
    } catch (error) {
        console.error('API Request failed:', error);
        throw error;
    }
}

// Button loading states
function addLoadingState(button, originalText = null) {
    if (!originalText) {
        originalText = button.innerHTML;
    }
    
    button.disabled = true;
    button.innerHTML = `
        <div class="f1-spinner"></div> Processing...
    `;
    
    return originalText;
}

function removeLoadingState(button, originalText) {
    button.disabled = false;
    button.innerHTML = originalText;
}

// Tab switching with visual feedback
function showTab(tabName) {
    // Update sidebar buttons
    const buttons = document.querySelectorAll('.f1-quick-btn');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.id === tabName + '-btn') {
            btn.classList.add('active');
        }
    });
    
    // Hide all tabs
    const tabs = document.querySelectorAll('.f1-capability-tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
        tab.style.display = 'none';
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + '-tab');
    if (selectedTab) {
        selectedTab.style.display = 'block';
        setTimeout(() => {
            selectedTab.classList.add('active');
        }, 10);
    }
    
    // Tab switching is a minor UI action - no toast needed
}

// Load circuit and team data on page load
document.addEventListener('DOMContentLoaded', async function() {
    try {
        // Load circuits for simulation form
        const circuits = await fetch('/api/data/circuits');
        const circuitData = await circuits.json();
        
        const simCircuitSelect = document.getElementById('simCircuit');
        if (simCircuitSelect) {
            Object.keys(circuitData).forEach(key => {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = `${circuitData[key].name} (${circuitData[key].country})`;
                simCircuitSelect.appendChild(option);
            });
        }
        
        // Load circuits for update form
        const updateCircuitSelect = document.getElementById('updateCircuit');
        if (updateCircuitSelect) {
            Object.keys(circuitData).forEach(key => {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = `${circuitData[key].name} (${circuitData[key].country})`;
                updateCircuitSelect.appendChild(option);
            });
        }
        
    } catch (error) {
        console.error('Failed to load data:', error);
        showToast('Loading Error', 'Failed to load circuit data', 'warning');
    }
});

// Form validation with visual feedback
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = 'var(--danger)';
            field.style.boxShadow = '0 0 15px rgba(255, 68, 68, 0.3)';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--f1-grey)';
            field.style.boxShadow = 'none';
        }
    });
    
    if (!isValid) {
        showToast('Validation Error', 'Please fill in all required fields', 'warning');
    }
    
    return isValid;
}

// Copy to clipboard function with toast feedback
function copyToClipboard(text, successMessage = 'Copied to clipboard!') {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied!', successMessage, 'success', 2000);
    }).catch(function(err) {
        console.error('Failed to copy text: ', err);
        showToast('Copy Failed', 'Failed to copy text to clipboard', 'danger');
    });
}

// Format position for display
function formatPosition(position) {
    const pos = parseInt(position);
    let className = 'f1-position-other';
    
    if (pos === 1) className = 'f1-position-1';
    else if (pos === 2) className = 'f1-position-2';
    else if (pos === 3) className = 'f1-position-3';
    else if (pos <= 10) className = 'f1-position-points';
    
    return `<span class="f1-position-badge ${className}">P${pos}</span>`;
}

// Session type formatting
function formatSessionType(sessionType) {
    const sessionMap = {
        'fp1': 'Free Practice 1',
        'fp2': 'Free Practice 2',
        'fp3': 'Free Practice 3',
        'sprint_shootout': 'Sprint Shootout',
        'sprint_race': 'Sprint Race',
        'qualifying': 'Qualifying',
        'race': 'Race'
    };
    
    return sessionMap[sessionType] || sessionType.charAt(0).toUpperCase() + sessionType.slice(1);
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    showTab('speak');
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement && activeElement.form) {
                const submitButton = activeElement.form.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.click();
                    e.preventDefault();
                }
            }
        }
        
        // Number keys for quick tab switching (only when not typing in input fields)
        if (e.key >= '1' && e.key <= '4' && !e.ctrlKey && !e.altKey) {
            // Don't trigger tab switch if user is typing in an input field
            const activeElement = document.activeElement;
            if (activeElement && (activeElement.tagName === 'INPUT' || activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'SELECT' || activeElement.isContentEditable)) {
                return; // Let the user type normally
            }
            
            const tabMap = ['speak', 'act', 'think', 'simulation'];
            const tabIndex = parseInt(e.key) - 1;
            if (tabMap[tabIndex]) {
                showTab(tabMap[tabIndex]);
                e.preventDefault();
            }
        }
    });
    
    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });
    
    // Interface loaded - no toast needed for basic initialization
});