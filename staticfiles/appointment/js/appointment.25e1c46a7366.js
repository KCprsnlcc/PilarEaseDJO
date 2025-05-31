/**
 * Appointment Module JavaScript
 * Handles UI interactions, form submissions, and AJAX calls for the appointment module
 */

document.addEventListener('DOMContentLoaded', function() {
  // Dashboard card hover effects
  const statCards = document.querySelectorAll('.dashboard-stat-card');
  if (statCards) {
    statCards.forEach(card => {
      card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-8px)';
        this.style.boxShadow = '0 12px 30px rgba(0, 0, 0, 0.15)';
      });
      
      card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(-5px)';
        this.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.12)';
      });
    });
  }
  
  // Table row hover effect
  const tableRows = document.querySelectorAll('.table tbody tr');
  if (tableRows) {
    tableRows.forEach(row => {
      row.addEventListener('mouseenter', function() {
        this.style.backgroundColor = 'rgba(63, 81, 181, 0.08)';
        this.style.transition = 'background-color 0.2s ease';
      });
      
      row.addEventListener('mouseleave', function() {
        this.style.backgroundColor = '';
      });
    });
  }
  
  // Handle appointment approval
  const approveButtons = document.querySelectorAll('.approve-btn');
  if (approveButtons) {
    approveButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        const appointmentId = this.getAttribute('data-id');
        updateAppointmentStatus(appointmentId, 'approved');
      });
    });
  }
  
  // Handle appointment rejection
  const rejectButtons = document.querySelectorAll('.reject-btn');
  if (rejectButtons) {
    rejectButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        const appointmentId = this.getAttribute('data-id');
        showRejectReasonModal(appointmentId);
      });
    });
  }
  
  // Handle appointment cancellation
  const cancelButtons = document.querySelectorAll('.cancel-btn');
  if (cancelButtons) {
    cancelButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        const appointmentId = this.getAttribute('data-id');
        showCancelReasonModal(appointmentId);
      });
    });
  }
  
  // Handle appointment rescheduling
  const rescheduleButtons = document.querySelectorAll('.reschedule-btn');
  if (rescheduleButtons) {
    rescheduleButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        const appointmentId = this.getAttribute('data-id');
        showRescheduleModal(appointmentId);
      });
    });
  }
  
  // Handle notification marking as read
  const markReadButtons = document.querySelectorAll('.mark-read-btn');
  if (markReadButtons) {
    markReadButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        const notificationId = this.getAttribute('data-id');
        markNotificationAsRead(notificationId);
      });
    });
  }
  
  // Initialize date/time pickers if available
  if (typeof flatpickr !== 'undefined') {
    flatpickr('.date-picker', {
      dateFormat: 'Y-m-d',
      minDate: 'today'
    });
    
    flatpickr('.time-picker', {
      enableTime: true,
      noCalendar: true,
      dateFormat: 'H:i',
      time_24hr: true,
      minuteIncrement: 30
    });
  }
  
  // Initialize tooltips
  const tooltips = document.querySelectorAll('[data-toggle="tooltip"]');
  if (tooltips.length > 0 && typeof bootstrap !== 'undefined') {
    tooltips.forEach(tooltip => {
      new bootstrap.Tooltip(tooltip);
    });
  }
  
  // Form validation
  const forms = document.querySelectorAll('.needs-validation');
  if (forms) {
    forms.forEach(form => {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      });
    });
  }
});

/**
 * Updates the status of an appointment via AJAX
 * @param {number} appointmentId - The ID of the appointment to update
 * @param {string} status - The new status ('approved', 'rejected', 'cancelled', etc.)
 * @param {string} reason - Optional reason for the status change
 */
function updateAppointmentStatus(appointmentId, status, reason = '') {
  // Get CSRF token from cookie
  const csrftoken = getCookie('csrftoken');
  
  // Prepare the request data
  const data = {
    appointment_id: appointmentId,
    status: status
  };
  
  if (reason) {
    data.reason = reason;
  }
  
  // Show loading indicator
  showLoadingIndicator();
  
  // Send AJAX request
  fetch('/appointment/appointment/' + appointmentId + '/update/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(data => {
    hideLoadingIndicator();
    
    if (data.success) {
      showSuccessMessage(data.message);
      // Reload the page after 1 second to show the updated state
      setTimeout(() => {
        location.reload();
      }, 1000);
    } else {
      showErrorMessage(data.message || 'An error occurred.');
    }
  })
  .catch(error => {
    hideLoadingIndicator();
    showErrorMessage('An error occurred: ' + error.message);
  });
}

