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
    profileModal.classList.add('slide-down');
    profileModal.classList.remove('slide-up');
});

// Close profile modal when the close button is clicked
closeProfileModal.addEventListener('click', () => {
    profileModal.classList.add('slide-up');
    profileModal.classList.remove('slide-down');
});

profileModal.addEventListener('animationend', (event) => {
    if (event.animationName === 'slideUp') {
        profileModal.style.display = 'none';
    }
});
