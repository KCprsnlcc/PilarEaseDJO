document.addEventListener("DOMContentLoaded", function () {
  const tips = [
    "Keep your contact information up to date for smooth communication.",
    "Ensure your email is verified to receive notifications.",
    "Use a strong password for your account security.",
    "Avoid sharing sensitive information online.",
    "Update your profile regularly to stay connected.",
  ];

  function displayRandomTip() {
    const randomIndex = Math.floor(Math.random() * tips.length);
    const randomTipElement = document.getElementById("randomTip");
    randomTipElement.classList.remove("pop-in");

    setTimeout(() => {
      randomTipElement.innerText = `Tip: ${tips[randomIndex]}`;
      randomTipElement.classList.add("pop-in");
    }, 10);
  }

  setInterval(displayRandomTip, 5000); // Update tip every 5 seconds
});
