// Main JavaScript file for the subscription management system

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    // Add subscription form validation
    const addSubscriptionForm = document.querySelector('form[action*="add_subscription"]');
    if (addSubscriptionForm) {
        addSubscriptionForm.addEventListener('submit', function(e) {
            const price = document.getElementById('price').value;
            const termMonths = document.getElementById('term_months').value;
            
            if (price <= 0) {
                e.preventDefault();
                alert('Please enter a valid price greater than 0');
                return false;
            }
            
            if (!termMonths) {
                e.preventDefault();
                alert('Please select a subscription term');
                return false;
            }
        });
    }
    
    // Renew subscription form validation
    const renewSubscriptionForm = document.querySelector('form[action*="renew_subscription"]');
    if (renewSubscriptionForm) {
        renewSubscriptionForm.addEventListener('submit', function(e) {
            const termMonths = document.getElementById('term_months').value;
            const transactionId = document.getElementById('transaction_id').value;
            
            if (!termMonths) {
                e.preventDefault();
                alert('Please select a subscription term');
                return false;
            }
            
            if (!transactionId) {
                e.preventDefault();
                alert('Please enter a transaction ID');
                return false;
            }
        });
    }
});

// Auto-update subscription status
function updateSubscriptionStatus() {
    const statusElements = document.querySelectorAll('[id^="time-remaining-"]');
    statusElements.forEach(element => {
        const subscriptionId = element.id.split('-')[2];
        fetch(`/api/subscription/${subscriptionId}/status`)
            .then(response => response.json())
            .then(data => {
                element.textContent = data.time_remaining;
                element.classList.add('status-change');
                setTimeout(() => {
                    element.classList.remove('status-change');
                }, 500);
            });
    });
}

// Initialize auto-update if on subscriptions page
if (window.location.pathname.includes('/subscriptions')) {
    updateSubscriptionStatus();
    setInterval(updateSubscriptionStatus, 60000); // Update every minute
}

// Chart initialization
function initializeCharts() {
    const chartElements = document.querySelectorAll('canvas');
    chartElements.forEach(canvas => {
        const ctx = canvas.getContext('2d');
        const chartType = canvas.id.includes('subscription') ? 'line' : 'doughnut';
        
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: ['#28a745', '#007bff', '#dc3545'],
                    borderColor: ['#28a745', '#007bff', '#dc3545'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });
}

// Initialize charts if on dashboard page
if (window.location.pathname === '/') {
    initializeCharts();
} 