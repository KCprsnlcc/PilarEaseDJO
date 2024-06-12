function showError(message) {
    const dialogOverlay = document.getElementById('dialogOverlay');
    const dialogBox = document.getElementById('dialogBox');
    const dialogContent = document.getElementById('dialogContent');
    
    dialogContent.innerHTML = message;
    dialogOverlay.style.display = 'block';
    dialogBox.style.display = 'block';
    
    dialogOverlay.classList.add('show');
    dialogBox.classList.add('pop-in');

    setTimeout(() => {
        dialogBox.classList.remove('pop-in');
    }, 300);
}

function showSuccess(message) {
    const successOverlay = document.getElementById('successOverlay');
    const successBox = document.getElementById('successBox');
    const successContent = document.getElementById('successContent');
    
    successContent.innerHTML = message;
    successOverlay.style.display = 'block';
    successBox.style.display = 'block';
    
    successOverlay.classList.add('show');
    successBox.classList.add('pop-in');

    setTimeout(() => {
        successBox.classList.remove('pop-in');
    }, 300);
}

function closeErrorDialog() {
    const dialogOverlay = document.getElementById('dialogOverlay');
    const dialogBox = document.getElementById('dialogBox');

    dialogBox.classList.add('pop-out');
    setTimeout(() => {
        dialogOverlay.style.display = 'none';
        dialogBox.style.display = 'none';
        dialogBox.classList.remove('pop-out');
    }, 300);
}

function closeSuccessDialog() {
    const successOverlay = document.getElementById('successOverlay');
    const successBox = document.getElementById('successBox');

    successBox.classList.add('pop-out');
    setTimeout(() => {
        successOverlay.style.display = 'none';
        successBox.style.display = 'none';
        successBox.classList.remove('pop-out');
    }, 300);
}

// Close dialog when clicking outside
document.getElementById('dialogOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
        closeErrorDialog();
    }
});

document.getElementById('dialogClose').addEventListener('click', function() {
    closeErrorDialog();
});

document.getElementById('successOverlay').addEventListener('click', function(event) {
    if (event.target === this) {
        closeSuccessDialog();
    }
});

document.getElementById('successClose').addEventListener('click', function() {
    closeSuccessDialog();
});

// Modal functionality
var loginModal = document.getElementById("loginModal");
var registerModal = document.getElementById("registerModal");
var overlay = document.getElementById("overlay");
var loginLink = document.getElementById("loginLink");
var registerLink = document.getElementById("registerLink");
var closeLoginModal = document.getElementById("closeLoginModal");
var closeRegisterModal = document.getElementById("closeRegisterModal");
var loginLinkFromRegister = document.getElementById("loginLinkFromRegister");

// Show login modal and        overlay
if (loginLink) {
    loginLink.onclick = function(event) {
        event.preventDefault();
        loginModal.style.display = "block";
        overlay.style.display = "flex";
        setTimeout(() => {
            loginModal.classList.add("pop-in");
            overlay.classList.add("show");
        }, 10);
    }
}

// Show register modal and overlay
if (registerLink) {
    registerLink.onclick = function(event) {
        event.preventDefault();
        loginModal.style.display = "none";
        registerModal.style.display = "block";
        setTimeout(() => {
            registerModal.classList.add("pop-in");
            overlay.classList.add("show");
        }, 10);
    }
}

// Show login modal from register modal
if (loginLinkFromRegister) {
    loginLinkFromRegister.onclick = function(event) {
        event.preventDefault();
        registerModal.style.display = "none";
        loginModal.style.display = "block";
        setTimeout(() => {
            loginModal.classList.add("pop-in");
            overlay.classList.add("show");
        }, 10);
    }
}

// Hide login modal and overlay
if (closeLoginModal) {
    closeLoginModal.onclick = function() {
        loginModal.classList.add("pop-out");
        overlay.classList.add("hide");
        setTimeout(() => {
            loginModal.style.display = "none";
            overlay.style.display = "none";
            loginModal.classList.remove("pop-in", "pop-out");
            overlay.classList.remove("show", "hide");
        }, 300);
    }
}

// Hide register modal and overlay
if (closeRegisterModal) {
    closeRegisterModal.onclick = function() {
        registerModal.classList.add("pop-out");
        overlay.classList.add("hide");
        setTimeout(() => {
            registerModal.style.display = "none";
            overlay.style.display = "none";
            registerModal.classList.remove("pop-in", "pop-out");
            overlay.classList.remove("show", "hide");
        }, 300);
    }
}

