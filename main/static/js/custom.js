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
const scrollToLatestButton = document.getElementById("scrollToLatestButton");

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

// Function to open chat popup
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

  if (!questionnaireStarted) {
    fetchStartChat();
  }
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
      removeLoadingPlaceholder();
      console.error("Error fetching chat history:", error);
      // Show error message to the user
      showErrorMessage("Failed to load chat history. Please try again.");
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
      message.sender === "user"
        ? "user-message chat-message"
        : "chatbot-message chat-message";
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
  fetch("/start_chat/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({}),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success && data.message) {
        simulateTyping(data.message, "bot", () => {
          if (data.options && data.options.length > 0) {
            displayOptions(data.options);
            questionnaireStarted = true;
          }
        });
      } else if (data.success && !data.message) {
        // Chat is not empty; no action needed
      } else {
        showErrorMessage(data.error || "Failed to start chat session.");
      }
    })
    .catch((error) => {
      showErrorMessage("Failed to start chat session. Please try again.");
    });
}
// Function to display options (e.g., Start, Not Yet)
function displayOptions(options) {
  const optionsWrapper = document.createElement("div");
  optionsWrapper.className = "message-wrapper options-wrapper pop-up";
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

async function fetchWithRetry(url, options, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const response = await fetch(url, options);
      if (!response.ok) throw new Error(`HTTP status ${response.status}`);
      return await response.json();
    } catch (error) {
      if (i < retries - 1) {
        await new Promise((resolve) => setTimeout(resolve, delay * (i + 1)));
      } else {
        showErrorMessage("Network error. Please try again.");
        throw error;
      }
    }
  }
}
function handleOptionClick(option, optionsWrapper) {
  // Display user message
  generateMessage(option, "user");

  optionsWrapper.classList.add("poptotheright");
  optionsWrapper
    .querySelectorAll("button")
    .forEach((btn) => (btn.disabled = true));

  fetchWithRetry("/submit_answer/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      question_index: currentQuestionIndex,
      answer_text: option,
    }),
  }).then((data) => {
    if (data.success) {
      sessionStorage.removeItem("chatError"); // Clear error if successful
      optionsWrapper.remove();
      simulateTyping(data.response, "bot", () => {
        if (data.next_question_index !== undefined) {
          currentQuestionIndex = data.next_question_index;
          displayAnswerOptions(currentQuestionIndex);
        }
        if (data.end_of_questions) displayFinalOptions();
      });
    }
    // Removed else block as per instruction
  });
  // Removed catch block as per instruction
}
// Function to display a question based on question index
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

// Function to display answer options for a question
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

// Function to handle answer selection
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
          if (data.next_question_index !== undefined) {
            currentQuestionIndex = data.next_question_index;
            displayQuestion(data.next_question_index);
          }

          if (data.end_of_questions) {
            displayFinalOptions();
          }
        });
      } else {
        console.error("Error:", data.error);
        showErrorMessage("Failed to submit answer. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error submitting answer:", error);
      showErrorMessage("Failed to submit answer. Please try again.");
    });
}

// Function to display final options (e.g., Yes/No)
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

// Function to handle final option selection
function handleFinalOptionSelection(selection, optionsWrapper) {
  // Display user selection
  generateMessage(selection, "user");

  // Apply the 'poptotheright' animation class
  optionsWrapper.classList.add("poptotherright");

  // Disable buttons to prevent multiple clicks
  const buttons = optionsWrapper.querySelectorAll("button");
  buttons.forEach((btn) => (btn.disabled = true));

  // Send the selected final option to the server
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
        // Remove the options after animation completes
        setTimeout(() => {
          optionsWrapper.remove();
        }, 500); // Match the animation duration

        // Append bot response
        simulateTyping(data.message, "bot");
      } else {
        console.error("Error:", data.error);
        showErrorMessage("Failed to submit your choice. Please try again.");
      }
    })
    .catch((error) => {
      console.error("Error submitting final option:", error);
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
  showLoader(chatBody);
  const typingDelay = Math.max(500, text.length * 30); // Adjusted delay

  setTimeout(() => {
    removeLoader(chatBody);
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
}

// Utility Function to Get CSRF Token
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

// Accessibility: Keyboard navigation for chat input
chatInput.addEventListener("keydown", function (e) {
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

// Additional accessibility: Keyboard navigation for chat input
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
