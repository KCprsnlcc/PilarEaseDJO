// main/static/js/admin_login.js

document.addEventListener("DOMContentLoaded", function () {
  // Randomize SVG Paths for Curved Lines
  document.querySelectorAll(".curved-line path").forEach(function (path) {
    var controlPointX1 = Math.random() * 50;
    var controlPointY1 = Math.random() * 50;
    var controlPointX2 = 100 - Math.random() * 50;
    var controlPointY2 = Math.random() * 50;
    var endPointX = Math.random() * 100;
    var endPointY = Math.random() * 100;
    var d = `M0,0 C${controlPointX1},${controlPointY1} ${controlPointX2},${controlPointY2} ${endPointX},${endPointY}`;
    path.setAttribute("d", d);
  });

  const loginForm = document.getElementById("adminLoginForm");
  const errorElement = document.querySelector(".error");
  const loginContainer = document.querySelector(".login-container");

  // Form Submission Validation
  loginForm.addEventListener("submit", function (event) {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    // Clear previous errors
    if (errorElement) {
      errorElement.textContent = "";
      errorElement.style.display = "none";
    }

    let hasError = false;
    let errorMessage = "";

    // Simple client-side validation
    if (username === "") {
      hasError = true;
      errorMessage = "Username is required.";
    } else if (password === "") {
      hasError = true;
      errorMessage = "Password is required.";
    }

    if (hasError) {
      event.preventDefault();
      if (errorElement) {
        errorElement.textContent = errorMessage;
        errorElement.style.display = "block";
        errorElement.style.animation = "fadeIn 0.5s";
      }
    }
  });

  /* 3D Tilt Effect Implementation */
  loginContainer.addEventListener("mousemove", function (e) {
    const rect = loginContainer.getBoundingClientRect();
    const x = e.clientX - rect.left; // X position within the container
    const y = e.clientY - rect.top; // Y position within the container

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const deltaX = (x - centerX) / centerX;
    const deltaY = (y - centerY) / centerY;

    const rotateX = deltaY * 10; // Max rotation of 10 degrees
    const rotateY = -deltaX * 10;

    loginContainer.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-5px)`;
    loginContainer.classList.add("hovered");
  });

  loginContainer.addEventListener("mouseleave", function () {
    loginContainer.style.transform =
      "rotateX(0deg) rotateY(0deg) translateY(-5px)";
    loginContainer.classList.remove("hovered");
  });
});
