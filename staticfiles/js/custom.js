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
const chatInput = document.getElementById("chatInput");
const sendButton = chatPopup.querySelector(".chat-input button");
let scrollToLatestButton = document.getElementById("scrollToLatestButton");

// Chat state variables
let isDragging = false;
let isOpen = false;
let startX, startY, initialX, initialY;
let lastScrollTop = 0;

// For lazy loading chat history
let chatHistoryPage = 1; // Start with the first page
let loadingHistory = false;
let hasMoreHistory = true;

// Additional chat state variables
let questionnaireStarted = false;
let currentQuestionIndex = null;

// Initialize chat on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  initializeChat();
  updateChatPosition();

  // Check and display stored error messages
  const chatError = sessionStorage.getItem("chatError");
  if (chatError) {
    showErrorMessage(chatError);
    sessionStorage.removeItem("chatError"); // Clear the error after displaying
  }
});

// Scroll to Latest button creation and event listener
if (!scrollToLatestButton) {
  const newScrollToLatestButton = document.createElement("button");
  newScrollToLatestButton.id = "scrollToLatestButton";
  newScrollToLatestButton.innerHTML = '<i class="bx bx-down-arrow-alt"></i>';
  newScrollToLatestButton.style.display = "none"; // Initially hidden
  chatPopup.appendChild(newScrollToLatestButton);

  newScrollToLatestButton.addEventListener("click", () => {
    chatBody.scrollTop = chatBody.scrollHeight;
    newScrollToLatestButton.style.display = "none";
  });
}

// Update chat position based on window size
function updateChatPosition() {
  const buttonRect = floatingButton.getBoundingClientRect();
  chatPopup.style.bottom = window.innerHeight - buttonRect.bottom + 70 + "px";
  chatPopup.style.right = window.innerWidth - buttonRect.right + 20 + "px";
}

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

// Toggle chat popup on floating button click
floatingButton.addEventListener("click", function () {
  updateChatPosition();
  if (!isOpen) {
    openChat();
  } else {
    closeChat();
  }
});
function openChat() {
  chatPopup.style.display = "block";
  chatPopup.classList.remove("chatPopOut");
  chatPopup.classList.add("chatPopIn");
  floatingButton.firstElementChild.classList.add("icon-pop-out");

  // Scroll to the bottom to show the latest message
  chatBody.scrollTop = chatBody.scrollHeight;

  setTimeout(() => {
    floatingButton.firstElementChild.className = "bx bx-x icon-pop-in";
  }, 300);
  isOpen = true;

  // Remove automatic initiation of chat session
  // Only initiate when user clicks "Start"
  // if (!questionnaireStarted) {
  //   startChatSession(); // Initiate chat session
  // }
}

// Function to close chat popup
function closeChat() {
  chatPopup.classList.remove("chatPopIn");
  chatPopup.classList.add("chatPopOut");
  floatingButton.firstElementChild.classList.add("icon-pop-out");
  setTimeout(function () {
    chatPopup.style.display = "none";
    floatingButton.firstElementChild.className = "bx bxs-message icon-pop-in";
  }, 300);
  isOpen = false;
}

// Function to initialize chat session
function initializeChat() {
  chatBody.innerHTML = ""; // Clear chat body
  chatHistoryPage = 1; // Reset to first page
  hasMoreHistory = true;
  questionnaireStarted = false;
  currentQuestionIndex = null;
  loadChatHistory(true);
}

