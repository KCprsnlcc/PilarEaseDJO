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
let greetingDisplayed = false;

document
  .getElementById("floatingButton")
  .addEventListener("click", function () {
    document.getElementById("chatPopup").style.display = "block";
    const chatBody = document.getElementById("chatBody");

    if (!greetingDisplayed) {
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
  });

function displayOptions() {
  const chatBody = document.getElementById("chatBody");

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

function sendMessage() {
  const chatInput = document.getElementById("chatInput");
  const chatBody = document.getElementById("chatBody");
  const messageText = chatInput.value.trim();

  if (messageText !== "") {
    generateMessage(messageText, "user");

    fetch("/send_message/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        message: messageText,
        is_bot_message: false,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          if (messageText.toLowerCase() === "start") {
            setTimeout(() => {
              showLoader(chatBody);
              setTimeout(() => {
                removeLoader(chatBody);
                displayQuestion(0);
              }, 1500);
            }, 1000);
          } else if (messageText.toLowerCase() === "not yet") {
            setTimeout(() => {
              generateMessage("No worries, take your time.", "bot");
            }, 1000);
          } else {
            matchAnswerToOptions(messageText);
          }
        }
      });
    chatInput.value = ""; // Clear the input field after sending
  }
}

function matchAnswerToOptions(inputText) {
  const chatBody = document.getElementById("chatBody");
  const answersWrapper = document.querySelector(".answers-wrapper");

  if (answersWrapper) {
    const buttons = answersWrapper.querySelectorAll(".answers-button");

    buttons.forEach((button) => {
      if (button.textContent.toLowerCase() === inputText.toLowerCase()) {
        button.click();
      }
    });
  }
}

function showLoader(chatBody) {
  const loaderElement = document.createElement("div");
  loaderElement.className = "loader";
  loaderElement.innerHTML =
    '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
  chatBody.appendChild(loaderElement);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function removeLoader(chatBody) {
  const loaderElement = chatBody.querySelector(".loader");
  if (loaderElement) {
    chatBody.removeChild(loaderElement);
  }
}

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
}

function displayQuestion(questionIndex) {
  const questions = [
    "What aspects of your academic life cause you the most stress?",
    "How would you describe your overall emotional state in the past month?",
    "How comfortable do you feel talking to friends or family about your mental health?",
    "How frequently do you experience feelings of anxiety or worry related to school?",
    "How many hours of sleep do you usually get on a school night?",
    "How confident do you feel in your academic abilities?",
    "How do you usually feel about changes in your academic or personal life?",
    "How do you manage your time between schoolwork, extracurricular activities, and relaxation?",
    "How motivated do you feel to complete your academic tasks?",
    "Are you aware of the mental health resources available at your school?",
  ];

  if (questionIndex >= questions.length) {
    generateMessage("Thank you for answering all the questions!", "bot");
    return;
  }

  const currentQuestion = questions[questionIndex];

  showLoader(document.getElementById("chatBody"));
  setTimeout(() => {
    removeLoader(document.getElementById("chatBody"));
    generateMessage(currentQuestion, "bot");

    // Save the generated question to the database
    saveQuestionnaireData(currentQuestion, null, null);

    setTimeout(() => {
      displayAnswerOptions(questionIndex);
    }, 500);
  }, 1500);
}

