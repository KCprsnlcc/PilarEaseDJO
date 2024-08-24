// Script for dropdown menu
const burger = document.getElementById("burger");
const dropdown = document.querySelector(".dropdown");
const profileLink = document.getElementById("profileLink");
const profileModal = document.getElementById("profileModal");
const closeProfileModal = document.getElementById("closeProfileModal");
const avatarLink = document.getElementById("avatarLink");
const avatarModal = document.getElementById("avatarModal");
const closeAvatarModal = document.getElementById("closeAvatarModal");
const passwordLink = document.getElementById("passwordLink");
const passwordModal = document.getElementById("passwordModal");
const closePasswordModal = document.getElementById("closePasswordModal");
const statusModal = document.getElementById("statusModal");
const statusModalOverlay = document.getElementById("statusModalOverlay");
const closeStatusModal = document.getElementById("closeStatusModal");
const descriptionDiv = document.getElementById("description");
var statusComposerButton = document.getElementById("statuscomposer");

var floatingButton = document.getElementById("floatingButton");
var chatPopup = document.getElementById("chatPopup");
var isDragging = false;
var isOpen = false;
var startX, startY, initialX, initialY;

function updateChatPosition() {
  var buttonRect = floatingButton.getBoundingClientRect();
  chatPopup.style.bottom = window.innerHeight - buttonRect.bottom + 70 + "px";
  chatPopup.style.right = window.innerWidth - buttonRect.right + 20 + "px";
}

window.addEventListener("resize", updateChatPosition);

floatingButton.addEventListener("mousedown", function (e) {
  isDragging = true;
  startX = e.clientX;
  startY = e.clientY;
  initialX = floatingButton.offsetLeft;
  initialY = floatingButton.offsetTop;
  document.addEventListener("mousemove", onMouseMove);
  document.addEventListener("mouseup", onMouseUp);
  floatingButton.style.animation = "drag 0.5s infinite";
});

function onMouseMove(e) {
  if (isDragging) {
    var dx = e.clientX - startX;
    var dy = e.clientY - startY;
    floatingButton.style.left = initialX + dx + "px";
    floatingButton.style.top = initialY + dy + "px";
    updateChatPosition();
  }
}

function onMouseUp() {
  isDragging = false;
  document.removeEventListener("mousemove", onMouseMove);
  document.removeEventListener("mouseup", onMouseUp);
  floatingButton.style.animation = "float 3s ease-in-out infinite";
}

floatingButton.addEventListener("click", function () {
  updateChatPosition(); // Update position before showing
  if (!isOpen) {
    chatPopup.style.display = "block";
    chatPopup.classList.remove("chatPopOut");
    chatPopup.classList.add("chatPopIn");
    floatingButton.firstElementChild.classList.add("icon-pop-out");
    setTimeout(() => {
      floatingButton.firstElementChild.className = "bx bx-x icon-pop-in";
    }, 300);
    isOpen = true;
  } else {
    chatPopup.classList.remove("chatPopIn");
    chatPopup.classList.add("chatPopOut");
    floatingButton.firstElementChild.classList.add("icon-pop-out");
    setTimeout(function () {
      chatPopup.style.display = "none";
      floatingButton.firstElementChild.className = "bx bxs-message icon-pop-in";
    }, 300); // Match the animation duration
    isOpen = false;
  }
});
let lastMessageTime = null;
let greetingDisplayed = false; // Flag to track if the greeting has been displayed

document
  .getElementById("floatingButton")
  .addEventListener("click", function () {
    // Show the chat popup
    document.getElementById("chatPopup").style.display = "block";

    const chatBody = document.getElementById("chatBody");

    // If the greeting has already been displayed, skip the greeting
    if (!greetingDisplayed) {
      // Show the loader
      const loaderElement = document.createElement("div");
      loaderElement.className = "loader";
      loaderElement.innerHTML =
        '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
      chatBody.appendChild(loaderElement);
      chatBody.scrollTop = chatBody.scrollHeight;

      // Simulate a delay before showing the initial message
      setTimeout(function () {
        chatBody.removeChild(loaderElement); // Remove the loader

        // Display the initial greeting message from Piracle
        const botMessageWrapper = document.createElement("div");
        botMessageWrapper.className = "message-wrapper";

        const botMessageElement = document.createElement("div");
        botMessageElement.className = "chatbot-message chat-message";
        botMessageElement.textContent =
          "Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?";

        // Check if timestamp should be added for the first message
        addTimestampIfNeeded(chatBody);

        botMessageWrapper.appendChild(botMessageElement);
        chatBody.appendChild(botMessageWrapper);

        chatBody.scrollTop = chatBody.scrollHeight;

        // Delay before displaying the options
        setTimeout(displayOptions, 500); // Adjust delay as needed

        // Set the greetingDisplayed flag to true
        greetingDisplayed = true;
      }, 1500); // Delay for loader
    }
  });

