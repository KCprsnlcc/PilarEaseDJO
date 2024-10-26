// Constants and variables
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
const statusComposerButton = document.getElementById("statuscomposer");

// Chat variables
const floatingButton = document.getElementById("floatingButton");
const chatPopup = document.getElementById("chatPopup");
const chatBody = document.getElementById("chatBody");
let isDragging = false;
let isOpen = false;
let startX, startY, initialX, initialY;
let lastScrollTop = 0;

// For lazy loading chat history
let chatHistoryPage = 1;
let loadingHistory = false;
let hasMoreHistory = true;

// Scroll to Latest button
const scrollToLatestButton = document.createElement("button");
scrollToLatestButton.id = "scrollToLatestButton";
scrollToLatestButton.innerHTML = '<i class="bx bx-down-arrow-alt"></i>';
scrollToLatestButton.style.display = "none"; // Initially hidden
chatPopup.appendChild(scrollToLatestButton);

scrollToLatestButton.addEventListener("click", () => {
  chatBody.scrollTop = chatBody.scrollHeight;
  scrollToLatestButton.style.display = "none";
});

// Update chat position
function updateChatPosition() {
  const buttonRect = floatingButton.getBoundingClientRect();
  chatPopup.style.bottom = window.innerHeight - buttonRect.bottom + 70 + "px";
  chatPopup.style.right = window.innerWidth - buttonRect.right + 20 + "px";
}

window.addEventListener("resize", updateChatPosition);

// Floating button drag functionality
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
    const dx = e.clientX - startX;
    const dy = e.clientY - startY;
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

// Toggle chat popup
floatingButton.addEventListener("click", function () {
  updateChatPosition();
  if (!isOpen) {
    chatPopup.style.display = "block";
    chatPopup.classList.remove("chatPopOut");
    chatPopup.classList.add("chatPopIn");
    floatingButton.firstElementChild.classList.add("icon-pop-out");
    setTimeout(() => {
      floatingButton.firstElementChild.className = "bx bx-x icon-pop-in";
    }, 300);
    isOpen = true;
    initializeChat();
  } else {
    chatPopup.classList.remove("chatPopIn");
    chatPopup.classList.add("chatPopOut");
    floatingButton.firstElementChild.classList.add("icon-pop-out");
    setTimeout(function () {
      chatPopup.style.display = "none";
      floatingButton.firstElementChild.className = "bx bxs-message icon-pop-in";
    }, 300);
    isOpen = false;
  }
});

// Initialize chat session
function initializeChat() {
  chatBody.innerHTML = ""; // Clear chat body
  chatHistoryPage = 1;
  hasMoreHistory = true;
  loadChatHistory();
}
// Load chat history in batches
function loadChatHistory(scrollToBottom = true) {
  if (loadingHistory || !hasMoreHistory) return;
  loadingHistory = true;

  fetch(`/get_chat_history/?page=${chatHistoryPage}`)
    .then((response) => response.json())
    .then((data) => {
      loadingHistory = false;
      if (data.chat_history && data.chat_history.length > 0) {
        const messages = data.chat_history; // No reverse needed

        if (chatHistoryPage === 1) {
          // Initial load: append messages normally
          messages.forEach((message) => {
            if (message.sender === "user" || message.sender === "bot") {
              generateMessage(message.message, message.sender);
            }
          });
          if (data.chat_history.length < 10) {
            hasMoreHistory = false;
          }
        } else {
          // Prepend older messages
          prependMessages(messages);
          if (data.chat_history.length < 10) {
            hasMoreHistory = false;
          }
        }
        chatHistoryPage++;
      } else {
        hasMoreHistory = false;
      }

      // Check if chat is empty and start session
      if (data.is_chat_empty) {
        startChatSession();
      } else if (
        data.last_message_type === "greeting" &&
        data.total_messages === 1
      ) {
        // If the last message is a greeting and it's the only message, display options
        displayOptions(["Start", "Not Yet"]);
      }

      if (data.awaiting_answer) {
        displayAnswerOptions(data.current_question_index);
      }

      if (scrollToBottom) {
        chatBody.scrollTop = chatBody.scrollHeight;
      }
    })
    .catch((error) => {
      loadingHistory = false;
      console.error("Error fetching chat history:", error);
      // Show error message to the user
      showErrorMessage("Failed to load chat history. Please try again.");
    });
}
// Prepend message to chat body
function prependMessages(messages) {
  messages.forEach((message) => {
    const messageWrapper = document.createElement("div");
    messageWrapper.className = "message-wrapper";

    const messageElement = document.createElement("div");
    messageElement.className =
      message.sender === "user"
        ? "user-message chat-message"
        : "chatbot-message chat-message";
    messageElement.textContent = message.message;

    messageWrapper.appendChild(messageElement);
    chatBody.insertBefore(messageWrapper, chatBody.firstChild);
  });

  // Adjust scroll position to maintain view after prepending
  // (Optional: Implement smooth scrolling if desired)
}