/**
 * Mark a notification as read via AJAX
 * @param {number} notificationId - The ID of the notification to mark as read
 */
function markNotificationAsRead(notificationId) {
  const csrftoken = getCookie('csrftoken');
  
  fetch('/appointment/notifications/' + notificationId + '/mark-read/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      // Find the notification item and remove the 'unread' class
      const notificationItem = document.querySelector('.notification-item[data-id="' + notificationId + '"]');
      if (notificationItem) {
        notificationItem.classList.remove('unread');
      }
      
      // Update the notification count if necessary
      const countElements = document.querySelectorAll('.notification-badge');
      countElements.forEach(element => {
        const count = parseInt(element.textContent) - 1;
        if (count > 0) {
          element.textContent = count;
        } else {
          element.style.display = 'none';
        }
      });
    }
  })
  .catch(error => {
    console.error('Error marking notification as read:', error);
  });
}

/**
 * Shows a modal for entering rejection reason
 * @param {number} appointmentId - The ID of the appointment to reject
 */
function showRejectReasonModal(appointmentId) {
  // Create modal HTML if it doesn't exist
  if (!document.getElementById('rejectReasonModal')) {
    const modalHtml = `
      <div class="pilarease-admin-modal" id="rejectReasonModal">
        <div class="pilarease-admin-modal-content">
          <span class="pilarease-admin-close">&times;</span>
          <h2>Reject Appointment</h2>
          <p>Please provide a reason for rejecting this appointment:</p>
          <form id="rejectReasonForm">
            <div class="form-group">
              <textarea class="form-control" id="rejectReason" rows="3" required></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" id="cancelRejectBtn">Cancel</button>
              <button type="submit" class="pilarease-admin-button">Confirm Rejection</button>
            </div>
          </form>
        </div>
      </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Add event listeners
    document.querySelector('#rejectReasonModal .pilarease-admin-close').addEventListener('click', function() {
      document.getElementById('rejectReasonModal').style.display = 'none';
    });
    
    document.getElementById('cancelRejectBtn').addEventListener('click', function() {
      document.getElementById('rejectReasonModal').style.display = 'none';
    });
    
    document.getElementById('rejectReasonForm').addEventListener('submit', function(e) {
      e.preventDefault();
      const reason = document.getElementById('rejectReason').value;
      document.getElementById('rejectReasonModal').style.display = 'none';
      updateAppointmentStatus(currentAppointmentId, 'rejected', reason);
    });
  }
  
  // Store the current appointment ID
  window.currentAppointmentId = appointmentId;
  
  // Show the modal
  document.getElementById('rejectReasonModal').style.display = 'block';
}

/**
 * Shows a modal for entering cancellation reason
 * @param {number} appointmentId - The ID of the appointment to cancel
 */
function showCancelReasonModal(appointmentId) {
  // Create modal HTML if it doesn't exist
  if (!document.getElementById('cancelReasonModal')) {
    const modalHtml = `
      <div class="pilarease-admin-modal" id="cancelReasonModal">
        <div class="pilarease-admin-modal-content">
          <span class="pilarease-admin-close">&times;</span>
          <h2>Cancel Appointment</h2>
          <p>Please provide a reason for cancelling this appointment:</p>
          <form id="cancelReasonForm">
            <div class="form-group">
              <textarea class="form-control" id="cancelReason" rows="3" required></textarea>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" id="cancelCancelBtn">Back</button>
              <button type="submit" class="pilarease-admin-button">Confirm Cancellation</button>
            </div>
          </form>
        </div>
      </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Add event listeners
    document.querySelector('#cancelReasonModal .pilarease-admin-close').addEventListener('click', function() {
      document.getElementById('cancelReasonModal').style.display = 'none';
    });
    
    document.getElementById('cancelCancelBtn').addEventListener('click', function() {
      document.getElementById('cancelReasonModal').style.display = 'none';
    });
    
    document.getElementById('cancelReasonForm').addEventListener('submit', function(e) {
      e.preventDefault();
      const reason = document.getElementById('cancelReason').value;
      document.getElementById('cancelReasonModal').style.display = 'none';
      updateAppointmentStatus(currentAppointmentId, 'cancelled', reason);
    });
  }
  
  // Store the current appointment ID
  window.currentAppointmentId = appointmentId;
  
  // Show the modal
  document.getElementById('cancelReasonModal').style.display = 'block';
}