// Function to load chat history
function loadChatHistory(scrollToBottom = true) {
  if (loadingHistory || !hasMoreHistory || chatHistoryPage < 1) return;
  loadingHistory = true;

  // Show the loading placeholder at the top
  showLoadingPlaceholder();

  // Capture the current scroll position and the current height of the chatBody
  const currentScrollTop = chatBody.scrollTop;
  const previousHeight = chatBody.scrollHeight;

  fetch(`/get_chat_history/?page=${chatHistoryPage}`)
    .then((response) => response.json())
    .then((data) => {
      loadingHistory = false;
      removeLoadingPlaceholder();

      if (data.chat_history && data.chat_history.length > 0) {
        const messages = data.chat_history;

        // Prepend older messages
        prependMessages(messages);

        if (chatHistoryPage >= data.total_pages) {
          hasMoreHistory = false;
        } else {
          chatHistoryPage++; // Increment to fetch the next page on future scrolls
        }
      } else {
        hasMoreHistory = false;
      }

      // Calculate the new height after loading messages
      const newHeight = chatBody.scrollHeight;

      // Maintain the scroll position after loading older messages
      chatBody.scrollTop = currentScrollTop + (newHeight - previousHeight);

      // Check if chat is empty and show greeting if needed
      if (data.is_chat_empty && data.show_greeting) {
        showGreetingMessage();
      }

      if (scrollToBottom) {
        chatBody.scrollTop = chatBody.scrollHeight;
      }
    })
    .catch((error) => {
      loadingHistory = false;
      removeLoadingPlaceholder();
      console.error("Error fetching chat history:", error);
      // Show error message to the user
      showErrorMessage("Failed to load chat history. Please try again.");
    });
}
// Function to display greeting message with simulated typing and options
function showGreetingMessage() {
  const greetingMessage =
    "Hello! Welcome to PilarEase, your emotional support companion. How can I assist you today? Should we start?";

  simulateTyping(greetingMessage, "bot", () => {
    displayOptions(["Start", "Not Yet"]);

    // Save the greeting message to the backend, associated with the authenticated user
    fetch("/send_chat_message/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        message: greetingMessage,
        is_bot_message: true,
        associate_with_user: true, // Custom flag to associate with user
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Greeting message saved successfully.");
        } else {
          console.error("Failed to save greeting message:", data.error);
          showErrorMessage("Failed to save greeting message.");
        }
      })
      .catch((error) => {
        console.error("Error saving greeting message:", error);
        showErrorMessage("Failed to save greeting message.");
      });
  });
}
// Function to prepend messages to chat body
function prependMessages(messages) {
  // Record the current scroll position
  const previousScrollHeight = chatBody.scrollHeight;

  messages.forEach((message) => {
    const messageWrapper = document.createElement("div");
    messageWrapper.className = "message-wrapper";

    const messageElement = document.createElement("div");
    messageElement.className =
      message.sender === "bot"
        ? "chatbot-message chat-message"
        : "user-message chat-message";
    messageElement.textContent = message.message;

    messageWrapper.appendChild(messageElement);
    chatBody.insertBefore(messageWrapper, chatBody.firstChild);
  });

  // Calculate the new scroll position to maintain view
  const newScrollHeight = chatBody.scrollHeight;
  chatBody.scrollTop = newScrollHeight - previousScrollHeight;
}

// Function to show loading placeholder
function showLoadingPlaceholder() {
  const loaderWrapper = document.createElement("div");
  loaderWrapper.id = "loadingPlaceholder";
  loaderWrapper.className = "loading-placeholder";

  const loader = document.createElement("div");
  loader.className = "loader";
  loader.innerHTML =
    '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';

  loaderWrapper.appendChild(loader);
  chatBody.insertBefore(loaderWrapper, chatBody.firstChild);
}

// Function to remove loading placeholder
function removeLoadingPlaceholder() {
  const loaderWrapper = document.getElementById("loadingPlaceholder");
  if (loaderWrapper) {
    chatBody.removeChild(loaderWrapper);
  }
}

// Function to start chat session
function startChatSession() {
  fetch("/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      message: "start", // Send 'start' to initiate the questionnaire
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        if (data.question && data.answer_options) {
          // Display the first question with its answer options
          simulateTyping(data.question, "bot", () => {
            displayAnswerOptions(data.answer_options, data.question_index);
            questionnaireStarted = true;
            currentQuestionIndex = data.question_index;
          });
        } else if (data.message && data.show_greeting) {
          // If a greeting message is returned, display it with options
          simulateTyping(data.message, "bot", () => {
            displayOptions(data.show_greeting); // ["Start", "Not Yet"]
            questionnaireStarted = true; // Indicate that the greeting has been shown
          });
        } else {
          // Handle other possible responses
          showErrorMessage(data.error || "Failed to start chat session.");
        }
      } else {
        showErrorMessage(data.error || "Failed to start chat session.");
      }
    })
    .catch((error) => {
      console.error("Error starting chat session:", error);
      showErrorMessage("Failed to start chat session. Please try again.");
    });
}

