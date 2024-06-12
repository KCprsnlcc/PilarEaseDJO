document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loader').style.display = 'none';

    // Start session timeout timer
    startSessionTimer();
});

function startSessionTimer() {
    document.addEventListener('mousemove', resetTimer);
    document.addEventListener('keypress', resetTimer);

    const sessionTimeout = 30 * 60 * 1000;

    let timeout;

    function resetTimer() {
        clearTimeout(timeout);
        timeout = setTimeout(endSession, sessionTimeout);
    }

    function endSession() {
        showError("Session Expired, Please log in again.", 'session');
        fetch('/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            }
        }).then(response => response.json()).then(data => {
            if (data.success) {
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
            }
        });
    }

    resetTimer();
}

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

var loginModal = document.getElementById("loginModal");
var registerModal = document.getElementById("registerModal");
var overlay = document.getElementById("overlay");
var loginLink = document.getElementById("loginLink");
var registerLink = document.getElementById("registerLink");
var closeLoginModal = document.getElementById("closeLoginModal");
var closeRegisterModal = document.getElementById("closeRegisterModal");
var loginLinkFromRegister = document.getElementById("loginLinkFromRegister");

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

if (registerLink) {
    registerLink.onclick = function(event) {
        event.preventDefault();
        registerModal.style.display = "block";
        overlay.style.display = "flex";
        setTimeout(() => {
            registerModal.classList.add("pop-in");
            overlay.classList.add("show");
        }, 10);
    }
}

if (loginLinkFromRegister) {
    loginLinkFromRegister.onclick = function(event) {
        event.preventDefault();
        registerModal.classList.add("pop-out");
        setTimeout(() => {
            registerModal.style.display = "none";
            registerModal.classList.remove("pop-out");
            loginModal.style.display = "block";
            setTimeout(() => {
                loginModal.classList.add("pop-in");
                overlay.classList.add("show");
            }, 10);
        }, 300);
    }
}

if (closeLoginModal) {
    closeLoginModal.onclick = function() {
        loginModal.classList.add("pop-out");
        overlay.classList.add("hide");
        setTimeout(() => {
            loginModal.style.display = 'none';
            overlay.style.display = 'none';
            loginModal.classList.remove('pop-in', 'pop-out');
            overlay.classList.remove('show', 'hide');
        }, 300);
    }
}

if (closeRegisterModal) {
    closeRegisterModal.onclick = function() {
        registerModal.classList.add("pop-out");
        overlay.classList.add("hide");
        setTimeout(() => {
            registerModal.style.display = 'none';
            overlay.style.display = 'none';
            registerModal.classList.remove('pop-in', 'pop-out');
            overlay.classList.remove('show', 'hide');
        }, 300);
    }
}

function showError(message, type) {
    console.error(type + " error:", message);
    const dialogBox = document.getElementById(type === 'login' ? 'loginDialogBox' : type === 'register' ? 'registerDialogBox' : 'sessionDialogBox');
    const dialogContent = document.getElementById(type === 'login' ? 'loginDialogContent' : type === 'register' ? 'registerDialogContent' : 'sessionDialogContent');

    dialogContent.innerHTML = message;
    dialogBox.style.display = 'block';
    dialogBox.classList.add('error');
    dialogBox.classList.remove('pop-out');
    dialogBox.classList.add('pop-in');

    setTimeout(() => {
        dialogBox.classList.remove('pop-in');
        dialogBox.classList.add('pop-out');
        setTimeout(() => {
            dialogBox.style.display = 'none';
            dialogBox.classList.remove('pop-out');
        }, 300);
    }, 3000);
}

function showSuccess(message, type) {
    console.log(type + " success:", message);
    const successBox = document.getElementById(type === 'login' ? 'loginSuccessBox' : type === 'register' ? 'registerSuccessBox' : 'logoutSuccessBox');
    const successContent = document.getElementById(type === 'login' ? 'loginSuccessContent' : type === 'register' ? 'registerSuccessContent' : 'logoutSuccessContent');

    successContent.innerHTML = message;
    successBox.style.display = 'block';
    successBox.classList.add('success');
    successBox.classList.remove('pop-out');
    successBox.classList.add('pop-in');

    setTimeout(() => {
        successBox.classList.remove('pop-in');
        successBox.classList.add('pop-out');
        setTimeout(() => {
            successBox.style.display = 'none';
            successBox.classList.remove('pop-out');
        }, 300);
    }, 3000);
}

function parseErrorMessages(errors) {
    for (let field in errors) {
        if (errors.hasOwnProperty(field)) {
            return errors[field][0].message;
        }
    }
    return "An error occurred. Please try again.";
}

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
        showError(errorMessage, 'register');
        return;
    }
    fetch(this.action, {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Register response:", data);
        if (data.success) {
            showSuccess("Registration successful!", 'register');
            setTimeout(() => {
                registerModal.classList.add("pop-out");
                setTimeout(() => {
                    registerModal.style.display = "none";
                    registerModal.classList.remove("pop-out");
                    loginModal.style.display = "block";
                    setTimeout(() => {
                        loginModal.classList.add("pop-in");
                        overlay.classList.add("show");
                    }, 10);
                }, 300);

                document.getElementById('registerForm').reset();
            }, 1500);
        } else {
            let errorMessage = parseErrorMessages(data.error_message);
            showError(errorMessage, 'register');
        }
    })
    .catch(error => {
        console.error("Registration error:", error);
        showError("An error occurred. Please try again.", 'register');
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
        showError(errorMessage, 'login');
        return;
    }
    fetch(this.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams(formData).toString()
    })
    .then(response => response.json())
    .then(data => {
        console.log("Login response:", data);
        if (data.success) {
            showSuccess("Login successful!", 'login');
            setTimeout(() => {
                document.getElementById('loginForm').reset();
                loginModal.classList.add("pop-out");
                overlay.classList.add("hide");
                setTimeout(() => {
                    loginModal.style.display = "none";
                    overlay.style.display = "none";
                    loginModal.classList.remove('pop-in', 'pop-out');
                    overlay.classList.remove('show', 'hide');
                    window.location.href = data.redirect_url;
                }, 300);
            }, 1500);
        } else {
            let errorMessage = parseErrorMessages(data.error_message);
            showError(errorMessage, 'login');
        }
    })
    .catch(error => {
        console.error("Login error:", error);  // Log error for debugging
        showError("An error occurred. Please try again.", 'login');
    });
});

document.querySelectorAll('.logout-link').forEach(item => {
    item.addEventListener('click', function(event) {
        event.preventDefault();
        fetch(this.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showSuccess("Logout successful!", 'logout');
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1500);
            }
        })
        .catch(error => {
            console.error("Logout error:", error);  // Log error for debugging
            showError("An error occurred during logout. Please try again.", 'logout');
        });
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

document.querySelectorAll('.v1_124 div').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.v1_127, .v1_129, .v1_131, .v1_133, .v1_135, .v1_137, .v1_139, .v1_141').forEach(span => {
            span.classList.remove('active');
        });
        this.querySelector('span').classList.add('active');
    });
});

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
