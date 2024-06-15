document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('loader-overlay').style.display = 'none';
    const avatarModal = document.getElementById('avatarModal');
    const closeAvatarModal = document.getElementById('closeAvatarModal');
    const saveAvatarBtn = document.getElementById('saveAvatarBtn');
    const cancelAvatarBtn = document.getElementById('cancelAvatarBtn');
    const avatarImages = document.querySelectorAll('.avatars-grid img');
    const uploadAvatarInput = document.getElementById('uploadAvatarInput');
    let selectedAvatar = null;

    avatarImages.forEach(img => {
        img.addEventListener('click', function() {
            avatarImages.forEach(i => i.classList.remove('selected'));
            this.classList.add('selected');
            selectedAvatar = this.src;
        });
    });

    document.querySelector('.upload-area').addEventListener('click', function() {
        uploadAvatarInput.click();
    });

    uploadAvatarInput.addEventListener('change', function() {
        if (uploadAvatarInput.files.length > 0) {
            const uploadedFile = uploadAvatarInput.files[0];
            const reader = new FileReader();
            reader.onload = function(e) {
                avatarImages.forEach(i => i.classList.remove('selected'));
                document.querySelector('.upload-area img').src = e.target.result;
                document.querySelector('.upload-area img').classList.add('selected');
                selectedAvatar = e.target.result;
            };
            reader.readAsDataURL(uploadedFile);
        }
    });

    saveAvatarBtn.addEventListener('click', function() {
        if (selectedAvatar) {
            console.log('Selected avatar:', selectedAvatar);
            // Handle saving the selected avatar
        } else {
            alert('Please select or upload an avatar.');
        }
    });

    cancelAvatarBtn.addEventListener('click', function() {
        avatarModal.classList.add('slide-upSolid');
        avatarModal.classList.remove('slide-downSolid');
    });

    closeAvatarModal.addEventListener('click', function() {
        avatarModal.classList.add('slide-upSolid');
        avatarModal.classList.remove('slide-downSolid');
    });
        const profileIcon = document.getElementById('profileIcon');
        const tooltip = document.getElementById('profileTooltip');
        const avatarLink = document.getElementById('avatarLink');
    
        profileIcon.addEventListener('mouseenter', function() {
            tooltip.classList.remove('popOut');
            tooltip.classList.add('popIn');
            tooltip.style.visibility = 'visible';
        });
    
        profileIcon.addEventListener('mouseleave', function() {
            tooltip.classList.remove('popIn');
            tooltip.classList.add('popOut');
            tooltip.addEventListener('animationend', function() {
                tooltip.style.visibility = 'hidden';
            }, { once: true });
        });
    
        profileIcon.addEventListener('click', function() {
            avatarLink.click(); // Trigger click event on avatar link
        });
    });
    
    
    // Start session timeout timer only if the user is authenticated
    if (document.body.classList.contains('authenticated')) {
        startSessionTimer();
    }

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
                // No redirect here, just show the session expired message
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
var loginRequiredModal = document.getElementById("loginRequiredModal");
var openLoginModalButton = document.getElementById("openLoginModal");
var overlay = document.getElementById("overlay");
var loginLink = document.getElementById("loginLink");
var registerLink = document.getElementById("registerLink");
var closeLoginModal = document.getElementById("closeLoginModal");
var closeRegisterModal = document.getElementById("closeRegisterModal");
var loginLinkFromRegister = document.getElementById("loginLinkFromRegister");

// Show login modal and overlay
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
        registerModal.style.display = "block";
        overlay.style.display = "flex";
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

// Hide login modal and overlay
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

// Hide register modal and overlay
if (closeRegisterModal) {
    closeRegisterModal.onclick = function() {
        registerModal.classList.add("pop-out");
        loginModal.classList.add("pop-out");
        overlay.classList.add("hide");
        setTimeout(() => {
            registerModal.style.display = 'none';
            loginModal.style.display = 'none';
            overlay.style.display = 'none';
            registerModal.classList.remove('pop-in', 'pop-out');
            loginModal.classList.remove('pop-in', 'pop-out');
            overlay.classList.remove('show', 'hide');
        }, 300);
    }
}

// Show login required modal and overlay
var expressFeelingsButton = document.getElementById("loginButton");
if (expressFeelingsButton) {
    expressFeelingsButton.onclick = function(event) {
        event.preventDefault();
        loginRequiredModal.style.display = "block";
        overlay.style.display = "flex";
        setTimeout(() => {
            loginRequiredModal.classList.add("pop-in");
            overlay.classList.add("show");
        }, 10);
    }
}

// Close modal and overlay when clicking outside
window.onclick = function(event) {
    if (event.target == overlay) {
        if (loginRequiredModal.style.display === "block" || document.querySelector('.flat-ui-dialog.session').style.display === "block") {
            closeModals();
        }
    }
}

function closeModals() {
    if (loginRequiredModal.style.display === "block") {
        loginRequiredModal.classList.add("pop-out");
        overlay.classList.add("hide");
        setTimeout(() => {
            loginRequiredModal.style.display = "none";
            overlay.style.display = "none";
            loginRequiredModal.classList.remove("pop-in", "pop-out");
            overlay.classList.remove('show', 'hide');
        }, 300);
    } else if (document.querySelector('.flat-ui-dialog.session').style.display === "block") {
        const sessionDialogBox = document.querySelector('.flat-ui-dialog.session');
        sessionDialogBox.classList.add("pop-out");
        overlay.classList.add("hide");
        setTimeout(() => {
            sessionDialogBox.style.display = "none";
            overlay.style.display = "none";
            sessionDialogBox.classList.remove("pop-in", "pop-out");
            overlay.classList.remove('show', 'hide');
            window.location.reload();
        }, 300);
    }
}