// Function to display options (e.g., Start, Not Yet)
function displayOptions(options) {
  const optionsWrapper = document.createElement("div");
  optionsWrapper.className = "message-wrapper options-wrapper pop-up"; // Added 'pop-up' class
  optionsWrapper.id = "dialogOptions";

  options.forEach((option) => {
    const button = document.createElement("button");
    button.className = "option-button";
    button.textContent = option;
    button.onclick = function () {
      handleOptionClick(option, optionsWrapper);
    };
    optionsWrapper.appendChild(button);
  });

  chatBody.appendChild(optionsWrapper);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Function to display answer options for a question
function displayAnswerOptions(options, questionIndex) {
  const answersWrapper = document.createElement("div");
  answersWrapper.className = "message-wrapper answers-wrapper pop-up";
  answersWrapper.id = "answersWrapper"; // Assign ID to remove later

  options.forEach((answerText) => {
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
}

// Function to handle option click (e.g., Start, Not Yet)
function handleOptionClick(option, optionsWrapper) {
  // Display user selection
  generateMessage(option, "user");

  // Apply the 'pop-down' animation class
  optionsWrapper.classList.remove("pop-up");
  optionsWrapper.classList.add("pop-down");

  // Disable buttons to prevent multiple clicks
  optionsWrapper
    .querySelectorAll("button")
    .forEach((btn) => (btn.disabled = true));

  // Listen for the end of the animation to remove the wrapper
  optionsWrapper.addEventListener(
    "animationend",
    () => {
      optionsWrapper.remove();
    },
    { once: true }
  );

  if (option === "Start" || option === "Not Yet") {
    // Send the selected option to the backend
    fetch("/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ message: option }), // Send as "Start" or "Not Yet"
    })
      .then((response) => response.json())
      .then((data) => {
        if (
          option === "Start" &&
          data.success &&
          data.question &&
          data.answer_options
        ) {
          // Proceed to display the first question
          simulateTyping(data.question, "bot", () => {
            displayAnswerOptions(data.answer_options, data.question_index);
            currentQuestionIndex = data.question_index;
            questionnaireStarted = true;
          });
        } else if (option === "Not Yet" && data.message) {
          // Handle "Not Yet" acknowledgment
          simulateTyping(data.message, "bot");
        } else {
          // Handle server-side errors
          console.error("Error:", data.error);
          showErrorMessage(
            data.error || "Failed to start the questionnaire. Please try again."
          );
        }
      })
      .catch((error) => {
        console.error("Error starting questionnaire:", error);
        showErrorMessage(
          "Failed to start the questionnaire. Please try again."
        );
      });
  }
}
// Function to handle answer selection within the questionnaire
function handleAnswerSelection(questionIndex, answerText) {
  const answersWrapper = document.getElementById("answersWrapper");

  if (answersWrapper) {
    // Animate and remove the answer options
    answersWrapper.classList.remove("pop-up");
    answersWrapper.classList.add("pop-down");
    setTimeout(() => answersWrapper.remove(), 300);
  }

  // Display the user's selected answer in the chat
  generateMessage(answerText, "user");

  // Generate a unique answer_id
  const answer_id = generateUUID();

  // Send the selected answer to the backend
  fetch("/submit_answer/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      question_index: questionIndex,
      answer_text: answerText,
      answer_id: answer_id,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        if (data.response) {
          // Display the predefined response first
          simulateTyping(data.response, "bot", () => {
            if (
              data.next_question_index !== undefined &&
              data.question &&
              data.answer_options
            ) {
              // After response, display the next question
              simulateTyping(data.question, "bot", () => {
                displayAnswerOptions(
                  data.answer_options,
                  data.next_question_index
                );
                currentQuestionIndex = data.next_question_index;
              });
            } else if (data.end_of_questions && data.final_bot_message) {
              // If it's the end of the questionnaire, display the final message
              simulateTyping(data.final_bot_message, "bot", () => {
                displayFinalOptions();
              });
            }
          });
        } else if (
          data.next_question_index !== undefined &&
          data.question &&
          data.answer_options
        ) {
          // Fallback: If no response, proceed to next question
          simulateTyping(data.question, "bot", () => {
            displayAnswerOptions(data.answer_options, data.next_question_index);
            currentQuestionIndex = data.next_question_index;
          });
        } else if (data.end_of_questions && data.final_bot_message) {
          // Handle end of questionnaire without response
          simulateTyping(data.final_bot_message, "bot", () => {
            displayFinalOptions();
          });
        }
      } else {
        // Handle errors returned from the backend
        if (data.error) {
          showErrorMessage(data.error);
        } else {
          showErrorMessage("An unexpected error occurred.");
        }
      }
    })
    .catch((error) => {
      console.error("Error submitting answer:", error);
      showErrorMessage("Failed to submit your choice. Please try again.");
    });
}