function displayOptions() {
  const chatBody = document.getElementById("chatBody");

  // Add options for "Start" and "Not Yet"
  const optionsWrapper = document.createElement("div");
  optionsWrapper.className = "message-wrapper options-wrapper pop-up";
  optionsWrapper.id = "dialogOptions"; // Assign an ID to the options wrapper

  const startButton = document.createElement("button");
  startButton.className = "option-button";
  startButton.textContent = "Start";
  startButton.onclick = function () {
    autoSendMessage("Start", optionsWrapper);
  };

  const notYetButton = document.createElement("button");
  notYetButton.className = "option-button";
  notYetButton.textContent = "Not Yet";
  notYetButton.onclick = function () {
    autoSendMessage("Not Yet", optionsWrapper);
  };

  optionsWrapper.appendChild(startButton);
  optionsWrapper.appendChild(notYetButton);
  chatBody.appendChild(optionsWrapper);

  chatBody.scrollTop = chatBody.scrollHeight; // Scroll to the bottom
}

function autoSendMessage(message, optionsWrapper) {
  // Add pop-down animation before removing the options
  optionsWrapper.classList.remove("pop-up");
  optionsWrapper.classList.add("pop-down");

  setTimeout(() => {
    optionsWrapper.remove(); // Remove the options after the animation
    const chatInput = document.getElementById("chatInput");
    chatInput.value = message; // Set the input value
    sendMessage(); // Automatically send the message
  }, 300); // Delay matches the pop-down animation duration
}

function sendMessage() {
  const chatInput = document.getElementById("chatInput");
  const chatBody = document.getElementById("chatBody");
  const messageText = chatInput.value;

  // Remove the dialog options if they exist
  const optionsWrapper = document.getElementById("dialogOptions");
  if (optionsWrapper) {
    optionsWrapper.classList.remove("pop-up");
    optionsWrapper.classList.add("pop-down");
    setTimeout(() => optionsWrapper.remove(), 300); // Delay for the pop-down animation
  }

  if (messageText.trim() !== "") {
    // Check if timestamp should be added for the user's message
    addTimestampIfNeeded(chatBody);

    const messageWrapper = document.createElement("div");
    messageWrapper.className = "message-wrapper";

    const messageElement = document.createElement("div");
    messageElement.className = "user-message chat-message";
    messageElement.textContent = messageText;

    messageWrapper.appendChild(messageElement);
    chatBody.appendChild(messageWrapper);

    chatInput.value = "";
    chatBody.scrollTop = chatBody.scrollHeight;

    if (messageText.toLowerCase() === "start") {
      // Logic for starting the conversation or any specific action
      setTimeout(() => {
        generateChatbotResponse("Great! Let's begin.");
      }, 1000);
    } else if (messageText.toLowerCase() === "not yet") {
      setTimeout(() => {
        generateChatbotResponse("No worries, take your time.");
      }, 1000);
    }
  }
}

function generateChatbotResponse(responseText) {
  const chatBody = document.getElementById("chatBody");

  const loaderElement = document.createElement("div");
  loaderElement.className = "loader";
  loaderElement.innerHTML =
    '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  chatBody.appendChild(loaderElement);
  chatBody.scrollTop = chatBody.scrollHeight;

  setTimeout(function () {
    chatBody.removeChild(loaderElement); // Remove the loader

    // Check if timestamp should be added for the chatbot's response
    addTimestampIfNeeded(chatBody);

    const botMessageWrapper = document.createElement("div");
    botMessageWrapper.className = "message-wrapper";

    const botMessageElement = document.createElement("div");
    botMessageElement.className = "chatbot-message chat-message";
    botMessageElement.textContent = responseText;

    botMessageWrapper.appendChild(botMessageElement);
    chatBody.appendChild(botMessageWrapper);

    chatBody.scrollTop = chatBody.scrollHeight;
  }, 2000); // Adjust the delay time as necessary to simulate the chatbot typing
}

function addTimestampIfNeeded(chatBody) {
  const currentTime = new Date();

  // Check if it's the first message or more than 5 minutes have passed since the last message
  if (!lastMessageTime || currentTime - lastMessageTime > 300000) {
    // Add timestamp
    const sessionTimestamp = document.createElement("div");
    sessionTimestamp.className = "session-timestamp";
    sessionTimestamp.textContent = getCurrentTime();
    chatBody.appendChild(sessionTimestamp);
  }

  // Update the last message time
  lastMessageTime = currentTime;
}

function getCurrentTime() {
  const now = new Date();
  let hours = now.getHours();
  const minutes = now.getMinutes();
  const ampm = hours >= 12 ? "PM" : "AM";

  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  const strMinutes = minutes < 10 ? "0" + minutes : minutes;
  const strTime = hours + ":" + strMinutes + " " + ampm;

  return strTime;
}

document.addEventListener("DOMContentLoaded", updateChatPosition);