// Start chat session
function startChatSession() {
  fetch("/start_chat/")
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.message) {
        simulateTyping(data.message, "bot", () => {
          if (data.options && data.options.length > 0) {
            displayOptions(data.options);
          }
        });
      }
    })
    .catch((error) => {
      console.error("Error starting chat session:", error);
      showErrorMessage("Failed to start chat session. Please try again.");
    });
}
// Display options (e.g., Start, Not Yet)
function displayOptions(options) {
  const optionsWrapper = document.createElement("div");
  optionsWrapper.className = "message-wrapper options-wrapper pop-up";
  optionsWrapper.id = "dialogOptions";

  options.forEach((option) => {
    const button = document.createElement("button");
    button.className = "option-button";
    button.textContent = option;
    button.onclick = function () {
      autoSendMessage(option, optionsWrapper);
    };
    optionsWrapper.appendChild(button);
  });

  chatBody.appendChild(optionsWrapper);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Auto-send message (for options)
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

// Send message function
function sendMessage() {
  const chatInput = document.getElementById("chatInput");
  const messageText = chatInput.value.trim();

  if (messageText === "") return;

  generateMessage(messageText, "user");
  chatInput.value = ""; // Clear input field

  // Send message to the server
  fetch("/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      message: messageText,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        handleBotResponse(data);
      } else {
        showErrorMessage(data.error);
      }
    })
    .catch((error) => {
      console.error("Error sending message:", error);
      showErrorMessage("Failed to send message. Please try again.");
    });
}

// Handle bot response
function handleBotResponse(data) {
  if (data.message) {
    simulateTyping(data.message, "bot");
  }
  if (data.question_index !== undefined) {
    setTimeout(() => {
      displayQuestion(data.question_index);
    }, 1000); // Delay before displaying the question
  }
  if (data.end_of_questions) {
    simulateTyping(
      "Thank you for completing the questionnaire! Would you like to talk to a counselor?",
      "bot",
      () => {
        displayFinalOptions();
      }
    );
  }
}

// Generate chat message
function generateMessage(text, sender) {
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
}
// Simulate typing with delay
function simulateTyping(text, sender, callback = null) {
  showLoader(chatBody);
  const typingDelay = Math.max(500, text.length * 30); // Reduced delay

  setTimeout(() => {
    removeLoader(chatBody);
    generateMessage(text, sender);
    if (callback) callback();
  }, typingDelay);
}

// Show loader animation
function showLoader(chatBody) {
  const loaderElement = document.createElement("div");
  loaderElement.className = "loader";
  loaderElement.innerHTML =
    '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  chatBody.appendChild(loaderElement);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Remove loader animation
function removeLoader(chatBody) {
  const loaderElement = chatBody.querySelector(".loader");
  if (loaderElement) {
    chatBody.removeChild(loaderElement);
  }
}

// Display question
function displayQuestion(questionIndex) {
  fetch(`/get_question/${questionIndex}/`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        simulateTyping(data.question, "bot", () => {
          displayAnswerOptions(questionIndex);
        });
      } else {
        showErrorMessage(data.error);
      }
    })
    .catch((error) => {
      console.error("Error fetching question:", error);
      showErrorMessage("Failed to load question. Please try again.");
    });
}
// Display answer options
function displayAnswerOptions(questionIndex) {
  fetch(`/get_answer_options/${questionIndex}/`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const answersWrapper = document.createElement("div");
        answersWrapper.className = "message-wrapper answers-wrapper";
        answersWrapper.id = "answersWrapper"; // Assign ID to remove later

        data.answer_options.forEach((answerText) => {
          const answerButton = document.createElement("button");
          answerButton.className = "answers-button";
          answerButton.textContent = answerText;
          answerButton.onclick = function () {
            handleAnswerSelection(questionIndex, answerText);
          };
          answersWrapper.appendChild(answerButton);
        });

        chatBody.appendChild(answersWrapper);
        chatBody.scrollTop = chatBody.scrollHeight;
      } else {
        showErrorMessage(data.error);
      }
    })
    .catch((error) => {
      console.error("Error fetching answer options:", error);
      showErrorMessage("Failed to load answer options. Please try again.");
    });
}

