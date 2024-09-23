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
// Variable to control floating button and chat popup behavior
var floatingButton = document.getElementById("floatingButton");
var chatPopup = document.getElementById("chatPopup");
var isDragging = false;
var isOpen = false;
var startX, startY, initialX, initialY;
var chatSessionChanged = false; // New variable to track session changes

// Variables for chat management
let lastMessageTime = null;
let greetingDisplayed = false;
let currentQuestionIndex = -1;
let sessionData = [];
let sessionId = null;
let savingInProgress = false; // New flag to prevent duplicate saves

// Function to update chat position relative to the floating button
function updateChatPosition() {
  var buttonRect = floatingButton.getBoundingClientRect();
  chatPopup.style.bottom = window.innerHeight - buttonRect.bottom + 70 + "px";
  chatPopup.style.right = window.innerWidth - buttonRect.right + 20 + "px";
}

// Event listener to update chat position when window resizes
window.addEventListener("resize", updateChatPosition);

// Function to handle the drag event for the floating button
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

// Function to toggle the chat popup and load the session
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

    // Load session if it hasn't been loaded yet
    if (!sessionId) {
      loadChatSession().then(() => {
        if (!greetingDisplayed && sessionData.length === 0) {
          displayGreeting();
        } else {
          restoreSession();
        }
      });
    }
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

// Function to load and restore chat session data
function loadChatSession() {
  return fetch("/load_chat_session/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.session_data) {
        sessionData = data.session_data;
        sessionId = data.session_id;
        renderChatSession(sessionData); // Render the restored session
      }
    });
}

// Function to restore a chat session from the saved session data
function restoreSession() {
  const chatBody = document.getElementById("chatBody");
  sessionData.forEach((message) => {
    if (message.sender === "timestamp") {
      addTimestamp(chatBody, message.text);
    } else {
      generateMessage(message.text, message.sender);
      if (message.sender === "bot" && message.questionIndex !== -1) {
        currentQuestionIndex = message.questionIndex;
      }
    }
  });
  checkLatestMessageType(); // Ensure options are shown correctly after restoring session
}

// Function to generate chat messages and append them to the chat body
function generateMessage(text, sender) {
  const chatBody = document.getElementById("chatBody");

  const messageWrapper = document.createElement("div");
  messageWrapper.className = "message-wrapper";

  const messageElement = document.createElement("div");
  messageElement.className =
    sender === "user"
      ? "user-message chat-message"
      : "chatbot-message chat-message";
  messageElement.textContent = text;

  messageWrapper.appendChild(messageElement);
  chatBody.appendChild(messageWrapper);

  chatBody.scrollTop = chatBody.scrollHeight;

  // Track session data only if it changes
  if (!savingInProgress) {
    sessionData.push({
      text: text,
      sender: sender,
      timestamp: new Date().toISOString(),
      questionIndex: currentQuestionIndex,
    });
    chatSessionChanged = true; // Mark session as changed
  }
}

// Function to save chat session data (with prevention of multiple saves)
function saveSession() {
  if (!chatSessionChanged || savingInProgress) return; // Save only if there's a change
  savingInProgress = true; // Prevent further saves while in progress

  fetch("/save_chat_session/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      session_data: sessionData,
    }),
  })
    .then(() => {
      chatSessionChanged = false; // Reset change tracker
    })
    .finally(() => {
      savingInProgress = false; // Allow saving again after completion
    });
}

// Function to display greeting if the chat is opened for the first time
function displayGreeting() {
  const chatBody = document.getElementById("chatBody");
  showLoader(chatBody);
  setTimeout(function () {
    removeLoader(chatBody);
    addTimestampIfNeeded(chatBody);
    generateMessage(
      "Hello! Welcome to Piracle, your emotional support companion. How can I assist you today? Should we start?",
      "bot"
    );
    setTimeout(displayOptions, 500);
    greetingDisplayed = true;
  }, 1500);
}

// Function to display options for the user to start or delay interaction
function displayOptions() {
  const chatBody = document.getElementById("chatBody");
  if (!document.getElementById("dialogOptions")) {
    const optionsWrapper = document.createElement("div");
    optionsWrapper.className = "message-wrapper options-wrapper pop-up";
    optionsWrapper.id = "dialogOptions";

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

    chatBody.scrollTop = chatBody.scrollHeight;
  }
}

// Function to handle automatic message sending
function autoSendMessage(message, optionsWrapper) {
  optionsWrapper.classList.remove("pop-up");
  optionsWrapper.classList.add("pop-down");

  setTimeout(() => {
    optionsWrapper.remove();
    const chatInput = document.getElementById("chatInput");
    chatInput.value = message;
    sendMessage();
  }, 300);
}

// Function to handle user message sending
function sendMessage() {
  const chatInput = document.getElementById("chatInput");
  const chatBody = document.getElementById("chatBody");
  const messageText = chatInput.value;

  if (messageText.trim() !== "") {
    generateMessage(messageText, "user");
    if (messageText.toLowerCase() === "start") {
      setTimeout(() => {
        showLoader(chatBody);
        setTimeout(() => {
          removeLoader(chatBody);
          displayQuestion(0); // Start the questionnaire from the first question
        }, 1500);
      }, 1000);
    } else if (messageText.toLowerCase() === "not yet") {
      setTimeout(() => {
        generateMessage("No worries, take your time.", "bot");
      }, 1000);
    }
  }
  chatInput.value = ""; // Clear the input field after sending
}

// Function to start displaying questions for the questionnaire
function startQuestionnaire() {
  setTimeout(() => {
    showLoader(document.getElementById("chatBody"));
    setTimeout(() => {
      removeLoader(document.getElementById("chatBody"));
      displayQuestion(0);
    }, 1500);
  }, 1000);
}

// Check and handle answers for the given message text
function checkAndHandleAnswer(messageText) {
  const answers = [
    "Managing multiple assignments and deadlines.",
    "Understanding difficult subjects or topics.",
    "Balancing academics with extracurricular activities.",
    // Add more predefined answers here as needed
  ];

  const answerIndex = answers.findIndex(
    (answer) => answer.toLowerCase() === messageText.toLowerCase()
  );

  if (answerIndex !== -1 && currentQuestionIndex !== -1) {
    handleAnswerSelection(
      currentQuestionIndex,
      answerIndex,
      answers[answerIndex]
    );
  }
}

// Helper function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Call this function to save the session when chat data changes
window.addEventListener("beforeunload", saveSession);

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
