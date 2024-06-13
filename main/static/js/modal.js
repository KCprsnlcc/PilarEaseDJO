// Floating Nav Button Logic

const nav = document.querySelector("nav"),
    toggleBtn = nav?.querySelector(".toggle-btn");

let isDragging = false;
let dragStartY = 0;
let dragStartTop = 0;
let velocityY = 0;
let animationFrameId;

toggleBtn?.addEventListener("click", () => {
    nav.classList.toggle("open");
});

function startDrag(event) {
    isDragging = true;
    dragStartY = event.clientY;
    dragStartTop = parseInt(window.getComputedStyle(nav).top);
    cancelAnimationFrame(animationFrameId);
}

function drag(event) {
    if (!isDragging) return;
    const dragDistance = event.clientY - dragStartY;
    let newTop = dragStartTop + dragDistance;

    // Limit the top position to prevent dragging beyond the edge of the browser window
    const minTop = 0;
    const maxTop = window.innerHeight - nav.offsetHeight;
    newTop = Math.max(minTop, Math.min(newTop, maxTop));

    nav.style.top = `${newTop}px`;
}

function endDrag() {
    isDragging = false;
    const dragDistance = parseInt(window.getComputedStyle(nav).top) - dragStartTop;
    const timeConstant = 200; // Adjust this value for desired animation speed
    velocityY = dragDistance / timeConstant;
    animateScroll();
}

function animateScroll() {
    const currentTop = parseInt(window.getComputedStyle(nav).top);
    if (Math.abs(velocityY) > 0.1 && currentTop >= 0 && currentTop <= window.innerHeight - nav.offsetHeight) {
        const timeStep = 16; // 60 FPS
        nav.style.top = `${currentTop + velocityY * timeStep}px`;
        velocityY *= 0.95; // Deceleration factor, adjust for desired behavior
        animationFrameId = requestAnimationFrame(animateScroll);
    }
}

nav?.addEventListener("mousedown", startDrag);
window.addEventListener("mousemove", drag);
window.addEventListener("mouseup", endDrag);

nav?.addEventListener("wheel", (event) => {
    event.preventDefault(); // Prevent scrolling the page

    // If Shift key is pressed, allow scrolling the page
    if (event.shiftKey) return;

    const delta = event.deltaY;
    const scrollSpeed = 0.5; // Adjust this value for desired scroll speed
    let newTop = parseInt(window.getComputedStyle(nav).top) - delta * scrollSpeed;

    // Limit the top position to prevent dragging beyond the edge of the browser window
    const minTop = 0;
    const maxTop = window.innerHeight - nav.offsetHeight;
    newTop = Math.max(minTop, Math.min(newTop, maxTop));

    nav.style.top = `${newTop}px`;
});