// Hide modals and overlay when clicking outside
window.onclick = function(event) {
    if (event.target == overlay) {
        if (loginModal.style.display === "block") {
            loginModal.classList.add("pop-out");
        }
        if (registerModal.style.display === "block") {
            registerModal.classList.add("pop-out");
        }
        overlay.classList.add("hide");
        setTimeout(() => {
            loginModal.style.display = "none";
            registerModal.style.display = "none";
            overlay.style.display = "none";
            loginModal.classList.remove("pop-in", "pop-out");
            registerModal.classList.remove("pop-in", "pop-out");
            overlay.classList.remove("show", "hide");
        }, 300);
    }
}

// Hide the loader when the page is fully loaded
window.addEventListener('load', function() {
    document.getElementById('loader').style.display = 'none';
});
function getCookie(name) {
    let cookieValue = null;
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

const csrftoken = getCookie('csrftoken');

document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    let errorMessage = checkEmptyFields(formData, {
        'student_id': 'Student ID No.',
        'username': 'Username',
        'full_name': 'Full Name',
        'academic_year_level': 'Academic Year Level',
        'contact_number': 'Contact Number',
        'email': 'Email',
        'password1': 'Password',
        'password2': 'Confirm Password'
    });
    if (errorMessage) {
        showError(errorMessage);
        return;
    }
    fetch(this.action, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess("Registration successful!");
            setTimeout(() => {
                window.location.href = data.redirect_url;
            }, 1500);
        } else {
            let errorMessage = parseErrorMessages(data.error_message);
            showError(errorMessage);
        }
    })
    .catch(error => {
        showError("An error occurred. Please try again.");
    });
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    let errorMessage = checkEmptyFields(formData, {
        'username': 'Username',
        'password': 'Password'
    });
    if (errorMessage) {
        showError(errorMessage);
        return;
    }
    fetch(this.action, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            let errorMessage = parseErrorMessages(data.error_message);
            showError(errorMessage);
        }
    })
    .catch(error => {
        showError("An error occurred. Please try again.");
    });
});

function checkEmptyFields(formData, fields) {
    let emptyFields = [];
    let allFieldsEmpty = true;

    for (let field in fields) {
        if (formData.get(field) && formData.get(field).trim() !== "") {
            allFieldsEmpty = false;
        } else {
            emptyFields.push(fields[field] + " is required.");
        }
    }

    if (allFieldsEmpty) {
        return "All fields are required.";
    }

    return emptyFields.length ? emptyFields[0] : null;
}

function parseErrorMessages(errors) {
    const fieldNames = {
        'student_id': 'Student ID No.',
        'username': 'Username',
        'full_name': 'Full Name',
        'academic_year_level': 'Academic Year Level',
        'contact_number': 'Contact Number',
        'email': 'Email',
        'password1': 'Password',
        'password2': 'Confirm Password'
    };

    let errorMessages = '';
    for (let field in errors) {
        if (errors.hasOwnProperty(field)) {
            errors[field].forEach(error => {
                errorMessages += `<p>${fieldNames[field]}: ${error.message}</p>`;
            });
        }
    }
    return errorMessages;
}

// Additional functionality

document.querySelectorAll('.v1_124 div').forEach(item => {
    item.addEventListener('click', function() {
        // Remove 'active' class from all spans
        document.querySelectorAll('.v1_127, .v1_129, .v1_131, .v1_133, .v1_135, .v1_137, .v1_139, .v1_141').forEach(span => {
            span.classList.remove('active');
        });
        // Add 'active' class to clicked span
        this.querySelector('span').classList.add('active');
    });
});

// Check for click events on the "EXPRESS YOUR FEELINGS" button
document.getElementById('loginButton').addEventListener('click', function() {
    console.log('Login button clicked'); // Debugging statement
    document.getElementById('dialogOverlay').style.display = 'block';
    document.getElementById('dialogBox').style.display = 'block';
});

// Check for click events on the close button
document.getElementById('dialogClose').addEventListener('click', function() {
    console.log('Close button clicked'); // Debugging statement
    document.getElementById('dialogOverlay').style.display = 'none';
    document.getElementById('dialogBox').style.display = 'none';
});

// Hide the modal if the user clicks outside of it
window.onclick = function(event) {
    var modal = document.getElementById('dialogBox');
    if (event.target == modal) {
        modal.style.display = 'none';
        document.getElementById('dialogOverlay').style.display = 'none';
    }
};

// Randomize curves
document.querySelectorAll('.curved-line path').forEach(function(path) {
    var controlPointX1 = Math.random() * 50; // Random control point X1
    var controlPointY1 = Math.random() * 50; // Random control point Y1
    var controlPointX2 = 100 - Math.random() * 50; // Random control point X2
    var controlPointY2 = Math.random() * 50; // Random control point Y2
    var endPointX = Math.random() * 100; // Random end point X
    var endPointY = Math.random() * 100; // Random end point Y
    var d = `M0,0 C${controlPointX1},${controlPointY1} ${controlPointX2},${controlPointY2} ${endPointX},${endPointY}`; // Construct path data
    path.setAttribute('d', d); // Set path data
});
