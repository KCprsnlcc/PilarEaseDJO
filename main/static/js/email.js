document.addEventListener("DOMContentLoaded", function () {
  // List of random tips
  const tips = [
    "Keep your contact information up to date for smooth communication.",
    "Ensure your email is verified to receive notifications.",
    "Use a strong password for your account security.",
    "Avoid sharing sensitive information online.",
    "Update your profile regularly to stay connected.",
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