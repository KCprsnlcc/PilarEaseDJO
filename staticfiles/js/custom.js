// Script for dropdown menu
const burger = document.getElementById('burger');
const dropdown = document.querySelector('.dropdown');
const profileLink = document.getElementById('profileLink');
const profileModal = document.getElementById('profileModal');
const closeProfileModal = document.getElementById('closeProfileModal');

burger.addEventListener('change', () => {
    if (burger.checked) {
        dropdown.classList.add('slide-down');
        dropdown.classList.remove('slide-up');
        dropdown.style.display = 'block';
    } else {
        dropdown.classList.add('slide-up');
        dropdown.classList.remove('slide-down');
    }
});

dropdown.addEventListener('animationend', (event) => {
    if (event.animationName === 'slideUp') {
        dropdown.style.display = 'none';
    }
});

// Close dropdown menu when any link is clicked
document.querySelectorAll('.dropdown a').forEach(link => {
    link.addEventListener('click', () => {
        burger.checked = false;
        dropdown.classList.add('slide-up');
        dropdown.classList.remove('slide-down');
    });
});

// Show profile modal when profile link is clicked
profileLink.addEventListener('click', (e) => {
    e.preventDefault();
    profileModal.style.display = 'block';
    profileModal.classList.add('slide-downOp');
    profileModal.classList.remove('slide-upOp');
});

// Close profile modal when the close button is clicked
closeProfileModal.addEventListener('click', () => {
    profileModal.classList.add('slide-upOp');
    profileModal.classList.remove('slide-downOp');
});

profileModal.addEventListener('animationend', (event) => {
    if (event.animationName === 'slideUpOp') {
        profileModal.style.display = 'none';
    }
});

// Show profile modal when profile link is clicked
avatarLink.addEventListener('click', (e) => {
    e.preventDefault();
    avatarModal.style.display = 'block';
    avatarModal.classList.add('slide-downOp');
    avatarModal.classList.remove('slide-upOp');
});

// Close profile modal when the close button is clicked
closeAvatarModal.addEventListener('click', () => {
    avatarModal.classList.add('slide-upOp');
    avatarModal.classList.remove('slide-downOp');
});

avatarModal.addEventListener('animationend', (event) => {
    if (event.animationName === 'slideUpOp') {
        avatarModal.style.display = 'none';
    }
});

// Show profile modal when profile link is clicked
passwordLink.addEventListener('click', (e) => {
    e.preventDefault();
    passwordModal.style.display = 'block';
    passwordModal.classList.add('slide-downOp');
    passwordModal.classList.remove('slide-upOp');
});

// Close profile modal when the close button is clicked
closePasswordModal.addEventListener('click', () => {
    passwordModal.classList.add('slide-upOp');
    passwordModal.classList.remove('slide-downOp');
});

passwordModal.addEventListener('animationend', (event) => {
    if (event.animationName === 'slideUpOp') {
        passwordModal.style.display = 'none';
    }
});