// Handle answer selection
function handleAnswerSelection(questionIndex, answerText) {
  const answersWrapper = document.getElementById("answersWrapper");

  if (answersWrapper) {
    answersWrapper.classList.remove("pop-up");
    answersWrapper.classList.add("pop-down");
    setTimeout(() => answersWrapper.remove(), 300);
  }

  generateMessage(answerText, "user");

  fetch("/submit_answer/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      question_index: questionIndex,
      answer_text: answerText,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        simulateTyping(data.response, "bot", () => {
          if (
            data.next_question_index !== undefined &&
            data.next_question_index !== null
          ) {
            setTimeout(() => {
              displayQuestion(data.next_question_index);
            }, 1000);
          } else if (data.end_of_questions) {
            simulateTyping(
              "Thank you for completing the questionnaire! Would you like to talk to a counselor?",
              "bot",
              () => {
                displayFinalOptions();
              }
            );
          }
        });
      } else {
        showErrorMessage(data.error);
      }
    })
    .catch((error) => {
      console.error("Error submitting answer:", error);
      showErrorMessage("Failed to submit answer. Please try again.");
    });
}
// Display final options after questionnaire
function displayFinalOptions() {
  const optionsWrapper = document.createElement("div");
  optionsWrapper.className = "message-wrapper options-wrapper pop-up";
  optionsWrapper.id = "finalOptions";

  const options = ["Yes", "No"];
  options.forEach((option) => {
    const button = document.createElement("button");
    button.className = "option-button";
    button.textContent = option;
    button.onclick = function () {
      handleFinalOptionSelection(option, optionsWrapper);
    };
    optionsWrapper.appendChild(button);
  });

  chatBody.appendChild(optionsWrapper);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Handle final option selection
function handleFinalOptionSelection(selection, optionsWrapper) {
  optionsWrapper.classList.remove("pop-up");
  optionsWrapper.classList.add("pop-down");

  setTimeout(() => {
    optionsWrapper.remove();
    generateMessage(selection, "user");

    fetch("/final_option_selection/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        selection: selection,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          simulateTyping(data.message, "bot");
        } else {
          showErrorMessage(data.error);
        }
      })
      .catch((error) => {
        console.error("Error submitting final selection:", error);
        showErrorMessage("Failed to submit your choice. Please try again.");
      });
  }, 300);
}

// Show error message
function showErrorMessage(errorText) {
  const errorWrapper = document.createElement("div");
  errorWrapper.className = "message-wrapper";

  const errorElement = document.createElement("div");
  errorElement.className = "error-message chat-message";
  errorElement.textContent = errorText;

  errorWrapper.appendChild(errorElement);
  chatBody.appendChild(errorWrapper);

  chatBody.scrollTop = chatBody.scrollHeight;
}

// Get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      // Fixed the loop condition
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Initialize chat position
document.addEventListener("DOMContentLoaded", updateChatPosition);

// Accessibility: Keyboard navigation for chat input
document.getElementById("chatInput").addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Scroll detection for "Scroll to Latest" button and lazy loading
chatBody.addEventListener("scroll", function () {
  const scrollTop = chatBody.scrollTop;
  const scrollHeight = chatBody.scrollHeight;
  const clientHeight = chatBody.clientHeight;

  if (scrollTop < 100 && !loadingHistory && hasMoreHistory) {
    // Load more messages when scrolled to top
    loadChatHistory(false);
  }

  if (scrollTop < scrollHeight - clientHeight - 100) {
    // User scrolled up more than 100px
    scrollToLatestButton.style.display = "block";
  } else {
    scrollToLatestButton.style.display = "none";
  }
});

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
