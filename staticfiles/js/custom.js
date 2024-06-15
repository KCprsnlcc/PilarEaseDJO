// Script for dropdown menu
const burger = document.getElementById('burger');
const dropdown = document.querySelector('.dropdown');
const profileLink = document.getElementById('profileLink');
const profileModal = document.getElementById('profileModal');
const closeProfileModal = document.getElementById('closeProfileModal');
const avatarLink = document.getElementById('avatarLink');
const avatarModal = document.getElementById('avatarModal');
const closeAvatarModal = document.getElementById('closeAvatarModal');
const passwordLink = document.getElementById('passwordLink');
const passwordModal = document.getElementById('passwordModal');
const closePasswordModal = document.getElementById('closePasswordModal');
// Function to close currently open modal
function closeCurrentModal() {
    const modals = document.querySelectorAll('.modal-content');
    modals.forEach(modal => {
        if (modal.style.display === 'block') {
            modal.classList.add('slide-upSolid');
            modal.classList.remove('slide-downSolid');
        }
    });
}

// Listen for the end of the slide-up animation to hide the modal
document.querySelectorAll('.modal-content').forEach(modal => {
    modal.addEventListener('animationend', (event) => {
        if (event.animationName === 'slideUpSolid') {
            modal.style.display = 'none';
        }
    });
});
// Show profile modal when profile link is clicked
profileLink.addEventListener('click', (e) => {
    e.preventDefault();
    closeCurrentModal();
    profileModal.style.display = 'block';
    profileModal.classList.add('slide-downSolid');
    profileModal.classList.remove('slide-upSolid');
    fetchUserProfile();  // Fetch and populate user data when the modal is opened
});
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
    closeCurrentModal();
    profileModal.style.display = 'block';
    profileModal.classList.add('slide-downSolid');
    profileModal.classList.remove('slide-upSolid');
});

// Close profile modal when the close button is clicked
closeProfileModal.addEventListener('click', () => {
    closeProfileModal.style.display = 'none'; // Hide the close button
    profileModal.classList.add('slide-upSolid');
    profileModal.classList.remove('slide-downSolid');
});

// Show avatar modal when avatar link is clicked
avatarLink.addEventListener('click', (e) => {
    e.preventDefault();
    closeCurrentModal();
    avatarModal.style.display = 'block';
    avatarModal.classList.add('slide-downSolid');
    avatarModal.classList.remove('slide-upSolid');
});

// Close avatar modal when the close button is clicked
closeAvatarModal.addEventListener('click', () => {
    closeAvatarModal.style.display = 'none'; // Hide the close button
    avatarModal.classList.add('slide-upSolid');
    avatarModal.classList.remove('slide-downSolid');
});

// Show password modal when password link is clicked
passwordLink.addEventListener('click', (e) => {
    e.preventDefault();
    closeCurrentModal();
    passwordModal.style.display = 'block';
    passwordModal.classList.add('slide-downSolid');
    passwordModal.classList.remove('slide-upSolid');
});

// Close password modal when the close button is clicked
closePasswordModal.addEventListener('click', () => {
    closePasswordModal.style.display = 'none'; // Hide the close button
    passwordModal.classList.add('slide-upSolid');
    passwordModal.classList.remove('slide-downSolid');
});