// Function to display final options (e.g., Yes/No)
function displayFinalOptions() {
  const optionsWrapper = document.createElement("div");
  optionsWrapper.className = "message-wrapper final-options-wrapper pop-up"; // Added 'pop-up' class
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

// Function to handle final option selection
function handleFinalOptionSelection(selection, optionsWrapper) {
  // Display user selection
  generateMessage(selection, "user");

  // Apply the 'pop-down' animation class
  optionsWrapper.classList.remove("pop-up");
  optionsWrapper.classList.add("pop-down");

  // Disable buttons to prevent multiple clicks
  const buttons = optionsWrapper.querySelectorAll("button");
  buttons.forEach((btn) => (btn.disabled = true));

  // Listen for the end of the animation to remove the wrapper
  optionsWrapper.addEventListener(
    "animationend",
    () => {
      optionsWrapper.remove();
    },
    { once: true }
  );

  // Send POST request to the /final_option_selection/ endpoint
  fetch("/final_option_selection/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      selection: selection,
      // answer_id: generateUUID(), // Include if necessary
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.message) {
        // Append bot response with simulated typing
        simulateTyping(data.message, "bot");
      } else if (data.error) {
        // Display error message from backend
        showErrorMessage(data.error);
      } else {
        showErrorMessage("An unexpected error occurred.");
      }
    })
    .catch((error) => {
      console.error("Error submitting selection:", error);
      showErrorMessage("Failed to submit your choice. Please try again.");
    });
}
// Function to generate chat message
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

// Function to simulate typing with delay
function simulateTyping(text, sender, callback = null) {
  showLoader(chatBody); // Show loader once
  const typingDelay = Math.max(500, text.length * 30); // Adjusted delay

  setTimeout(() => {
    removeLoader(chatBody); // Remove loader once
    generateMessage(text, sender);
    if (callback) callback();
  }, typingDelay);
}

// Function to show loader animation
function showLoader(chatBody) {
  const loaderElement = document.createElement("div");
  loaderElement.className = "loader";
  loaderElement.innerHTML =
    '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  chatBody.appendChild(loaderElement);
  chatBody.scrollTop = chatBody.scrollHeight;
}

// Function to remove loader animation
function removeLoader(chatBody) {
  const loaderElement = chatBody.querySelector(".loader");
  if (loaderElement) {
    chatBody.removeChild(loaderElement);
  }
}

// Function to show error message
function showErrorMessage(errorText) {
  const errorWrapper = document.createElement("div");
  errorWrapper.className = "message-wrapper";

  const errorElement = document.createElement("div");
  errorElement.className = "error-message chat-message";
  errorElement.textContent = errorText;

  errorWrapper.appendChild(errorElement);
  chatBody.appendChild(errorWrapper);

  chatBody.scrollTop = chatBody.scrollHeight;

  // Optionally, store the error in sessionStorage to display on reload
  sessionStorage.setItem("chatError", errorText);
}

// Function to send messages via chat input
function sendMessage() {
  const message = chatInput.value.trim();
  if (message === "") return;

  generateMessage(message, "user");
  chatInput.value = "";

  // Send the message to the backend
  fetch("/chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({ message: message }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        if (data.question && data.answer_options) {
          // Handle the next question
          simulateTyping(data.question, "bot", () => {
            displayAnswerOptions(data.answer_options, data.question_index);
            currentQuestionIndex = data.question_index;
          });
        } else if (data.message) {
          // Handle any bot messages
          simulateTyping(data.message, "bot");
        }
      } else {
        // Handle errors or prompts from the bot
        if (data.message) {
          simulateTyping(data.message, "bot");
        } else {
          showErrorMessage(data.error || "An error occurred.");
        }
      }
    })
    .catch((error) => {
      console.error("Error sending message:", error);
      showErrorMessage("Failed to send message. Please try again.");
    });
}

// Function to display a question based on question index
function displayQuestion(questionIndex, questionText) {
  simulateTyping(questionText, "bot", () => {
    // The answer options are already displayed via displayAnswerOptions
    // No need to fetch them again
  });
}

