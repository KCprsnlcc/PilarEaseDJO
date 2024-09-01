document.addEventListener("DOMContentLoaded", function () {
  // List of random tips
  const tips = [
    "Use a combination of letters, numbers, and special characters for a strong password.",
    "Avoid using the same password for multiple accounts.",
    "Consider using a password manager to store and manage your passwords securely.",
    "Change your passwords regularly, especially for sensitive accounts.",
    "Never share your passwords with anyone.",
  ];

  // Function to display a random tip with pop-in animation
  function displayRandomTip() {
    const randomIndex = Math.floor(Math.random() * tips.length);
    const randomTipElement = document.getElementById("randomTip");
    randomTipElement.classList.remove("pop-in");

    // Delay the text change slightly to ensure animation restarts smoothly
    setTimeout(() => {
      randomTipElement.innerText = `Tip: ${tips[randomIndex]}`;
      randomTipElement.classList.add("pop-in");
    }, 10); // A small delay to trigger the reflow and restart animation
  }

  // Set interval to change the tip every 3 seconds
  setInterval(displayRandomTip, 3000);
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
});
document
  .getElementById("resetPasswordForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const newPassword = document.querySelector(
      'input[name="new_password"]'
    ).value;
    const confirmPassword = document.querySelector(
      'input[name="new_password_confirm"]'
    ).value;
    const submitButton = document.querySelector(".btn");
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    // Validate that the passwords match
    if (newPassword !== confirmPassword) {
      showResetPasswordError("Passwords do not match.");
      return;
    }

    // Validate password strength
    const passwordStrengthRegex =
      /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!passwordStrengthRegex.test(newPassword)) {
      showResetPasswordError(
        "Password must be at least 8 characters long, contain both uppercase and lowercase letters, include at least one numeric digit, and one special character."
      );
      return;
    }

    // Show the loader
    showResetPassLoader();

    // Disable the button
    submitButton.disabled = true;

    fetch(window.location.href, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": csrfToken,
      },
      body: new URLSearchParams({
        new_password: newPassword,
        new_password_confirm: confirmPassword,
      }),
    })
      .then((response) => {
        if (response.ok) {
          // Transition to the password reset complete page with smooth animation
          smoothTransitionToCompletePage();
        } else {
          return response.text().then((text) => {
            hideResetPassLoader();
            showResetPasswordError("An error occurred. Please try again.");
            submitButton.disabled = false;
          });
        }
      })
      .catch((error) => {
        hideResetPassLoader(); // Ensure loader is hidden on error
        console.error("Error:", error);
        showResetPasswordError("An error occurred. Please try again later.");
        submitButton.disabled = false;
      });
  });

function showResetPassLoader() {
  document.getElementById("resetpassOverlay").style.display = "block";
}

function hideResetPassLoader() {
  document.getElementById("resetpassOverlay").style.display = "none";
}

function showResetPasswordError(message) {
  const errorBox = document.getElementById("resetPasswordErrorBox");
  document.getElementById("resetPasswordErrorContent").innerText = message;
  errorBox.classList.remove("pop-out");
  errorBox.classList.add("pop-in");
  errorBox.style.display = "block";

  setTimeout(() => {
    errorBox.classList.remove("pop-in");
    errorBox.classList.add("pop-out");

    // Hide the dialog after the animation is done
    setTimeout(() => {
      errorBox.style.display = "none";
      errorBox.classList.remove("pop-in", "pop-out");
    }, 300);
  }, 3000);
}

function smoothTransitionToCompletePage() {
  const resetContainer = document.getElementById("reset-container");
  resetContainer.classList.add("fade-out");

  setTimeout(() => {
    window.location.href = "/reset/done/"; // Redirect to the complete page
  }, 600); // Match this with CSS transition duration
}