// Close login required modal and show login modal
if (openLoginModalButton) {
    openLoginModalButton.onclick = function() {
        loginRequiredModal.classList.add("pop-out");
        setTimeout(() => {
            loginRequiredModal.style.display = "none";
            loginRequiredModal.classList.remove("pop-out");
            loginModal.style.display = "block";
            setTimeout(() => {
                loginModal.classList.add("pop-in");
            }, 10);
        }, 300);
    }
}

function showError(message, type) {
    const dialogBox = document.getElementById(type === 'login' ? 'loginDialogBox' : type === 'register' ? 'registerDialogBox' : 'sessionDialogBox');
    const dialogContent = document.getElementById(type === 'login' ? 'loginDialogContent' : type === 'register' ? 'registerDialogContent' : 'sessionDialogContent');

    dialogContent.innerHTML = message;
    dialogBox.style.display = 'block';
    dialogBox.classList.add('error');
    dialogBox.classList.remove('pop-out');
    dialogBox.classList.add('pop-in');
    
    if (type === 'session') {
        overlay.style.display = 'flex';
        overlay.classList.add('pop-in');
        overlay.addEventListener('click', function handleOverlayClick() {
            dialogBox.classList.add('pop-out');
            overlay.classList.add('hide');
            setTimeout(() => {
                dialogBox.style.display = 'none';
                dialogBox.classList.remove('pop-out');
                overlay.style.display = 'none';
                overlay.classList.remove('show', 'hide');
                overlay.removeEventListener('click', handleOverlayClick);
                window.location.reload();
            }, 300);
        });
    }

    if (type !== 'session') {
        setTimeout(() => {
            dialogBox.classList.remove('pop-in');
            dialogBox.classList.add('pop-out');
            setTimeout(() => {
                dialogBox.style.display = 'none';
                dialogBox.classList.remove('pop-out');
            }, 300);
        }, 3000);
    }
}

function showSuccess(message, type) {
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

    if (type === 'logout') {
        overlay.addEventListener('click', function handleOverlayClick() {
            successBox.classList.add('pop-out');
            overlay.classList.add('hide');
            setTimeout(() => {
                successBox.style.display = 'none';
                successBox.classList.remove('pop-out');
                overlay.style.display = 'none';
                overlay.classList.remove('show', 'hide');
                overlay.removeEventListener('click', handleOverlayClick);
                window.location.reload();
            }, 300);
        });
    }
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
        showError("An error occurred. Please try again.", 'login');
    });
});

document.querySelectorAll('.logout-link').forEach(item => {
    item.addEventListener('click', function(event) {
        event.preventDefault();
        
        // Disable the logout button to prevent multiple clicks
        this.style.pointerEvents = 'none';

        // Send the logout request
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
                    document.getElementById('logoutSuccessBox').classList.add("pop-out");
                    overlay.classList.add("hide");
                    setTimeout(() => {
                        document.getElementById('logoutSuccessBox').style.display = "none";
                        overlay.style.display = "none";
                        document.getElementById('logoutSuccessBox').classList.remove('pop-in', 'pop-out');
                        overlay.classList.remove('show', 'hide');
                        window.location.href = data.redirect_url;
                    }, 300);
                }, 1500);
            } else {
                // Handle failure silently
                window.location.reload(); // Refresh the page on failure
            }
        })
        .catch(error => {
            // Handle network errors silently
            window.location.reload(); // Refresh the page on error
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
    var controlPointX1 = Math.random() * 50;
    var controlPointY1 = Math.random() * 50;
    var controlPointX2 = 100 - Math.random() * 50;
    var controlPointY2 = Math.random() * 50;
    var endPointX = Math.random() * 100;
    var endPointY = Math.random() * 100;
    var d = `M0,0 C${controlPointX1},${controlPointY1} ${controlPointX2},${controlPointY2} ${endPointX},${endPointY}`;
    path.setAttribute('d', d);
});

// Function to fetch user profile data
function fetchUserProfile() {
    fetch('/get_user_profile/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('student-id').value = data.student_id;
            document.getElementById('username').value = data.username;
            document.getElementById('full-name').value = data.full_name;
            document.getElementById('academic-year').value = data.academic_year_level;
            document.getElementById('contact-number').value = data.contact_number;
            document.getElementById('email').value = data.email;
        })
        .catch(error => console.error('Error fetching user profile:', error));
}

// Function to update user profile data
function updateUserProfile(event) {
    event.preventDefault(); // Prevent the form from submitting in the traditional way

    const username = document.getElementById('username').value;
    const contactNumber = document.getElementById('contact-number').value;
    const email = document.getElementById('email').value;
    const academicYear = document.getElementById('academic-year').value;

    fetch('/update_user_profile/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')  // Include CSRF token
        },
        body: JSON.stringify({
            username: username,
            contact_number: contactNumber,
            email: email,
            academic_year_level: academicYear,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showSuccess('Profile updated successfully!', 'update');
        } else {
            // Check for specific errors
            if (data.errors.username) {
                showError(data.errors.username, 'update');
            } else if (data.errors.email) {
                showError(data.errors.email, 'update');
            } else {
                showError('Error updating profile. Please try again.', 'update');
            }
        }
    })
    .catch(error => {
        console.error('Error updating user profile:', error);
        showError('Error updating profile. Please try again.', 'update');
    });
}

document.getElementById('profileForm').addEventListener('submit', updateUserProfile);