if (statusComposerButton) {
  // Show the modal with pop-in animation
  statusComposerButton.addEventListener("click", function () {
    statusModal.style.display = "block";
    statusModalOverlay.style.display = "block";
    setTimeout(() => {
      statusModal.classList.add("pop-in");
      statusModalOverlay.classList.add("pop-in");
    }, 10);
  });
}

// Close the modal with pop-out animation
closeStatusModal.addEventListener("click", function () {
  closeModal();
});

statusModalOverlay.addEventListener("click", function () {
  closeModal();
});

function closeModal() {
  statusModal.classList.remove("pop-in");
  statusModal.classList.add("pop-out");
  statusModalOverlay.classList.remove("pop-in");
  statusModalOverlay.classList.add("pop-out");
  setTimeout(() => {
    statusModal.style.display = "none";
    statusModal.classList.remove("pop-out");
    statusModalOverlay.style.display = "none";
    statusModalOverlay.classList.remove("pop-out");
  }, 300);
}

// Placeholder functionality
function showPlaceholder() {
  if (!descriptionDiv.textContent.trim().length) {
    descriptionDiv.classList.add("placeholder");
    descriptionDiv.textContent = descriptionDiv.getAttribute("placeholder");
  }
}

function hidePlaceholder() {
  if (descriptionDiv.classList.contains("placeholder")) {
    descriptionDiv.classList.remove("placeholder");
    descriptionDiv.textContent = "";
  }
}

descriptionDiv.addEventListener("focus", hidePlaceholder);
descriptionDiv.addEventListener("blur", showPlaceholder);

// Initial placeholder display
showPlaceholder();

// Feeling icons selection
const feelingIcons = document.querySelectorAll(".feeling-icon");
feelingIcons.forEach((icon) => {
  icon.addEventListener("click", () => {
    feelingIcons.forEach((i) => i.classList.remove("active"));
    icon.classList.add("active");
  });
});

// Text formatting
window.formatText = function (command, value = null) {
  document.execCommand(command, false, value);
};

// Function to close currently open modal
function closeCurrentModal() {
  const modals = document.querySelectorAll(".modal-content");
  modals.forEach((modal) => {
    if (modal.style.display === "block") {
      modal.classList.add("slide-upSolid");
      modal.classList.remove("slide-downSolid");
    }
  });
}

// Listen for the end of the slide-up animation to hide the modal
document.querySelectorAll(".modal-content").forEach((modal) => {
  modal.addEventListener("animationend", (event) => {
    if (event.animationName === "slideUpSolid") {
      modal.style.display = "none";
    }
  });
});
// Show profile modal when profile link is clicked
profileLink.addEventListener("click", (e) => {
  e.preventDefault();
  closeCurrentModal();
  profileModal.style.display = "block";
  profileModal.classList.add("slide-downSolid");
  profileModal.classList.remove("slide-upSolid");
  fetchUserProfile(); // Fetch and populate user data when the modal is opened
});
burger.addEventListener("change", () => {
  if (burger.checked) {
    dropdown.classList.add("slide-down");
    dropdown.classList.remove("slide-up");
    dropdown.style.display = "block";
  } else {
    dropdown.classList.add("slide-up");
    dropdown.classList.remove("slide-down");
  }
});

dropdown.addEventListener("animationend", (event) => {
  if (event.animationName === "slideUp") {
    dropdown.style.display = "none";
  }
});

// Close dropdown menu when any link is clicked
document.querySelectorAll(".dropdown a").forEach((link) => {
  link.addEventListener("click", () => {
    burger.checked = false;
    dropdown.classList.add("slide-up");
    dropdown.classList.remove("slide-down");
  });
});

// Show profile modal when profile link is clicked
profileLink.addEventListener("click", (e) => {
  e.preventDefault();
  closeCurrentModal();
  profileModal.style.display = "block";
  profileModal.classList.add("slide-downSolid");
  profileModal.classList.remove("slide-upSolid");
});

// Close profile modal when the close button is clicked
closeProfileModal.addEventListener("click", () => {
  profileModal.classList.add("slide-upSolid");
  profileModal.classList.remove("slide-downSolid");
});

// Show avatar modal when avatar link is clicked
avatarLink.addEventListener("click", (e) => {
  e.preventDefault();
  closeCurrentModal();
  avatarModal.style.display = "block";
  avatarModal.classList.add("slide-downSolid");
  avatarModal.classList.remove("slide-upSolid");
});

// Close avatar modal when the close button is clicked
closeAvatarModal.addEventListener("click", () => {
  avatarModal.classList.add("slide-upSolid");
  avatarModal.classList.remove("slide-downSolid");
});

// Show password modal when password link is clicked
passwordLink.addEventListener("click", (e) => {
  e.preventDefault();
  closeCurrentModal();
  passwordModal.style.display = "block";
  passwordModal.classList.add("slide-downSolid");
  passwordModal.classList.remove("slide-upSolid");
});

// Close password modal when the close button is clicked
closePasswordModal.addEventListener("click", () => {
  passwordModal.classList.add("slide-upSolid");
  passwordModal.classList.remove("slide-downSolid");
});