/**
 * Shows a modal for rescheduling an appointment
 * @param {number} appointmentId - The ID of the appointment to reschedule
 */
function showRescheduleModal(appointmentId) {
  // Implementation will depend on your UI/UX preferences
  // This is a placeholder function
  console.log('Showing reschedule modal for appointment ID:', appointmentId);
}

/**
 * Helper function to show a loading indicator
 */
function showLoadingIndicator() {
  if (!document.getElementById('loadingSpinner')) {
    const spinnerHtml = `
      <div id="loadingSpinner" class="loading-spinner">
        <i class="bx bx-loader-alt"></i> Processing...
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', spinnerHtml);
  }
  
  document.getElementById('loadingSpinner').style.display = 'block';
}

/**
 * Helper function to hide the loading indicator
 */
function hideLoadingIndicator() {
  const spinner = document.getElementById('loadingSpinner');
  if (spinner) {
    spinner.style.display = 'none';
  }
}

/**
 * Helper function to show a success message
 * @param {string} message - The success message to display
 */
function showSuccessMessage(message) {
  // Create alert element
  const alertHtml = `
    <div class="alert alert-success alert-dismissible fade show animate__animated animate__fadeIn" role="alert">
      <i class="bx bx-check-circle"></i>
      ${message}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  `;
  
  // Add to messages container or body if no container exists
  const messagesContainer = document.querySelector('.messages');
  if (messagesContainer) {
    messagesContainer.insertAdjacentHTML('beforeend', alertHtml);
  } else {
    const container = document.createElement('div');
    container.classList.add('messages');
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '1000';
    container.style.maxWidth = '400px';
    container.innerHTML = alertHtml;
    document.body.appendChild(container);
  }
  
  // Auto-remove after 5 seconds
  const newAlert = document.querySelector('.alert:last-child');
  setTimeout(() => {
    newAlert.classList.add('animate__fadeOut');
    setTimeout(() => {
      newAlert.remove();
    }, 500);
  }, 5000);
}

/**
 * Helper function to show an error message
 * @param {string} message - The error message to display
 */
function showErrorMessage(message) {
  // Implementation similar to showSuccessMessage but with error styling
  const alertHtml = `
    <div class="alert alert-danger alert-dismissible fade show animate__animated animate__fadeIn" role="alert">
      <i class="bx bx-x-circle"></i>
      ${message}
      <button type="button" class="close" data-dismiss="alert" aria-label="Close">
        <span aria-hidden="true">&times;</span>
      </button>
    </div>
  `;
  
  const messagesContainer = document.querySelector('.messages');
  if (messagesContainer) {
    messagesContainer.insertAdjacentHTML('beforeend', alertHtml);
  } else {
    const container = document.createElement('div');
    container.classList.add('messages');
    container.style.position = 'fixed';
    container.style.top = '20px';
    container.style.right = '20px';
    container.style.zIndex = '1000';
    container.style.maxWidth = '400px';
    container.innerHTML = alertHtml;
    document.body.appendChild(container);
  }
  
  const newAlert = document.querySelector('.alert:last-child');
  setTimeout(() => {
    newAlert.classList.add('animate__fadeOut');
    setTimeout(() => {
      newAlert.remove();
    }, 500);
  }, 5000);
}

/**
 * Helper function to get a cookie by name
 * Used for retrieving the CSRF token
 * @param {string} name - The name of the cookie to retrieve
 * @returns {string} The cookie value or an empty string if not found
 */
function getCookie(name) {
  let cookieValue = '';
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
} 