function displayAnswerOptions(questionIndex) {
  const answers = [
    [
      "Managing multiple assignments and deadlines.",
      "Understanding difficult subjects or topics.",
      "Balancing academics with extracurricular activities.",
    ],
    [
      "Generally positive, with only occasional low moods.",
      "Mixed, with frequent ups and downs.",
      "Often stressed or anxious.",
    ],
    [
      "Very comfortable, I often share how I’m feeling.",
      "Somewhat comfortable, I share occasionally.",
      "Not comfortable, I usually keep things to myself.",
    ],
    [
      "Almost daily, it’s a constant presence.",
      "Occasionally, but only around stressful times like exams.",
      "Rarely, I don’t get anxious easily.",
    ],
    [
      "Less than 6 hours, I often stay up late.",
      "Between 6 and 8 hours, it varies.",
      "More than 8 hours, I prioritize my sleep.",
    ],
    [
      "Very confident, I believe in my abilities.",
      "Somewhat confident, but I have doubts sometimes.",
      "Not very confident, I often worry about my performance.",
    ],
    [
      "Excited and ready to adapt.",
      "Nervous but willing to adjust.",
      "Stressed and resistant to change.",
    ],
    [
      "I create a schedule and stick to it as much as possible.",
      "I try to balance things, but it’s a challenge.",
      "I often struggle to manage my time effectively.",
    ],
    [
      "Highly motivated, I’m eager to succeed.",
      "Moderately motivated, but it depends on the task.",
      "Often unmotivated, I struggle to find the drive.",
    ],
    [
      "Yes, I know where to find help if I need it.",
      "Somewhat, I’ve heard of some resources but haven’t explored them.",
      "No, I’m not aware of the available resources.",
    ],
  ];

  const chatBody = document.getElementById("chatBody");

  const answersWrapper = document.createElement("div");
  answersWrapper.className = "message-wrapper answers-wrapper";

  answers[questionIndex].forEach((answerText, index) => {
    const answerButton = document.createElement("button");
    answerButton.className = "answers-button";
    answerButton.textContent = answerText;
    answerButton.onclick = function () {
      handleAnswerSelection(questionIndex, index, answerText);
    };
    answersWrapper.appendChild(answerButton);
  });

  chatBody.appendChild(answersWrapper);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function handleAnswerSelection(questionIndex, answerIndex, answerText) {
  const chatBody = document.getElementById("chatBody");

  const answersWrapper = document.querySelector(".answers-wrapper");
  if (answersWrapper) {
    answersWrapper.classList.remove("pop-up");
    answersWrapper.classList.add("pop-down");
    setTimeout(() => answersWrapper.remove(), 300);
  }

  generateMessage(answerText, "user");

  const responses = [
    [
      "Managing multiple assignments can lead to significant stress, which can impact your mental health. It's important to develop strategies to manage this workload to protect your well-being.",
      "Struggling with difficult subjects can cause stress and anxiety. Seeking help or using different study methods can reduce these feelings and improve your mental health.",
      "Balancing academics and extracurriculars can be stressful and may overwhelm your mental health. Finding a healthy balance is key to maintaining your well-being.",
    ],
    [
      "It's great to hear that you've been feeling generally positive. Maintaining a positive emotional state is important for good mental health, so keep focusing on what keeps you feeling well.",
      "Experiencing frequent ups and downs can be challenging for your mental health. It might be helpful to explore techniques to stabilize your emotions and support your well-being.",
      "Feeling stressed or anxious often can take a toll on your mental health. It's important to address these feelings and find ways to manage them to protect your well-being.",
    ],
    [
      "It’s excellent that you feel comfortable discussing your mental health with others. Having a support system is crucial for maintaining good mental health.",
      "It’s good that you share your feelings sometimes. Being open about your mental health can provide relief and support, which are important for emotional well-being.",
      "Keeping your feelings to yourself can lead to increased stress and affect your mental health. Consider finding a trusted person to talk to, as sharing can be very beneficial.",
    ],
    [
      "Experiencing daily anxiety can significantly impact your mental health. It's important to seek ways to reduce this anxiety, as prolonged stress can have serious effects on your well-being.",
      "Feeling anxious during stressful times like exams is common, but managing this anxiety is key to protecting your mental health during these periods.",
      "It's great that you rarely experience anxiety. Maintaining this level of calm is beneficial for your mental health, and it’s important to continue practicing whatever keeps you feeling this way.",
    ],
    [
      "Getting less than 6 hours of sleep can negatively affect your mental health, leading to increased stress and reduced emotional resilience. Prioritizing sleep is crucial for your well-being.",
      "Getting between 6 and 8 hours of sleep is important, but inconsistency can impact your mental health. A regular sleep routine can improve your emotional stability and reduce stress.",
      "Prioritizing sleep is one of the best things you can do for your mental health. It helps maintain emotional balance and resilience, which are key to handling stress.",
    ],
    [
      "Feeling confident in your abilities is excellent for your mental health. It can reduce anxiety and stress, contributing to a more positive and balanced state of mind.",
      "Having some doubts is normal, but too much self-doubt can negatively impact your mental health. Building confidence through small successes can help improve your overall well-being.",
      "Constant worry about your performance can lead to anxiety and stress, affecting your mental health. It's important to address these worries and work on building self-confidence.",
    ],
    [
      "Being excited about change is a positive sign for your mental health. Adaptability and a positive outlook can help you manage stress and maintain emotional well-being.",
      "It’s normal to feel nervous about change, but being willing to adjust is important for your mental health. Embracing change gradually can help reduce stress and anxiety.",
      "Resistance to change can cause stress, which may impact your mental health. Finding ways to cope with change is crucial for maintaining emotional stability.",
    ],
    [
      "Having a schedule and sticking to it is excellent for your mental health. It helps reduce stress and ensures you have time for relaxation, which is crucial for well-being.",
      "Balancing your responsibilities can be challenging and impact your mental health. Developing better time management skills can reduce stress and improve your overall well-being.",
      "Struggling with time management can lead to stress and affect your mental health. Working on these skills can help you feel more in control and reduce anxiety.",
    ],
    [
      "High motivation is a great indicator of good mental health. Staying motivated helps you manage stress and keep a positive outlook.",
      "It's normal for motivation to vary, but staying engaged in your tasks can support your mental health by providing a sense of accomplishment.",
      "Struggling with motivation can be a sign of mental fatigue or stress. It’s important to address these feelings to prevent them from negatively impacting your mental health.",
    ],
    [
      "It’s great that you’re aware of the mental health resources available. Knowing where to get help is crucial for maintaining your mental well-being.",
      "It’s good that you’re somewhat aware, but exploring these resources further can ensure you have the support you need when challenges arise.",
      "It’s important to be informed about mental health resources, as they can provide crucial support when needed. Taking the time to learn about them can make a big difference.",
    ],
  ];

  // Save the selected answer and response to the database
  saveQuestionnaireData(
    null,
    answerText,
    responses[questionIndex][answerIndex]
  );

  setTimeout(() => {
    showLoader(chatBody);
    setTimeout(() => {
      removeLoader(chatBody);
      generateMessage(responses[questionIndex][answerIndex], "bot");

      setTimeout(() => {
        displayQuestion(questionIndex + 1);
      }, 2000);
    }, 1500);
  }, 1000);
}

function saveQuestionnaireData(question, answer, response) {
  fetch("/save_questionnaire_data/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      question: question,
      answer: answer,
      response: response,
    }),
  });
}

function addTimestampIfNeeded(chatBody) {
  const currentTime = new Date();

  if (!lastMessageTime || currentTime - lastMessageTime > 300000) {
    const sessionTimestamp = document.createElement("div");
    sessionTimestamp.className = "session-timestamp";
    sessionTimestamp.textContent = getCurrentTime();
    chatBody.appendChild(sessionTimestamp);
  }

  lastMessageTime = currentTime;
}

function getCurrentTime() {
  const now = new Date();
  let hours = now.getHours();
  const minutes = now.getMinutes();
  const ampm = hours >= 12 ? "PM" : "AM";

  hours = hours % 12;
  hours = hours ? hours : 12;
  const strMinutes = minutes < 10 ? "0" + minutes : minutes;
  const strTime = hours + ":" + strMinutes + " " + ampm;

  return strTime;
}

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