// Function to generate UUID
function generateUUID() {
  // Public Domain/MIT
  var d = new Date().getTime(); // Timestamp
  var d2 = (performance && performance.now && performance.now() * 1000) || 0; // Time in microseconds since page-load or 0 if unsupported
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function (c) {
    var r = Math.random() * 16; // random number between 0 and 16
    if (d > 0) {
      r = (d + r) % 16 | 0;
      d = Math.floor(d / 16);
    } else {
      r = (d2 + r) % 16 | 0;
      d2 = Math.floor(d2 / 16);
    }
    return (c === "x" ? r : (r & 0x3) | 0x8).toString(16);
  });
}

// Utility Function to Get CSRF Token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Accessibility: Keyboard navigation for chat input
chatInput.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Accessibility: Close modal with Escape key
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeModal();
  }
});

// Scroll detection for "Scroll to Latest" button and lazy loading
chatBody.addEventListener("scroll", function () {
  const scrollTop = chatBody.scrollTop;
  const scrollHeight = chatBody.scrollHeight;
  const clientHeight = chatBody.clientHeight;

  if (scrollTop === 0 && !loadingHistory && hasMoreHistory) {
    // Load more messages when scrolled to top
    loadChatHistory(false);
  }

  if (scrollTop < scrollHeight - clientHeight - 100) {
    // User scrolled up more than 100px from the bottom
    scrollToLatestButton.style.display = "block";
  } else {
    scrollToLatestButton.style.display = "none";
  }
});

// Profile Modal Handling
profileLink.addEventListener("click", (e) => {
  e.preventDefault();
  closeCurrentModal();
  profileModal.style.display = "block";
  profileModal.classList.add("slide-downSolid");
  profileModal.classList.remove("slide-upSolid");
  fetchUserProfile(); // Fetch and populate user data when the modal is opened
});

// Close Profile Modal
closeProfileModal.addEventListener("click", () => {
  profileModal.classList.add("slide-upSolid");
  profileModal.classList.remove("slide-downSolid");
});

// Avatar Modal Handling
avatarLink.addEventListener("click", (e) => {
  e.preventDefault();
  closeCurrentModal();
  avatarModal.style.display = "block";
  avatarModal.classList.add("slide-downSolid");
  avatarModal.classList.remove("slide-upSolid");
});

// Close Avatar Modal
closeAvatarModal.addEventListener("click", () => {
  avatarModal.classList.add("slide-upSolid");
  avatarModal.classList.remove("slide-downSolid");
});

// Password Modal Handling
passwordLink.addEventListener("click", (e) => {
  e.preventDefault();
  closeCurrentModal();
  passwordModal.style.display = "block";
  passwordModal.classList.add("slide-downSolid");
  passwordModal.classList.remove("slide-upSolid");
});

// Close Password Modal
closePasswordModal.addEventListener("click", () => {
  passwordModal.classList.add("slide-upSolid");
  passwordModal.classList.remove("slide-downSolid");
});

// Status Modal Handling
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

// Close Status Modal
closeStatusModal.addEventListener("click", function () {
  closeModal();
});

// Close modal when clicking outside the modal content
statusModalOverlay.addEventListener("click", function () {
  closeModal();
});

// Function to close any open modal with animation
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

// Burger Menu Handling
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

// Close dropdown menu when any link is clicked
document.querySelectorAll(".dropdown a").forEach((link) => {
  link.addEventListener("click", () => {
    burger.checked = false;
    dropdown.classList.add("slide-up");
    dropdown.classList.remove("slide-down");
  });
});

// Placeholder functionality for description div
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

// Function to fetch user profile data (Assuming an endpoint exists)
function fetchUserProfile() {
  fetch("/get_user_profile/")
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Populate profile modal with user data
        document.getElementById("profileUsername").textContent = data.username;
        document.getElementById("profileFullName").textContent = data.full_name;
        document.getElementById("profileEmail").textContent = data.email;
        // Add more fields as necessary
      } else {
        showErrorMessage("Failed to load profile data.");
      }
    })
    .catch((error) => {
      console.error("Error fetching user profile:", error);
      showErrorMessage("Failed to load profile data.");
    });
}

// Debounce function to limit the rate at which a function can fire.
function debounce(func, wait) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// Optional: Debounce some heavy operations if needed
// Example usage: const debouncedFunction = debounce(myFunction, 300);

// Additional functionalities can be added here...
