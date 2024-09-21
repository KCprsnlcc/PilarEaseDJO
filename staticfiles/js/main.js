document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("loader-overlay").style.display = "none";
  function fontsAndIconsLoaded() {
    const fontNames = ["Aguafina Script", "Gothic A1", "Inter", "Epilogue"];

    const allFontsLoaded = fontNames.every((font) =>
      document.fonts.check(`1em ${font}`)
    );

    // Check if Boxicons are loaded by checking if any element using it has been styled
    const boxiconLoaded = document.fonts.check('1em "boxicons"');

    return allFontsLoaded && boxiconLoaded;
  }

  // Hide the loader once fonts and icons are loaded
  document.fonts.ready.then(() => {
    if (fontsAndIconsLoaded()) {
      document.getElementById("loader-overlay").style.display = "none";
      document.getElementById("overlay").style.display = "none";
    } else {
      // If not loaded, keep checking
      const interval = setInterval(() => {
        if (fontsAndIconsLoaded()) {
          clearInterval(interval);
          document.getElementById("loader-overlay").style.display = "none";
          document.getElementById("overlay").style.display = "none";
        }
      }, 100); // Check every 100ms
    }
  });
  const avatarLoader = document.getElementById("avatarLoader");
  const currentAvatar = document.getElementById("currentAvatar");
  const avatarModal = document.getElementById("avatarModal");
  const closeAvatarModal = document.getElementById("closeAvatarModal");
  const saveAvatarBtn = document.getElementById("saveAvatarBtn");
  const cancelAvatarBtn = document.getElementById("cancelAvatarBtn");
  const avatarImages = document.querySelectorAll(
    ".avatars-grid img.avatar-option"
  );
  const uploadAvatarInput = document.getElementById("uploadAvatarInput");
  const cropperModal = document.getElementById("cropperModal");
  const closeCropperModal = document.getElementById("closeCropperModal");
  const cropImageBtn = document.getElementById("cropImageBtn");
  const cancelCropBtn = document.getElementById("cancelCropBtn");
  const imageToCrop = document.getElementById("imageToCrop");
  let selectedAvatar = null;
  let cropper;

  const uploadAvatarUrl = document.getElementById("uploadAvatarUrl").value;
  const placeholderUrl = currentAvatar.dataset.placeholderUrl;

  const statusModal = document.getElementById("statusModal");
  const statusForm = document.getElementById("statusForm");
  const feelingIcons = document.querySelectorAll(".feeling-icon");
  const statusTitle = document.getElementById("caption");
  const statusDescription = document.getElementById("description");
  const statusLoader = document.getElementById("statusLoader");
  const confirmStatusModal = document.getElementById("ConfirmStatusModal");
  const confirmBtn = document.getElementById("confirmBtn");
  const cancelBtn = document.getElementById("cancelBtn");
  const categoryElements = document.querySelectorAll(".v1_124 div");
  const contactUsButton = document.getElementById("contactUsButton");
  const contactUsModal = document.getElementById("contactUsModal");
  const closeContactUsModal = document.getElementById("closeContactUsModal");

  let selectedEmotion = null;
  let page = 1;
  let isLoading = false;
  let hasNext = true;
  let activeCategory = "recent";

  document.addEventListener("DOMContentLoaded", function () {
    const rememberMeCheckbox = document.getElementById("rememberMe");
    const usernameField = document.querySelector('input[name="username"]');
    const passwordField = document.querySelector('input[name="password"]');

    // Check if credentials are stored
    if (localStorage.getItem("rememberMe") === "true") {
      usernameField.value = localStorage.getItem("username");
      passwordField.value = localStorage.getItem("password");
      rememberMeCheckbox.checked = true;
    }

    // Save credentials if "Remember Me" is checked
    document.getElementById("loginForm").onsubmit = function () {
      if (rememberMeCheckbox.checked) {
        localStorage.setItem("rememberMe", "true");
        localStorage.setItem("username", usernameField.value);
        localStorage.setItem("password", passwordField.value);
      } else {
        localStorage.removeItem("rememberMe");
        localStorage.removeItem("username");
        localStorage.removeItem("password");
      }
    };
  });

  // Get the relevant elements
  const forgotPasswordLink = document.getElementById("forgotPasswordLink");
  const forgotPasswordModal = document.getElementById("forgotPasswordModal");
  const closeForgotPasswordModal = document.getElementById(
    "closeForgotPasswordModal"
  );

  // Show Forgot Password modal
  if (forgotPasswordLink) {
    forgotPasswordLink.onclick = function (event) {
      event.preventDefault();
      forgotPasswordModal.style.display = "block"; // Display the modal
      setTimeout(() => {
        forgotPasswordModal.classList.add("pop-in"); // Add pop-in animation
      }, 10);
    };
  }

  // Close Forgot Password modal
  if (closeForgotPasswordModal) {
    closeForgotPasswordModal.onclick = function () {
      forgotPasswordModal.classList.add("pop-out"); // Add pop-out animation to the forgot password modal
      setTimeout(() => {
        forgotPasswordModal.style.display = "none"; // Hide the modal after the animation
        forgotPasswordModal.classList.remove("pop-in", "pop-out"); // Clean up classes
      }, 300); // Duration should match the animation time
    };
  }
  document
    .getElementById("forgotPasswordForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission

      const emailInput = document.querySelector('input[name="email"]');
      const email = emailInput.value;
      const submitButton = document.querySelector(".v53_207");
      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

      // Show the loader
      showForgotPassLoader();

      // Disable the button
      submitButton.disabled = true;

      fetch("/password-reset/", {
        // Use the correct URL path
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": csrfToken,
        },
        body: new URLSearchParams({ email: email }),
      })
        .then((response) => response.json())
        .then((data) => {
          // Hide the loader
          hideForgotPassLoader();

          if (data.success) {
            forgotPasswordSuccessBox(data.message);
          } else {
            if (data.error.includes("3 minutes")) {
              forgotPasswordCooldownBox(data.error);
            } else {
              forgotPasswordErrorBox(data.error);
            }
          }

          // Re-enable the button after the animation finishes
          setTimeout(() => {
            submitButton.disabled = false;
          }, 3600); // 3000ms for dialog visibility + 300ms for pop-out animation
        })
        .catch((error) => {
          hideForgotPassLoader(); // Ensure loader is hidden on error
          console.error("Error:", error);
          forgotPasswordErrorBox("An error occurred. Please try again later.");
          setTimeout(() => {
            submitButton.disabled = false;
          }, 3600);
        });
    });

  function showForgotPassLoader() {
    document.getElementById("forgotpassOverlay").style.display = "block";
  }

  function hideForgotPassLoader() {
    document.getElementById("forgotpassOverlay").style.display = "none";
  }

  // Function to show success dialog with pop-in and pop-out animation
  function forgotPasswordSuccessBox(message) {
    const successBox = document.getElementById("forgotPasswordSuccessBox");
    document.getElementById("forgotPasswordSuccessContent").innerText = message;
    successBox.classList.remove("pop-out");
    successBox.classList.add("pop-in");
    successBox.style.display = "block";

    setTimeout(() => {
      successBox.classList.remove("pop-in");
      successBox.classList.add("pop-out");

      // Hide the dialog and refresh the page
      setTimeout(() => {
        successBox.style.display = "none";
        successBox.classList.remove("pop-in", "pop-out");
        window.location.reload(); // Refresh the browser
      }, 300);
    }, 3000);
  }

  // Function to show error dialog with pop-in and pop-out animation
  function forgotPasswordErrorBox(error) {
    const errorBox = document.getElementById("forgotPasswordErrorBox");
    document.getElementById("forgotPasswordErrorContent").innerText = error;
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

  // Function to show cooldown notification dialog with pop-in and pop-out animation
  function forgotPasswordCooldownBox(message) {
    const cooldownBox = document.getElementById("forgotPasswordCooldownBox");
    document.getElementById("forgotPasswordCooldownContent").innerText =
      message;
    cooldownBox.classList.remove("pop-out");
    cooldownBox.classList.add("pop-in");
    cooldownBox.style.display = "block";

    setTimeout(() => {
      cooldownBox.classList.remove("pop-in");
      cooldownBox.classList.add("pop-out");

      // Hide the dialog after the animation is done
      setTimeout(() => {
        cooldownBox.style.display = "none";
        cooldownBox.classList.remove("pop-in", "pop-out");
      }, 300);
    }, 3000);
  }

  // Show modal when Contact Us button is clicked
  contactUsButton.addEventListener("click", function (event) {
    event.preventDefault();
    contactUsModal.style.display = "block";
    setTimeout(() => {
      contactUsModal.classList.add("pop-in");
      document.querySelector(".modal-content").classList.add("pop-in");
    }, 10);
  });

  // Close modal when the close button is clicked
  closeContactUsModal.addEventListener("click", function () {
    document.querySelector(".modal-content").classList.add("pop-out");
    contactUsModal.classList.add("pop-out");
    setTimeout(() => {
      contactUsModal.style.display = "none";
      document.querySelector(".modal-content").classList.remove("pop-out");
      contactUsModal.classList.remove("pop-out");
    }, 300);
  });

  // Close modal when clicking outside of the modal content
  window.addEventListener("click", function (event) {
    if (event.target === contactUsModal) {
      document.querySelector(".modal-content").classList.add("pop-out");
      contactUsModal.classList.add("pop-out");
      setTimeout(() => {
        contactUsModal.style.display = "none";
        document.querySelector(".modal-content").classList.remove("pop-out");
        contactUsModal.classList.remove("pop-out");
      }, 300);
    }
  });

  // Handle form submission
  const contactUsForm = document.getElementById("contactUsForm");
  contactUsForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(contactUsForm);

    fetch("/contact_us/", {
      method: "POST",
      body: JSON.stringify({
        name: formData.get("name"),
        email: formData.get("email"),
        subject: formData.get("subject"),
        message: formData.get("message"),
      }),
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("Your message has been sent successfully!");
          contactUsModal.style.display = "none";
          contactUsForm.reset();
        } else {
          alert("There was an error sending your message. Please try again.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("There was an error sending your message. Please try again.");
      });
  });
  // Added back button functionality
  const backButton = document.getElementById("backButton");
  if (backButton) {
    backButton.addEventListener("click", function () {
      window.location.href = "/";
    });
  }

  // Function to add pop animation to status detail
  function addPopAnimation() {
    const statusDetailContainer = document.querySelector(
      ".status-detail-container"
    );
    if (statusDetailContainer) {
      statusDetailContainer.classList.add("pop-in");
    }
  }

  addPopAnimation();

  // Auto-mention the username in the reply form when clicking the reply label
  const replyLabels = document.querySelectorAll(".reply-label");

  replyLabels.forEach((label) => {
    label.addEventListener("click", function () {
      const replyId = this.getAttribute("data-reply-id");
      const replyForm = document.getElementById(`replyForm-${replyId}`);
      const username = this.getAttribute("data-username");
      const level = parseInt(this.getAttribute("data-level"));

      // Show the reply form
      if (
        replyForm.style.display === "none" ||
        replyForm.style.display === ""
      ) {
        replyForm.style.display = "block";
      } else {
        replyForm.style.display = "none";
      }

      // Insert the mentioned username at the beginning of the textarea
      const textarea = replyForm.querySelector("textarea");
      textarea.value = `@${username} `; // Mention the user
      textarea.focus(); // Auto-focus on the textarea
    });
  });

  // Handle reply submission with AJAX
  const submitReplyButtons = document.querySelectorAll(".submit-reply");

  submitReplyButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const replyId = this.getAttribute("data-reply-id");
      const level = parseInt(this.getAttribute("data-level"));
      const replyForm = document.getElementById(`replyForm-${replyId}`);
      const textarea = replyForm.querySelector("textarea");
      const replyText = textarea.value;

      // Use AJAX to submit the reply without reloading the page
      const statusId = document
        .querySelector(".status-detail-container")
        .getAttribute("data-status-id");

      let parentReplyId = replyId;

      // If level is 3, we should not create further nesting
      if (level >= 3) {
        parentReplyId = null; // Do not pass parent reply ID to prevent nesting
      }

      // Build the URL accordingly
      let url = `/add_reply/${statusId}/`;
      if (parentReplyId) {
        url += `${parentReplyId}/`;
      }

      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": "{{ csrf_token }}",
        },
        body: JSON.stringify({ text: replyText }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Append the new reply to the DOM
            // Depending on the level, we need to insert the new reply in the appropriate place
            if (level >= 3) {
              // Append the reply as a Level 3 reply (without further nesting)
              const nestedRepliesContainer =
                replyForm.closest(".nested-replies");
              const newReply = `
              <div class="reply nested-reply level-3" id="reply-${data.reply.id}">
                <img src="${data.reply.avatar_url}" alt="Avatar" class="reply-avatar" />
                <div class="reply-content">
                  <strong>${data.reply.username}</strong>
                  <p>${data.reply.text}</p>
                  <div class="reply-footer">
                    <span class="reply-timestamp">${data.reply.created_at}</span>
                    <span class="reply-label" data-reply-id="${data.reply.id}" data-username="${data.reply.username}" data-level="3">Reply</span>
                  </div>
                  <!-- Reply Form -->
                  <div class="reply-form-container" id="replyForm-${data.reply.id}" style="display: none;">
                    <textarea placeholder="Write a reply..."></textarea>
                    <button class="submit-reply" data-reply-id="${data.reply.id}" data-level="3">Submit Reply</button>
                  </div>
                </div>
              </div>
              `;
              nestedRepliesContainer.insertAdjacentHTML("beforeend", newReply);
            } else {
              // For levels less than 3, append the reply as a nested reply
              const nestedRepliesContainer = document.getElementById(
                `nestedReplies-${replyId}`
              );
              const newReply = `
              <div class="reply nested-reply level-${level + 1}" id="reply-${
                data.reply.id
              }">
                <img src="${
                  data.reply.avatar_url
                }" alt="Avatar" class="reply-avatar" />
                <div class="reply-content">
                  <strong>${data.reply.username}</strong>
                  <p>${data.reply.text}</p>
                  <div class="reply-footer">
                    <span class="reply-timestamp">${
                      data.reply.created_at
                    }</span>
                    <span class="reply-label" data-reply-id="${
                      data.reply.id
                    }" data-username="${data.reply.username}" data-level="${
                level + 1
              }">Reply</span>
                  </div>
                  <!-- Reply Form -->
                  <div class="reply-form-container" id="replyForm-${
                    data.reply.id
                  }" style="display: none;">
                    <textarea placeholder="Write a reply..."></textarea>
                    <button class="submit-reply" data-reply-id="${
                      data.reply.id
                    }" data-level="${level + 1}">Submit Reply</button>
                  </div>
                </div>
                <!-- Nested Replies Container -->
                <div class="nested-replies" id="nestedReplies-${
                  data.reply.id
                }"></div>
              </div>
              `;
              nestedRepliesContainer.insertAdjacentHTML("beforeend", newReply);
            }

            // Clear the textarea after submission
            textarea.value = "";
            replyForm.style.display = "none";

            // Re-attach event listeners to new elements
            attachReplyLabelListeners();
            attachSubmitReplyListeners();
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });

  // Functions to re-attach event listeners
  function attachReplyLabelListeners() {
    const replyLabels = document.querySelectorAll(".reply-label");
    replyLabels.forEach((label) => {
      if (!label.hasAttribute("data-listener-attached")) {
        label.addEventListener("click", function () {
          // Same logic as above
        });
        label.setAttribute("data-listener-attached", "true");
      }
    });
  }

  function attachSubmitReplyListeners() {
    const submitReplyButtons = document.querySelectorAll(".submit-reply");

    submitReplyButtons.forEach((button) => {
      if (!button.hasAttribute("data-listener-attached")) {
        button.addEventListener("click", function () {
          const replyId = this.getAttribute("data-reply-id");
          const level = parseInt(this.getAttribute("data-level"));
          const replyForm = document.getElementById(`replyForm-${replyId}`);
          const textarea = replyForm.querySelector("textarea");
          const replyText = textarea.value;

          // Use AJAX to submit the reply without reloading the page
          const statusId = document
            .querySelector(".status-detail-container")
            .getAttribute("data-status-id");

          let parentReplyId = replyId;

          // If level is 3, we should not create further nesting
          if (level >= 3) {
            parentReplyId = null; // Do not pass parent reply ID to prevent nesting
          }

          // Build the URL accordingly
          let url = `/add_reply/${statusId}/`;
          if (parentReplyId) {
            url += `${parentReplyId}/`;
          }

          fetch(url, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": "{{ csrf_token }}",
            },
            body: JSON.stringify({ text: replyText }),
          })
            .then((response) => response.json())
            .then((data) => {
              if (data.success) {
                // Append the new reply to the DOM
                let newReplyHtml = "";
                if (level >= 3) {
                  // Append the reply as a Level 3 reply (without further nesting)
                  const nestedRepliesContainer =
                    replyForm.closest(".nested-replies");
                  newReplyHtml = `
                  <div class="reply nested-reply level-3" id="reply-${data.reply.id}">
                    <img src="${data.reply.avatar_url}" alt="Avatar" class="reply-avatar" />
                    <div class="reply-content">
                      <strong>${data.reply.username}</strong>
                      <p>${data.reply.text}</p>
                      <div class="reply-footer">
                        <span class="reply-timestamp">${data.reply.created_at}</span>
                        <span class="reply-label" data-reply-id="${data.reply.id}" data-username="${data.reply.username}" data-level="3">Reply</span>
                      </div>
                      <!-- Reply Form -->
                      <div class="reply-form-container" id="replyForm-${data.reply.id}" style="display: none; position: relative;">
                        <textarea placeholder="Write a reply..."></textarea>
                        <div class="mention-autocomplete" id="mentionAutocomplete-${data.reply.id}"></div>
                        <button class="submit-reply" data-reply-id="${data.reply.id}" data-level="3">Submit Reply</button>
                      </div>
                    </div>
                  </div>
                  `;
                  nestedRepliesContainer.insertAdjacentHTML(
                    "beforeend",
                    newReplyHtml
                  );
                } else {
                  // For levels less than 3, append the reply as a nested reply
                  const nestedRepliesContainer = document.getElementById(
                    `nestedReplies-${replyId}`
                  );
                  newReplyHtml = `
                  <div class="reply nested-reply level-${
                    level + 1
                  }" id="reply-${data.reply.id}">
                    <img src="${
                      data.reply.avatar_url
                    }" alt="Avatar" class="reply-avatar" />
                    <div class="reply-content">
                      <strong>${data.reply.username}</strong>
                      <p>${data.reply.text}</p>
                      <div class="reply-footer">
                        <span class="reply-timestamp">${
                          data.reply.created_at
                        }</span>
                        <span class="reply-label" data-reply-id="${
                          data.reply.id
                        }" data-username="${data.reply.username}" data-level="${
                    level + 1
                  }">Reply</span>
                      </div>
                      <!-- Reply Form -->
                      <div class="reply-form-container" id="replyForm-${
                        data.reply.id
                      }" style="display: none; position: relative;">
                        <textarea placeholder="Write a reply..."></textarea>
                        <div class="mention-autocomplete" id="mentionAutocomplete-${
                          data.reply.id
                        }"></div>
                        <button class="submit-reply" data-reply-id="${
                          data.reply.id
                        }" data-level="${level + 1}">Submit Reply</button>
                      </div>
                    </div>
                    <!-- Nested Replies Container -->
                    <div class="nested-replies" id="nestedReplies-${
                      data.reply.id
                    }"></div>
                  </div>
                  `;
                  nestedRepliesContainer.insertAdjacentHTML(
                    "beforeend",
                    newReplyHtml
                  );
                }

                // Clear the textarea after submission
                textarea.value = "";
                replyForm.style.display = "none";

                // Re-attach event listeners to new elements
                attachReplyLabelListeners();
                attachSubmitReplyListeners();
                reinitializeAutocomplete();

                // **Auto-scroll to the new reply**
                const newReplyElement = document.getElementById(
                  `reply-${data.reply.id}`
                );
                if (newReplyElement) {
                  newReplyElement.scrollIntoView({
                    behavior: "smooth",
                    block: "start",
                  });
                }
              } else {
                // Handle error (e.g., display error message)
                alert(
                  data.error || "An error occurred while submitting your reply."
                );
              }
            })
            .catch((error) => {
              console.error("Error:", error);
            });
        });
        button.setAttribute("data-listener-attached", "true");
      }
    });
  }
  function initMentionAutocomplete(textarea, autocompleteContainer) {
    let cursorPosition = 0;
    let mentionQuery = "";
    let mentionStartPos = -1;

    textarea.addEventListener("keyup", function (event) {
      const caretPosition = textarea.selectionStart;
      const text = textarea.value;
      const char = event.key;

      // Check if '@' is typed
      if (char === "@") {
        mentionStartPos = caretPosition - 1;
        mentionQuery = "";
        showAutocomplete();
      } else if (mentionStartPos >= 0) {
        // If we are in a mention query
        if (event.key === "Backspace") {
          if (caretPosition <= mentionStartPos) {
            // Cursor moved before the mention start, cancel mention
            hideAutocomplete();
            mentionStartPos = -1;
            mentionQuery = "";
            return;
          } else {
            mentionQuery = text.substring(mentionStartPos + 1, caretPosition);
          }
        } else if (event.key.length === 1) {
          mentionQuery = text.substring(mentionStartPos + 1, caretPosition);
        } else if (
          event.key === "ArrowUp" ||
          event.key === "ArrowDown" ||
          event.key === "Enter"
        ) {
          // Handle these keys in keydown event
          return;
        } else {
          mentionQuery = text.substring(mentionStartPos + 1, caretPosition);
        }

        if (mentionQuery.length > 0) {
          fetchUsernames(mentionQuery);
        } else {
          hideAutocomplete();
        }
      }
    });

    // Handle keydown for navigation in the autocomplete
    textarea.addEventListener("keydown", function (event) {
      if (autocompleteContainer.style.display === "block") {
        if (event.key === "ArrowDown") {
          event.preventDefault();
          moveSelection(1);
        } else if (event.key === "ArrowUp") {
          event.preventDefault();
          moveSelection(-1);
        } else if (event.key === "Enter") {
          event.preventDefault();
          selectUsername();
        }
      }
    });

    // Fetch usernames from server
    function fetchUsernames(query) {
      fetch(`/get_usernames/?q=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => {
          showAutocomplete(data.usernames);
        })
        .catch((error) => {
          console.error("Error fetching usernames:", error);
        });
    }

    // Show autocomplete suggestions
    function showAutocomplete(usernames = []) {
      if (usernames.length === 0) {
        hideAutocomplete();
        return;
      }

      autocompleteContainer.innerHTML = "<ul></ul>";
      const ul = autocompleteContainer.querySelector("ul");

      usernames.forEach((username, index) => {
        const li = document.createElement("li");
        li.textContent = username;
        li.dataset.index = index;
        li.addEventListener("mousedown", function (e) {
          e.preventDefault(); // Prevent textarea from losing focus
          selectUsername(username);
        });
        ul.appendChild(li);
      });

      autocompleteContainer.style.display = "block";
      setActiveItem(0);
    }

    // Hide autocomplete suggestions
    function hideAutocomplete() {
      autocompleteContainer.style.display = "none";
      autocompleteContainer.innerHTML = "";
    }

    let activeIndex = -1;

    function moveSelection(direction) {
      const items = autocompleteContainer.querySelectorAll("li");
      if (items.length === 0) return;

      activeIndex += direction;

      if (activeIndex < 0) activeIndex = items.length - 1;
      if (activeIndex >= items.length) activeIndex = 0;

      setActiveItem(activeIndex);
    }

    function setActiveItem(index) {
      const items = autocompleteContainer.querySelectorAll("li");
      items.forEach((item, idx) => {
        if (idx === index) {
          item.classList.add("active");
        } else {
          item.classList.remove("active");
        }
      });
    }

    function selectUsername(username = null) {
      const items = autocompleteContainer.querySelectorAll("li");
      if (!username && activeIndex >= 0 && activeIndex < items.length) {
        username = items[activeIndex].textContent;
      }
      if (username) {
        const beforeMention = textarea.value.substring(0, mentionStartPos);
        const afterMention = textarea.value.substring(textarea.selectionStart);
        textarea.value = `${beforeMention}@${username} ${afterMention}`;
        const newCaretPosition = beforeMention.length + username.length + 2;
        textarea.setSelectionRange(newCaretPosition, newCaretPosition);
        hideAutocomplete();
        mentionStartPos = -1;
        mentionQuery = "";
      }
    }

    // Click outside to hide autocomplete
    document.addEventListener("click", function (event) {
      if (
        !autocompleteContainer.contains(event.target) &&
        event.target !== textarea
      ) {
        hideAutocomplete();
      }
    });
  }

  // Initialize autocomplete for all reply textareas
  function initializeAllAutocomplete() {
    const replyForms = document.querySelectorAll(".reply-form-container");
    replyForms.forEach((form) => {
      const textarea = form.querySelector("textarea");
      const autocompleteContainer = form.querySelector(".mention-autocomplete");
      initMentionAutocomplete(textarea, autocompleteContainer);
    });

    // Initialize for the main reply form
    const mainTextarea = document.querySelector("#replyFormMain textarea");
    const mainAutocompleteContainer = document.querySelector(
      "#mentionAutocompleteMain"
    );
    if (mainTextarea && mainAutocompleteContainer) {
      initMentionAutocomplete(mainTextarea, mainAutocompleteContainer);
    }
  }

  initializeAllAutocomplete();

  // Re-initialize autocomplete when new reply forms are added dynamically
  function reinitializeAutocomplete() {
    // Remove existing autocomplete initialization to prevent duplicates
    const replyForms = document.querySelectorAll(".reply-form-container");
    replyForms.forEach((form) => {
      const textarea = form.querySelector("textarea");
      textarea.replaceWith(textarea.cloneNode(true));
    });
    initializeAllAutocomplete();
  }

  categoryElements.forEach((categoryElement) => {
    categoryElement.addEventListener("click", function () {
      categoryElements.forEach((el) =>
        el.querySelector("span").classList.remove("active")
      );
      this.querySelector("span").classList.add("active");
      activeCategory = this.id;
      page = 1;
      document.getElementById("boxContainer").innerHTML = "";
      fetchStatuses(page, activeCategory);
    });
  });

  // Fetch initial statuses
  fetchStatuses(page, activeCategory);

  // Add scroll event listener for infinite scrolling
  window.addEventListener("scroll", () => {
    if (
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 &&
      !isLoading &&
      hasNext
    ) {
      page++;
      fetchStatuses(page);
    }
  });

  // Show loader and overlay
  function showLoader() {
    statusLoader.style.display = "block";
  }

  // Hide loader and overlay
  function hideLoader() {
    statusLoader.style.display = "none";
  }

  feelingIcons.forEach((icon) => {
    icon.addEventListener("click", () => {
      feelingIcons.forEach((i) => i.classList.remove("active"));
      icon.classList.add("active");
      selectedEmotion = icon.querySelector("img").alt;
      saveFormData();
    });
  });

  statusTitle.addEventListener("input", saveFormData);
  statusDescription.addEventListener("input", saveFormData);

  // Show the profanity error modal with overlay
  function showProfanityError(message) {
    const dialogBox = document.getElementById("profanityErrorModal");
    const dialogContent = document.getElementById("profanityErrorContent");
    const overlay = document.getElementById("profanityErrorOverlay");

    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    overlay.style.display = "block";

    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");
  }

  // Event listener to close the profanity error modal when the close button is clicked
  document
    .getElementById("closeProfanityModal")
    .addEventListener("click", function () {
      const dialogBox = document.getElementById("profanityErrorModal");
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    });

  // Close the profanity error modal
  function closeProfanityErrorModal() {
    const dialogBox = document.getElementById("profanityErrorModal");
    const overlay = document.getElementById("profanityErrorOverlay");

    dialogBox.classList.remove("pop-in");
    dialogBox.classList.add("pop-out");
    setTimeout(() => {
      dialogBox.style.display = "none";
      dialogBox.classList.remove("pop-out");
      overlay.style.display = "none";
    }, 300);
  }

  // Show the guidelines modal
  function showGuidelinesModal() {
    const guidelinesModal = document.getElementById("guidelinesModal");
    const guidelinesOverlay = document.getElementById("guidelinesOverlay");

    guidelinesModal.style.display = "block";
    guidelinesOverlay.style.display = "block";

    guidelinesModal.classList.remove("pop-out");
    guidelinesModal.classList.add("pop-in");
  }

  // Close the guidelines modal
  function closeGuidelinesModal() {
    const guidelinesModal = document.getElementById("guidelinesModal");
    const guidelinesOverlay = document.getElementById("guidelinesOverlay");

    guidelinesModal.classList.remove("pop-in");
    guidelinesModal.classList.add("pop-out");
    setTimeout(() => {
      guidelinesModal.style.display = "none";
      guidelinesModal.classList.remove("pop-out");
      guidelinesOverlay.style.display = "none";
    }, 300);
  }

  // Event listener to close the profanity error modal when the close button is clicked
  document
    .getElementById("closeProfanityModal")
    .addEventListener("click", closeProfanityErrorModal);

  // Event listener to close the profanity error modal when the overlay is clicked
  document
    .getElementById("profanityErrorOverlay")
    .addEventListener("click", closeProfanityErrorModal);

  // Event listener to show the guidelines modal when the guidelines text is clicked
  document
    .getElementById("showGuidelines")
    .addEventListener("click", showGuidelinesModal);

  // Event listener to close the guidelines modal when the close button is clicked
  document
    .getElementById("closeGuidelinesModal")
    .addEventListener("click", closeGuidelinesModal);

  // Event listener to close the guidelines modal when the overlay is clicked
  document
    .getElementById("guidelinesOverlay")
    .addEventListener("click", closeGuidelinesModal);

  function convertNewLinesToSpaces(text) {
    return text.replace(/\n/g, " ");
  }

  document.getElementById("description").addEventListener("input", function () {
    const descriptionElement = document.getElementById("description");
    const plainDescription = descriptionElement.textContent;
    const tokenCount = countTokens(plainDescription);

    if (tokenCount > 512) {
      showStatusError("The description exceeds the 512 token limit.");
      // Trim the content to the 512-token limit
      const trimmedText = plainDescription.split(/\s+/).slice(0, 512).join(" ");
      descriptionElement.textContent = trimmedText;
      // Move cursor to the end after trimming
      moveCursorToEnd(descriptionElement);
      updateCounters(); // Update the counters after trimming
    } else {
      updateCounters(); // Update the counters normally
    }
  });

  //   if (tokenCount > 512) {
  //     showSuggestDiary();
  //     // Trim the content to the 512-token limit
  //     const trimmedText = plainDescription.split(/\s+/).slice(0, 512).join(" ");
  //     descriptionElement.textContent = trimmedText;
  //     moveCursorToEnd(descriptionElement);
  //     updateCounters(); // Update the counters after trimming
  //   } else {
  //     updateCounters(); // Update the counters normally
  //   }
  // });

  function moveCursorToEnd(element) {
    const range = document.createRange();
    const selection = window.getSelection();
    range.selectNodeContents(element);
    range.collapse(false);
    selection.removeAllRanges();
    selection.addRange(range);
    element.focus();
  }

  // Event listener to handle paste events
  document
    .getElementById("description")
    .addEventListener("paste", function (event) {
      handlePasteEvent(event);
    });

  // Event listener to handle drop events
  document
    .getElementById("description")
    .addEventListener("drop", function (event) {
      event.preventDefault(); // Prevent default drop behavior
      showStatusError(
        "Only text is allowed. Please do not drag and drop files or images."
      );
    });

  // Preventing drag over behavior to avoid confusion
  document
    .getElementById("description")
    .addEventListener("dragover", function (event) {
      event.preventDefault(); // Prevent default drag behavior
    });

  function handlePasteEvent(event) {
    const clipboardData = event.clipboardData || window.clipboardData;
    const items = clipboardData.items;

    // Check if any of the items are not text
    for (let i = 0; i < items.length; i++) {
      if (items[i].kind !== "string") {
        event.preventDefault(); // Prevent the paste
        showStatusError(
          "Only text is allowed. Please do not paste images, PDFs, or other files."
        );
        return;
      }
    }

    // If only text is being pasted, check the token limit
    setTimeout(() => {
      const descriptionElement = document.getElementById("description");
      const plainDescription = descriptionElement.textContent;
      const tokenCount = countTokens(plainDescription);

      if (tokenCount > 512) {
        showStatusError("The description exceeds the 512 token limit.");
        // Trim the content to the 512-token limit
        const trimmedText = plainDescription
          .split(/\s+/)
          .slice(0, 512)
          .join(" ");
        descriptionElement.textContent = trimmedText;
        moveCursorToEnd(descriptionElement);
        updateCounters(); // Update the counters after trimming
      } else {
        updateCounters(); // Update the counters normally
      }
    }, 0);
  }

  document
    .getElementById("description")
    .addEventListener("paste", function (event) {
      event.preventDefault();

      // Get plain text from the clipboard
      const text = (event.clipboardData || window.clipboardData).getData(
        "text/plain"
      );

      // Count the number of tokens in the pasted text
      const tokenCount = countTokens(text);
      const currentTokens = countTokens(
        document.getElementById("description").textContent
      );

      if (tokenCount + currentTokens > 512) {
        showStatusError("Pasting this text exceeds the 512 token limit.");
        return;
      }

      // Insert the plain text at the cursor position
      insertTextAtCursor(text);

      // Update the counters
      updateCounters();
    });

  // Utility function to insert text at the cursor position
  function insertTextAtCursor(text) {
    const selection = window.getSelection();
    if (!selection.rangeCount) return;

    const range = selection.getRangeAt(0);
    range.deleteContents();

    const textNode = document.createTextNode(text);
    range.insertNode(textNode);

    // Move the cursor to the end of the inserted text
    range.setStartAfter(textNode);
    selection.removeAllRanges();
    selection.addRange(range);
  }

  // Function to count tokens (assuming tokens are separated by spaces)
  function countTokens(text) {
    return text.split(/\s+/).filter(Boolean).length;
  }

  // Function to count words (splitting by spaces and filtering empty entries)
  function countWords(text) {
    return text.split(/\s+/).filter(Boolean).length; // Same logic as counting tokens
  }

  // Update the token and character count
  function updateCounters() {
    const descriptionElement = document.getElementById("description");

    // Check if the description is showing the placeholder; if so, ignore counting
    if (descriptionElement.classList.contains("placeholder")) {
      document.getElementById("characterCount").textContent = `0 characters`;
      document.getElementById("wordCount").textContent = `0 words`;
      document.getElementById("tokenCount").textContent = `0 tokens`;
      return;
    }

    // Get the text content of the description (ignoring placeholder)
    const plainDescription = descriptionElement.textContent.trim();

    // Update the counts
    const characterCount = plainDescription.length;
    const wordCount = countWords(plainDescription);
    const tokenCount = countTokens(plainDescription);

    // Update the DOM elements with the counts
    document.getElementById(
      "characterCount"
    ).textContent = `${characterCount} characters`;
    document.getElementById("wordCount").textContent = `${wordCount} words`;
    document.getElementById("tokenCount").textContent = `${tokenCount} tokens`;

    // If token count exceeds the limit, show the max token count
    if (tokenCount > 512) {
      document.getElementById(
        "tokenCount"
      ).textContent = `512 tokens (Max reached)`;
    }
  }
  // Add event listener to update counters on input
  document
    .getElementById("description")
    .addEventListener("input", updateCounters);
  // Add event listeners to update counters on input
  document
    .getElementById("description")
    .addEventListener("input", updateCounters);
  document
    .getElementById("description")
    .addEventListener("paste", function (e) {
      setTimeout(updateCounters, 0); // Update counters after paste
    });

  // Initial count update
  updateCounters();

  // Updated event listener for status form submission
  statusForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const title = statusTitle.value.trim();
    const description = statusDescription.classList.contains("placeholder")
      ? ""
      : statusDescription.textContent.trim();
    const plainDescription = description.replace(/\n+/g, " ");
    const tokenCount = countTokens(plainDescription);

    if (!selectedEmotion) {
      showStatusError("Choose your emotion label.");
      return;
    }

    if (!title) {
      showStatusError("Choose a title for this status.");
      return;
    }

    if (!description) {
      showStatusError("Write what you feel in the description.");
      return;
    }

    if (tokenCount > 512) {
      showStatusError("The description exceeds the 512 token limit.");
      return;
    }

    // Show confirmation dialog with pop-in animation
    confirmStatusModal.style.display = "block";
    setTimeout(() => {
      confirmStatusModal.classList.add("pop-in");
    }, 10);
  });

  confirmBtn.addEventListener("click", function () {
    const title = statusTitle.value.trim();
    const description = statusDescription.classList.contains("placeholder")
      ? ""
      : statusDescription.innerHTML.trim();
    const plainDescription = statusDescription.textContent
      .trim()
      .replace(/\n+/g, " ");

    // Hide confirmation dialog with pop-out animation
    confirmStatusModal.classList.remove("pop-in");
    confirmStatusModal.classList.add("pop-out");
    setTimeout(() => {
      confirmStatusModal.style.display = "none";
      confirmStatusModal.classList.remove("pop-out");

      // Proceed with profanity check
      fetch("/check_profanity/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          title: title,
          description: plainDescription,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.contains_profanity) {
            showProfanityError("Your post contains inappropriate content.");
          } else {
            // Proceed with status submission
            uploadStatus(title, description, plainDescription);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          showStatusError("Network error could not check profanity.");
        });
    }, 300);
  });

  cancelBtn.addEventListener("click", function () {
    // Hide confirmation dialog with pop-out animation
    confirmStatusModal.classList.remove("pop-in");
    confirmStatusModal.classList.add("pop-out");
    setTimeout(() => {
      confirmStatusModal.style.display = "none";
      confirmStatusModal.classList.remove("pop-out");
    }, 300);
  });

  function uploadStatus(title, description, plainDescription) {
    const csrfToken = document.querySelector(
      'input[name="csrfmiddlewaretoken"]'
    ).value;

    showLoader();
    statusModal.querySelector(".status-form").style.opacity = "0.5";

    fetch("/submit_status/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        emotion: selectedEmotion,
        title: title,
        description: description,
        plain_description: plainDescription,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        hideLoader();
        statusModal.querySelector(".status-form").style.opacity = "1";

        if (data.success) {
          showStatusSuccess("Status shared successfully!");
          setTimeout(() => {
            const dialogBox = document.getElementById(
              "statusNotificationSuccess"
            );
            dialogBox.classList.remove("pop-in");
            dialogBox.classList.add("pop-out");
            setTimeout(() => {
              dialogBox.style.display = "none";
              dialogBox.classList.remove("pop-out");

              // Hide the status modal with animation
              statusModal.classList.remove("pop-in");
              statusModal.classList.add("pop-out");
              setTimeout(() => {
                statusModal.style.display = "none";
                statusModal.classList.remove("pop-out");

                // Reload the page after both animations complete
                window.location.reload();
              }, 300); // Duration of the status modal pop-out animation
            }, 300); // Duration of the success dialog pop-out animation
          }, 3000); // Duration to show the success message
        } else {
          showStatusError(
            "Failed to share status: " + JSON.stringify(data.errors)
          );
        }
      })
      .catch((error) => {
        hideLoader();
        statusModal.querySelector(".status-form").style.opacity = "1";
        console.error("Error:", error);
        showStatusError("Network error could not upload.");
      });
  }

  function fetchStatuses(page, category) {
    isLoading = true;
    const statusLoader = document.getElementById("statusLoader");
    const statusOverlay = document.getElementById("statusOverlay");

    statusLoader.style.display = "block";
    statusOverlay.style.display = "block";

    fetch(`/get_all_statuses/?page=${page}&category=${category}`)
      .then((response) => response.json())
      .then((data) => {
        isLoading = false;
        statusLoader.style.display = "none";
        statusOverlay.style.display = "none";
        const container = document.getElementById("boxContainer");

        data.statuses.forEach((status) => {
          const newBox = document.createElement("div");
          newBox.classList.add("box5", "pop");
          newBox.innerHTML = `
                  <div class="avatar-content">
                      <a href="/status/${status.id}/">
                          <img src="${
                            status.avatar_url
                          }" alt="Avatar" class="circle-avatar-placeholder" />
                      </a>
                      <p class="username-placeholder">${status.username}</p>
                  </div>
                  <div class="content">
                      <a href="/status/${status.id}/">
                          <h2 class="title-placeholder">${status.title}</h2>
                          <p class="description-placeholder">${truncateText(
                            status.plain_description
                          )}</p>
                      </a>
                      <span class="time-stamp time-stamp-placeholder">${
                        status.created_at
                      } ago</span>
                      <span class="feelings feelings-placeholder">${getEmotionIcon(
                        status.emotion
                      )} ${mapEmotion(status.emotion)}</span>
                      <span class="replies replies-placeholder">${
                        status.replies
                      } ${status.replies === 1 ? "Reply" : "Replies"}</span>
                      ${
                        status.can_delete
                          ? `
                            <button id="edit-${status.id}" class="edit-button status">
                              <i class='bx bx-edit'></i>
                            </button>
                            <button id="delete-${status.id}" class="delete-button status">
                              <i class='bx bxs-trash bx-flip-horizontal'></i>
                            </button>`
                          : ""
                      }
                      ${
                        !status.can_delete
                          ? `<button id="refer-${status.id}" class="refer-button status"><i class='bx bxs-user-voice bx-tada'></i></button>`
                          : ""
                      }
                  </div>
              `;
          container.appendChild(newBox);

          if (status.can_delete) {
            document
              .getElementById(`delete-${status.id}`)
              .addEventListener("click", function () {
                deleteStatus(status.id);
              });

            // Add event listener for the edit button
            document
              .getElementById(`edit-${status.id}`)
              .addEventListener("click", function () {
                editStatus(status.id);
              });
          } else {
            document
              .getElementById(`refer-${status.id}`)
              .addEventListener("click", function () {
                referStatusToCounselor(status.id);
              });
          }

          newBox.addEventListener("animationend", function () {
            newBox.classList.remove("pop");
          });
        });

        hasNext = data.has_next;
      })
      .catch((error) => {
        isLoading = false;
        statusLoader.style.display = "none";
        statusOverlay.style.display = "none";
        console.error("Error fetching statuses:", error);
      });
  }

  document
    .getElementById("referralReason")
    .addEventListener("change", function () {
      const otherReasonContainer = document.getElementById(
        "otherReasonContainer"
      );
      if (this.value === "Other Concerns") {
        otherReasonContainer.style.display = "block";
      } else {
        otherReasonContainer.style.display = "none";
      }
    });

  let undoStack = []; // Stack to keep track of the last highlight for undo

  // Function to open the modal and fetch status data with animation
  function referStatusToCounselor(statusId) {
    fetch(`/get_status/${statusId}/`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          document.getElementById("referStatusTitle").textContent =
            data.status.title;
          document.getElementById("referStatusDescription").textContent =
            data.status.plain_description;

          const modalContent = document.getElementById("refercontent");
          const modalOverlay = document.getElementById("referralModalOverlay");

          // Display the modal overlay and content with animations
          modalOverlay.style.display = "block";
          modalOverlay.classList.remove("fade-out");
          modalOverlay.classList.add("fade-in");

          modalContent.style.display = "block";
          modalContent.classList.remove("pop-out");
          modalContent.classList.add("pop-in");

          enableCustomHighlighting("referStatusTitle");
          enableCustomHighlighting("referStatusDescription");

          document.getElementById("submitReferStatus").onclick = function () {
            showReferralConfirmation(statusId);
          };

          document.getElementById("clearHighlights").onclick = function () {
            clearAllHighlights();
          };

          document.getElementById("highlightAllTitle").onclick = function () {
            highlightAllText("referStatusTitle");
          };

          document.getElementById("highlightAllDescription").onclick =
            function () {
              highlightAllText("referStatusDescription");
            };

          document.addEventListener("keydown", handleUndoHighlight);
        } else {
          alert("Failed to load status data.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Error fetching status data. Please try again.");
      });
  }

  // Function to close the modal with animation (Renamed from closeModal)
  function closeReferModal() {
    const modalContent = document.getElementById("refercontent");
    const modalOverlay = document.getElementById("referralModalOverlay");

    modalContent.classList.remove("pop-in");
    modalContent.classList.add("pop-out");

    modalOverlay.classList.remove("fade-in");
    modalOverlay.classList.add("fade-out");

    // Wait for the animation to finish before hiding the modal content
    setTimeout(() => {
      modalContent.style.display = "none";
      modalOverlay.style.display = "none";
      document.removeEventListener("keydown", handleUndoHighlight);
    }, 300); // Match the duration of the popOut animation
  }

  // Close modal when the close button is clicked
  document.getElementById("closeReferStatusModal").onclick = function () {
    closeReferModal();
  };

  // Function to enable custom highlighting
  function enableCustomHighlighting(elementId) {
    const element = document.getElementById(elementId);

    element.addEventListener("mouseup", function () {
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);

        if (range && element.contains(range.commonAncestorContainer)) {
          if (!rangeIsWithinHighlightedText(range)) {
            wrapSelectedTextWithHighlight(range);
          }
          selection.removeAllRanges(); // Clear the selection
        }
      }
    });
  }

  // Function to check if the selection range is valid (doesn't include spaces)
  function isValidHighlight(range, originalText) {
    const selectedText = range.toString();
    const startOffset = originalText.indexOf(selectedText);

    // Check if the selected text matches exactly with the original text slice
    return (
      startOffset !== -1 &&
      selectedText.trim() !== "" &&
      originalText.slice(startOffset, startOffset + selectedText.length) ===
        selectedText
    );
  }

  // Function to wrap selected text or merge with adjacent highlights
  function mergeOrWrapSelectedText(range) {
    const selectedText = range.toString().trim();
    if (selectedText !== "") {
      const startContainer = range.startContainer;
      const endContainer = range.endContainer;

      let startSpan =
        startContainer.nodeType === 3 ? startContainer.previousSibling : null;
      let endSpan =
        endContainer.nodeType === 3 ? endContainer.nextSibling : null;

      // Check if the range is adjacent to existing highlighted spans and there is no space between them
      if (
        startSpan &&
        startSpan.classList &&
        startSpan.classList.contains("highlighted-text")
      ) {
        const textBeforeRange = startSpan.textContent.slice(-1); // Last character of the previous span
        const textBetween = startContainer.textContent.slice(
          0,
          range.startOffset
        );

        if (textBetween.trim() === "" && !/\s/.test(textBeforeRange)) {
          startSpan.textContent += selectedText;
          range.deleteContents();
          return;
        }
      }

      if (
        endSpan &&
        endSpan.classList &&
        endSpan.classList.contains("highlighted-text")
      ) {
        const textAfterRange = endSpan.textContent.charAt(0); // First character of the next span
        const textBetween = endContainer.textContent.slice(range.endOffset);

        if (textBetween.trim() === "" && !/\s/.test(textAfterRange)) {
          endSpan.textContent = selectedText + endSpan.textContent;
          range.deleteContents();
          return;
        }
      }

      // Create new highlight if merging is not possible or spaces are between the selected text
      const span = document.createElement("span");
      span.className = "highlighted-text";
      span.textContent = selectedText;
      range.deleteContents(); // Remove the selected text
      range.insertNode(span); // Insert the highlighted text

      // Push the span element to the undo stack
      undoStack.push(span);
    }
  }

  // Function to check if the selection range is within already highlighted text
  function rangeIsWithinHighlightedText(range) {
    const startContainer = range.startContainer;
    const endContainer = range.endContainer;

    return (
      (startContainer.parentElement &&
        startContainer.parentElement.classList.contains("highlighted-text")) ||
      (endContainer.parentElement &&
        endContainer.parentElement.classList.contains("highlighted-text"))
    );
  }

  // Function to get highlighted text from the content
  function getHighlightedText(elementId) {
    const element = document.getElementById(elementId);
    const highlightedElements =
      element.getElementsByClassName("highlighted-text");
    let highlightedText = "";

    for (let i = 0; i < highlightedElements.length; i++) {
      highlightedText += highlightedElements[i].textContent + " ";
    }

    return highlightedText.trim();
  }

  // Function to wrap selected text with custom highlight without deleting text
  function wrapSelectedTextWithHighlight(range) {
    const selectedText = range.toString().trim();
    if (selectedText !== "") {
      const span = document.createElement("span");
      span.className = "highlighted-text";
      range.surroundContents(span);
      undoStack.push(span);
    }
  }

  // Function to prevent merging highlights if spaces are involved
  function preventMergeWithSpaces(span) {
    const prevSibling = span.previousSibling;
    const nextSibling = span.nextSibling;

    if (
      prevSibling &&
      prevSibling.nodeType === 3 &&
      /\s$/.test(prevSibling.textContent)
    ) {
      const newTextNode = document.createTextNode(
        prevSibling.textContent.trimEnd()
      );
      span.parentNode.insertBefore(newTextNode, span);
      prevSibling.textContent = " ";
    }

    if (
      nextSibling &&
      nextSibling.nodeType === 3 &&
      /^\s/.test(nextSibling.textContent)
    ) {
      const newTextNode = document.createTextNode(
        nextSibling.textContent.trimStart()
      );
      span.parentNode.insertBefore(span, nextSibling);
      nextSibling.textContent = " ";
    }
  }

  // Function to clear all highlights
  function clearHighlightsInElement(elementId) {
    const element = document.getElementById(elementId);
    const highlightedElements = element.querySelectorAll(".highlighted-text");
    highlightedElements.forEach((highlighted) => {
      const parent = highlighted.parentNode;
      parent.replaceChild(
        document.createTextNode(highlighted.textContent),
        highlighted
      );
      parent.normalize(); // Merge adjacent text nodes
    });
  }

  // Function to clear all highlights in both title and description
  function clearAllHighlights() {
    clearHighlightsInElement("referStatusTitle");
    clearHighlightsInElement("referStatusDescription");
    undoStack = []; // Clear the undo stack
  }

  // Function to highlight all text in an element, reapplying even if already highlighted
  function highlightAllText(elementId) {
    const element = document.getElementById(elementId);

    // First, clear all existing highlights within this specific element
    clearHighlightsInElement(elementId);

    // Then, create a new highlight across all text in this element
    const range = document.createRange();
    range.selectNodeContents(element);
    wrapSelectedTextWithHighlight(range);
  }

  // Function to handle undoing the last highlight (Ctrl + Z)
  function handleUndoHighlight(event) {
    if (event.ctrlKey && event.key === "z") {
      const lastHighlighted = undoStack.pop();
      if (lastHighlighted) {
        const parent = lastHighlighted.parentNode;
        const newTextNode = document.createTextNode(
          lastHighlighted.textContent
        );
        parent.replaceChild(newTextNode, lastHighlighted);
        parent.normalize(); // Merge adjacent text nodes
      }
    }
  }

  document.querySelectorAll(".refer-status-button").forEach((button) => {
    button.addEventListener("click", function () {
      const statusId = this.dataset.statusId;
      referStatusToCounselor(statusId);
    });
  });

  // Function to show the confirmation dialog
  function showReferralConfirmation(statusId) {
    const confirmationDialog = document.getElementById(
      "referralConfirmationDialog"
    );
    confirmationDialog.classList.remove("pop-out");
    confirmationDialog.classList.add("pop-in");
    confirmationDialog.style.display = "block";

    document.getElementById("confirmSubmitReferral").onclick = function () {
      confirmationDialog.classList.remove("pop-in");
      confirmationDialog.classList.add("pop-out");

      setTimeout(() => {
        confirmationDialog.style.display = "none";
        showReferralLoader();
        submitReferral(statusId);
      }, 300); // Match the duration of the pop-out animation
    };

    document.getElementById("cancelSubmitReferral").onclick = function () {
      confirmationDialog.classList.remove("pop-in");
      confirmationDialog.classList.add("pop-out");

      setTimeout(() => {
        confirmationDialog.style.display = "none";
      }, 300); // Match the duration of the pop-out animation
    };
  }

  // Function to show the loader and overlay
  function showReferralLoader() {
    const loader = document.getElementById("referralLoader");
    const overlay = document.getElementById("referralOverlay");

    loader.style.display = "block";
    overlay.style.display = "block";
  }

  // Function to hide the loader and overlay
  function hideReferralLoader() {
    const loader = document.getElementById("referralLoader");
    const overlay = document.getElementById("referralOverlay");

    loader.style.display = "none";
    overlay.style.display = "none";
  }
  // Function to submit the referral
  function submitReferral(statusId) {
    const highlightedTitle = getHighlightedText("referStatusTitle");
    const highlightedDescription = getHighlightedText("referStatusDescription");

    // Check if either title or description is highlighted
    if (!highlightedTitle && !highlightedDescription) {
      showHighlightError();
      return;
    }

    const referralReason = document.getElementById("referralReason").value;
    const otherReason = document.getElementById("otherReason").value;

    // Check if "Other Concerns" is selected but the textarea is empty
    if (referralReason === "Other Concerns" && otherReason.trim() === "") {
      showOtherReasonError();
      return;
    }

    const formData = new FormData();
    formData.append("highlightedTitle", highlightedTitle);
    formData.append("highlightedDescription", highlightedDescription);
    formData.append("referralReason", referralReason);
    if (referralReason === "Other Concerns") {
      formData.append("otherReason", otherReason);
    }

    showReferralLoader(); // Show the loading overlay

    fetch(`/refer_status/${statusId}/`, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
      .then((response) => response.json())
      .then((data) => {
        hideReferralLoader(); // Hide the loading overlay

        if (data.success) {
          showReferralSuccess();
        } else {
          showReferralError();
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        hideReferralLoader(); // Hide the loading overlay
        showReferralError();
      });
  }

  // Function to show error dialog when "Other Concerns" is selected but no reason is provided
  function showOtherReasonError() {
    hideReferralLoader(); // Hide the loading overlay (if active)

    const errorDialog = document.getElementById("referralErrorDialog");
    errorDialog.classList.remove("pop-out");
    errorDialog.classList.add("pop-in");
    errorDialog.style.display = "block";

    document.getElementById("referralErrorContent").textContent =
      "Please provide referral reasons for 'Other Concerns'.";

    setTimeout(() => {
      errorDialog.classList.remove("pop-in");
      errorDialog.classList.add("pop-out");

      // Hide the dialog after the animation is done
      setTimeout(() => {
        errorDialog.style.display = "none";
      }, 300); // Match the duration of the popOut animation
    }, 3000); // Dialog visible for 3 seconds
  }

  // Function to show error dialog when no highlight is provided
  function showHighlightError() {
    hideReferralLoader(); // Hide the loading overlay (if active)

    const errorDialog = document.getElementById("referralErrorDialog");
    errorDialog.classList.remove("pop-out");
    errorDialog.classList.add("pop-in");
    errorDialog.style.display = "block";

    document.getElementById("referralErrorContent").textContent =
      "Please provide a highlight for title or description for referral reasons.";

    setTimeout(() => {
      errorDialog.classList.remove("pop-in");
      errorDialog.classList.add("pop-out");

      // Hide the dialog after the animation is done
      setTimeout(() => {
        errorDialog.style.display = "none";
      }, 300); // Match the duration of the popOut animation
    }, 3000); // Dialog visible for 3 seconds
  }
  // Function to show success dialog with pop-out animation and refresh the page
  function showReferralSuccess() {
    const successDialog = document.getElementById("referralSuccessDialog");
    successDialog.classList.remove("pop-out");
    successDialog.classList.add("pop-in");
    successDialog.style.display = "block";

    setTimeout(() => {
      successDialog.classList.remove("pop-in");
      successDialog.classList.add("pop-out");

      // Hide the dialog and close the modal with pop-out animation
      setTimeout(() => {
        successDialog.style.display = "none";
        closeReferModal(); // Close the modal
      }, 300); // Match the duration of the popOut animation
    }, 2000); // Dialog visible for 2 seconds

    // Refresh the page after the pop-out animation completes
    setTimeout(() => {
      window.location.reload(); // Refresh the browser
    }, 2300); // Allow time for the pop-out animation before refreshing
  }

  // Function to show error dialog with pop-out animation
  function showReferralError() {
    hideReferralLoader(); // Hide the loading overlay (if active)

    const errorDialog = document.getElementById("referralErrorDialog");
    errorDialog.classList.remove("pop-out");
    errorDialog.classList.add("pop-in");
    errorDialog.style.display = "block";

    setTimeout(() => {
      errorDialog.classList.remove("pop-in");
      errorDialog.classList.add("pop-out");

      // Hide the dialog after the animation is done
      setTimeout(() => {
        errorDialog.style.display = "none";
      }, 300); // Match the duration of the popOut animation
    }, 3000); // Dialog visible for 3 seconds
  }

  // Utility function to get selected text in an element
  window.getSelectionText = function (elementId) {
    const element = document.getElementById(elementId);
    let selectedText = "";
    if (window.getSelection) {
      const selection = window.getSelection();
      if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        if (
          range.commonAncestorContainer.parentNode === element ||
          range.commonAncestorContainer === element
        ) {
          selectedText = selection.toString();
        }
      }
      return selectedText;
    }
  };

  function deleteStatus(statusId) {
    const deleteDialog = document.getElementById("deleteConfirmationDialog");
    const confirmDeleteButton = document.getElementById("confirmSubmitDelete");
    const cancelDeleteButton = document.getElementById("cancelSubmitDelete");

    // Show the delete confirmation dialog with pop-in animation
    deleteDialog.classList.remove("pop-out");
    deleteDialog.classList.add("pop-in");
    deleteDialog.style.display = "block";

    // Handle cancel button click
    cancelDeleteButton.onclick = function () {
      closeDeleteDialog();
    };

    // Handle confirm delete button click
    confirmDeleteButton.onclick = function () {
      fetch(`/delete_status/${statusId}/`, {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            document
              .getElementById(`delete-${statusId}`)
              .closest(".box5")
              .remove();
            closeDeleteDialog(); // Close dialog after delete
          } else {
            showStatusError(data.message);
            closeDeleteDialog(); // Close dialog even if there's an error
          }
        })
        .catch((error) => {
          console.error("Error deleting status:", error);
          showStatusError("Error deleting status. Please try again.");
          closeDeleteDialog(); // Close dialog even if there's an error
        });
    };

    function closeDeleteDialog() {
      // Add pop-out animation and hide the dialog after the animation
      deleteDialog.classList.remove("pop-in");
      deleteDialog.classList.add("pop-out");

      setTimeout(() => {
        deleteDialog.style.display = "none";
      }, 300); // Match the animation duration
    }
  }

  function getEmotionIcon(emotion) {
    switch (emotion.toLowerCase()) {
      case "happiness":
        return "<i class='bx bx-happy-alt'></i>";
      case "sadness":
        return "<i class='bx bx-sad'></i>";
      case "fear":
        return "<i class='bx bx-dizzy' ></i>";
      case "anger":
        return "<i class='bx bx-angry'></i>";
      case "surprise":
        return "<i class='bx bx-shocked' ></i>";
      case "disgust":
        return "<i class='bx bx-confused' ></i>";
      default:
        return "<i class='bx bx-face'></i>";
    }
  }
  function mapEmotion(emotion) {
    switch (emotion.toLowerCase()) {
      case "happiness":
        return "Happy";
      case "sadness":
        return "Sad";
      case "fear":
        return "Fear";
      case "anger":
        return "Angry";
      case "surprise":
        return "Surprise";
      case "disgust":
        return "Disgust";
      default:
        return emotion;
    }
  }

  function truncateText(text, maxLength = 150) {
    if (text.length <= maxLength) {
      return text;
    }
    return text.substring(0, maxLength) + "...";
  }

  statusDescription.addEventListener("focus", hidePlaceholder);
  statusDescription.addEventListener("blur", showPlaceholder);

  function hidePlaceholder() {
    if (statusDescription.classList.contains("placeholder")) {
      statusDescription.classList.remove("placeholder");
      statusDescription.innerHTML = "";
    }
  }

  function showPlaceholder() {
    if (!statusDescription.innerHTML.trim().length) {
      statusDescription.classList.add("placeholder");
      statusDescription.innerHTML =
        statusDescription.getAttribute("placeholder");
    }
  }

  // Initialize placeholder display
  showPlaceholder();

  function saveFormData() {
    const title = statusTitle.value.trim();
    const description = statusDescription.innerHTML.trim();

    const formData = {
      selectedEmotion: selectedEmotion,
      title: title,
      description: description,
    };

    localStorage.setItem("statusFormData", JSON.stringify(formData));
  }

  function loadFormData() {
    const formData = JSON.parse(localStorage.getItem("statusFormData"));

    if (formData) {
      selectedEmotion = formData.selectedEmotion;
      statusTitle.value = formData.title;
      statusDescription.innerHTML = formData.description;

      feelingIcons.forEach((icon) => {
        if (icon.querySelector("img").alt === selectedEmotion) {
          icon.classList.add("active");
        } else {
          icon.classList.remove("active");
        }
      });
    }
  }

  function clearFormData() {
    localStorage.removeItem("statusFormData");
  }

  window.formatText = function (command, value = null) {
    document.execCommand(command, false, value);
    saveFormData();
  };

  // Function to show success message and close modal after animation
  function showStatusSuccess(message) {
    const dialogBox = document.getElementById("statusNotificationSuccess");
    const dialogContent = document.getElementById(
      "statusNotificationSuccessContent"
    );
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
        clearStatusComposerModal();
        closeStatusComposerModal(() => {
          setTimeout(() => {
            window.location.reload();
          }, 300); // Wait for statusModal pop-out animation to finish
        });
      }, 300); // Wait for dialogBox pop-out animation to finish
    }, 3000); // Duration to show the success message
  }
  // Function to show error message
  function showStatusError(message) {
    const errorDialog = document.getElementById("statusNotificationError");
    document.getElementById("statusNotificationErrorContent").textContent =
      message;

    errorDialog.classList.remove("pop-out");
    errorDialog.classList.add("pop-in");
    errorDialog.style.display = "block";

    setTimeout(() => {
      errorDialog.classList.remove("pop-in");
      errorDialog.classList.add("pop-out");

      setTimeout(() => {
        errorDialog.style.display = "none";
      }, 300); // Hide after pop-out animation
    }, 3000); // Error message visible for 3 seconds
  }

  // Function to close the status modal with fade-out and pop-out animation
  function closeStatusComposerModal(callback) {
    const statusModal = document.getElementById("statusModal");
    const statusModalOverlay = document.getElementById("statusModalOverlay");

    // Add pop-out and fade-out animations
    statusModal.classList.remove("pop-in");
    statusModal.classList.add("pop-out");
    statusModalOverlay.classList.remove("fade-in");
    statusModalOverlay.classList.add("fade-out");

    // Once the animations finish, hide the modal and overlay
    setTimeout(() => {
      statusModal.style.display = "none"; // Hide modal
      statusModal.classList.remove("pop-out"); // Remove pop-out class after animation

      statusModalOverlay.style.display = "none"; // Hide overlay
      statusModalOverlay.classList.remove("fade-out"); // Remove fade-out class after animation

      // If there's a callback (e.g., a page reload or additional action), call it
      if (callback) {
        callback();
      }
    }, 300); // Match animation duration (0.3s)
  }

  // Function to clear the modal content when closed
  function clearStatusComposerModal() {
    const statusTitle = document.getElementById("caption");
    const statusDescription = document.getElementById("description");
    const feelingIcons = document.querySelectorAll(".feeling-icon");

    selectedEmotion = null; // Reset selected emotion
    statusTitle.value = ""; // Clear title
    statusDescription.innerHTML = ""; // Clear description
    statusDescription.classList.add("placeholder"); // Reset placeholder
    feelingIcons.forEach((icon) => icon.classList.remove("active")); // Deselect emotion icons

    clearFormData(); // Clear local storage or form data
  }

  // Event listener to open the modal with animations
  const statusComposerButton = document.getElementById("statuscomposer");
  if (statusComposerButton) {
    statusComposerButton.addEventListener("click", function () {
      loadFormData(); // Load saved form data (if any)

      const statusModal = document.getElementById("statusModal");
      const statusModalOverlay = document.getElementById("statusModalOverlay");

      // Show modal and overlay
      statusModal.style.display = "block";
      statusModalOverlay.style.display = "block";

      // Trigger pop-in and fade-in animations
      setTimeout(() => {
        statusModal.classList.add("pop-in");
        statusModalOverlay.classList.add("fade-in");
      }, 10); // Minor delay to trigger CSS transition
    });
  }

  // Additional event listeners to close the modal with animations
  const closeStatusModal = document.getElementById("closeStatusModal");
  if (closeStatusModal) {
    closeStatusModal.addEventListener("click", closeStatusComposerModal);
  }

  const statusModalOverlay = document.getElementById("statusModalOverlay");
  if (statusModalOverlay) {
    statusModalOverlay.addEventListener("click", closeStatusComposerModal);
  }

  // Close the modal with pop-out animation
  closeStatusModal.addEventListener("click", function () {
    closeStatusComposerModal();
  });
  statusModalOverlay.addEventListener("click", function () {
    closeStatusComposerModal();
  });

  // Load current avatar
  fetch("/get_user_profile/")
    .then((response) => response.json())
    .then((data) => {
      currentAvatar.src = data.avatar || placeholderUrl;
      avatarLoader.style.display = "none";
      currentAvatar.style.display = "block";
    })
    .catch((error) => {
      console.error("", error);
      avatarLoader.style.display = "none";
      currentAvatar.style.display = "block";
    });

  // Select all avatar images and the upload-area image
  const uploadAreaImg = document.querySelector(".upload-area img");

  // Event listener for built-in avatars
  avatarImages.forEach((img) => {
    img.addEventListener("click", function () {
      // Remove 'selected' class from all avatar options and the upload-area image
      avatarImages.forEach((i) => i.classList.remove("selected"));
      uploadAreaImg.classList.remove("selected");

      // Add 'selected' class to the clicked avatar
      this.classList.add("selected");
      selectedAvatar = this.src;
      saveAvatarBtn.style.display = "inline-block";
    });
  });

  // Highlight the uploaded avatar like built-in avatars
  document.querySelector(".upload-area").addEventListener("click", function () {
    uploadAvatarInput.click();
  });

  // Event listener for the upload area click
  document.querySelector(".upload-area").addEventListener("click", function () {
    // Remove 'selected' class from all avatar options and the upload-area image
    avatarImages.forEach((i) => i.classList.remove("selected"));
    uploadAreaImg.classList.add("selected");

    // Trigger the file input click event
    uploadAvatarInput.click();
  });

  uploadAvatarInput.addEventListener("change", function () {
    if (uploadAvatarInput.files.length > 0) {
      const uploadedFile = uploadAvatarInput.files[0];

      // Check file size (limit to 1MB)
      if (uploadedFile.size > 1 * 1024 * 1024) {
        showNotificationError("File size exceeds the 1MB limit.");
        return;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        imageToCrop.src = e.target.result;

        // Show cropping modal
        cropperModal.style.display = "block";
        cropperModal.classList.add("pop-in");

        // Initialize cropper
        if (cropper) {
          cropper.destroy();
        }
        cropper = new Cropper(imageToCrop, {
          aspectRatio: 1, // Ensure square crop box
          viewMode: 1, // Keep crop box within the boundaries of the image
          guides: false, // Disable dashed lines (guides)
          center: false, // Disable center cross
          highlight: false, // Remove highlight when cropping
          background: false, // Disable dark background outside crop area
          autoCropArea: 0.9, // Set the initial crop area size
          dragMode: "move", // Allow moving the crop box within the image
        });
      };
      reader.readAsDataURL(uploadedFile);
    }
  });

  // Event listener for cropping the image
  cropImageBtn.addEventListener("click", function () {
    if (cropper) {
      const croppedCanvas = cropper.getCroppedCanvas({
        fillColor: "#ffffff", // Fill the background color to prevent transparency issues
      });

      // Create a circular cropped image
      const circleCanvas = document.createElement("canvas");
      const ctx = circleCanvas.getContext("2d");
      const radius = croppedCanvas.width / 2;

      // Adjust the circle canvas size to match the cropped area
      circleCanvas.width = croppedCanvas.width;
      circleCanvas.height = croppedCanvas.height;

      // Draw a circular clipping mask
      ctx.beginPath();
      ctx.arc(radius, radius, radius, 0, 2 * Math.PI);
      ctx.clip();

      // Draw the cropped image within the circular mask
      ctx.drawImage(croppedCanvas, 0, 0);

      // Convert the circular cropped image to a blob and upload
      circleCanvas.toBlob((blob) => {
        const formData = new FormData();
        formData.append("avatar", blob, "avatar.png");

        fetch(uploadAvatarUrl, {
          method: "POST",
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: formData,
        })
          .then((response) => {
            if (!response.ok) {
              return response.json().then((data) => {
                throw new Error(data.errors || "Unknown error");
              });
            }
            return response.json();
          })
          .then((data) => {
            if (data.success) {
              showNotificationSuccess("Avatar updated successfully!");
              // Update the current avatar in the profile immediately
              document.getElementById("currentAvatar").src = data.avatar_url;
              // Optionally, if you have a profile icon in the header or other parts
              document.getElementById("profileIconImage").src = data.avatar_url;
            } else {
              showNotificationError("" + (data.errors || "Unknown error"));
            }
            closeCropperModal.click();
          })
          .catch((error) => {
            console.error("", error);
            showNotificationError("" + error.message);
            closeCropperModal.click();
          });
      });
    }
  });

  // Event listener for saving the selected avatar
  saveAvatarBtn.addEventListener("click", function () {
    if (selectedAvatar) {
      fetch(selectedAvatar)
        .then((response) => response.blob())
        .then((blob) => {
          const formData = new FormData();
          formData.append("avatar", blob, "avatar.png");

          fetch(uploadAvatarUrl, {
            method: "POST",
            headers: {
              "X-CSRFToken": getCookie("csrftoken"),
            },
            body: formData,
          })
            .then((response) => {
              if (!response.ok) {
                return response.json().then((data) => {
                  throw new Error(data.errors || "Unknown error");
                });
              }
              return response.json();
            })
            .then((data) => {
              if (data.success) {
                showNotificationSuccess("Avatar updated successfully!");
                // Update the current avatar in the profile immediately
                document.getElementById("currentAvatar").src = data.avatar_url;
                // Optionally, if you have a profile icon in the header or other parts
                document.getElementById("profileIconImage").src =
                  data.avatar_url;
              } else {
                showNotificationError("" + (data.errors || "Unknown error"));
              }
            })
            .catch((error) => {
              console.error("", error);
              showNotificationError("" + error.message);
            });
        });
    } else {
      showNotificationError("Select or upload your avatar.");
    }
  });

  cancelCropBtn.addEventListener("click", function () {
    closeCropperModal.click();
  });

  closeCropperModal.addEventListener("click", function () {
    cropperModal.classList.remove("pop-in");
    cropperModal.classList.add("pop-out");
    setTimeout(() => {
      cropperModal.style.display = "none";
      cropperModal.classList.remove("pop-out");
      if (cropper) {
        cropper.destroy();
      }
    }, 300);
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function showNotificationSuccess(message) {
    const dialogBox = document.getElementById("notificationSuccessBox");
    const dialogContent = document.getElementById("notificationSuccessContent");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");

        // Close the avatar modal only after the success message animation is done
        avatarModal.classList.add("slide-upSolid");
        avatarModal.classList.remove("slide-downSolid");
      }, 300);
    }, 3000);
  }

  function showNotificationError(message) {
    const dialogBox = document.getElementById("notificationErrorBox");
    const dialogContent = document.getElementById("notificationErrorContent");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    }, 3000);
  }
  cancelAvatarBtn.addEventListener("click", function () {
    avatarModal.classList.add("slide-upSolid");
    avatarModal.classList.remove("slide-downSolid");
  });

  closeAvatarModal.addEventListener("click", function () {
    avatarModal.classList.add("slide-upSolid");
    avatarModal.classList.remove("slide-downSolid");
  });
});
const newPasswordInput = document.getElementById("newPassword");
const repeatPasswordInput = document.getElementById("repeatPassword");
const currentPasswordInput = document.getElementById("currentPassword");
const strengthBar = document.getElementById("strengthBar");
const generatePasswordBtn = document.getElementById("generatePassword");
const passwordForm = document.getElementById("passwordForm");

newPasswordInput.addEventListener("input", function () {
  const password = newPasswordInput.value;
  const strength = calculatePasswordStrength(password);
  updateStrengthBar(strength);
});

generatePasswordBtn.addEventListener("click", function () {
  const generatedPassword = generateSecurePassword();
  newPasswordInput.value = generatedPassword;
  repeatPasswordInput.value = generatedPassword;
  const strength = calculatePasswordStrength(generatedPassword);
  updateStrengthBar(strength);
});

passwordForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const currentPassword = currentPasswordInput.value;
  const newPassword = newPasswordInput.value;
  const repeatPassword = repeatPasswordInput.value;

  if (newPassword !== repeatPassword) {
    updatepassError("Passwords do not match.");
    return;
  }

  const data = {
    current_password: currentPassword,
    new_password: newPassword,
    repeat_new_password: repeatPassword,
  };

  fetch("/password_manager/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        updatepassSuccess("Password updated successfully!");
        passwordForm.reset();
        updateStrengthBar(0);
      } else {
        updatepassError("Please check your current password.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      updatepassError("Please check your current password.");
    });
});

function calculatePasswordStrength(password) {
  let strength = 0;
  if (password.length >= 8) strength += 1;
  if (/[A-Z]/.test(password)) strength += 1;
  if (/[0-9]/.test(password)) strength += 1;
  if (/[^A-Za-z0-9]/.test(password)) strength += 1;
  return strength;
}

function updateStrengthBar(strength) {
  const colors = ["#ff4b4b", "#ffb74b", "#fff44b", "#b4ff4b", "#4bff4b"];
  strengthBar.style.width = strength * 25 + "%";
  strengthBar.style.backgroundColor = colors[strength];
}

function generateSecurePassword() {
  const chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()";
  let password = "";
  for (let i = 0; i < 12; i++) {
    password += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return password;
}

function updatepassSuccess(message) {
  const dialogBox = document.getElementById("updatepasssuccess");
  const dialogContent = document.getElementById("updatepasssuccessContent");
  dialogContent.innerHTML = message;
  dialogBox.style.display = "block";
  setTimeout(() => {
    dialogBox.classList.add("pop-out");
    setTimeout(() => {
      dialogBox.style.display = "none";
      dialogBox.classList.remove("pop-out");
    }, 300);
  }, 3000);
}

function updatepassError(message) {
  const dialogBox = document.getElementById("updatepasserror");
  const dialogContent = document.getElementById("updatepasserrorContent");
  dialogContent.innerHTML = message;
  dialogBox.style.display = "block";
  setTimeout(() => {
    dialogBox.classList.add("pop-out");
    setTimeout(() => {
      dialogBox.style.display = "none";
      dialogBox.classList.remove("pop-out");
    }, 300);
  }, 3000);
}
// Start session timeout timer only if the user is authenticated
if (document.body.classList.contains("authenticated")) {
  startSessionTimer();
}

function startSessionTimer() {
  document.addEventListener("mousemove", resetTimer);
  document.addEventListener("keypress", resetTimer);

  const sessionTimeout = 30 * 60 * 1000;

  let timeout;

  function resetTimer() {
    clearTimeout(timeout);
    timeout = setTimeout(endSession, sessionTimeout);
  }

  function endSession() {
    showError("Session Expired, Please log in again.", "session");
    fetch("/logout/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // No redirect here, just show the session expired message
        }
      });
  }

  resetTimer();
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

const csrftoken = getCookie("csrftoken");

var loginModal = document.getElementById("loginModal");
var registerModal = document.getElementById("registerModal");
var loginRequiredModal = document.getElementById("loginRequiredModal");
var openLoginModalButton = document.getElementById("openLoginModal");
var overlay = document.getElementById("overlay");
var loginLink = document.getElementById("loginLink");
var registerLink = document.getElementById("registerLink");
var closeLoginModal = document.getElementById("closeLoginModal");
var closeRegisterModal = document.getElementById("closeRegisterModal");
var loginLinkFromRegister = document.getElementById("loginLinkFromRegister");

// Show login modal and overlay
if (loginLink) {
  loginLink.onclick = function (event) {
    event.preventDefault();
    loginModal.style.display = "block";
    overlay.style.display = "flex";
    setTimeout(() => {
      loginModal.classList.add("pop-in");
      overlay.classList.add("fade-in");
    }, 10);
  };
}

// Show register modal and overlay
if (registerLink) {
  registerLink.onclick = function (event) {
    event.preventDefault();
    registerModal.style.display = "block";
    overlay.style.display = "flex";
    setTimeout(() => {
      registerModal.classList.add("pop-in");
      overlay.classList.add("fade-in");
    }, 10);
  };
}

// Show login modal from register modal
if (loginLinkFromRegister) {
  loginLinkFromRegister.onclick = function (event) {
    event.preventDefault();
    registerModal.classList.add("pop-out");
    setTimeout(() => {
      registerModal.style.display = "none";
      registerModal.classList.remove("pop-out");
      loginModal.style.display = "block";
      setTimeout(() => {
        loginModal.classList.add("pop-in");
        overlay.classList.add("fade-in");
      }, 10);
    }, 300);
  };
}

// Hide login modal and overlay
if (closeLoginModal) {
  closeLoginModal.onclick = function () {
    loginModal.classList.add("pop-out");
    overlay.classList.add("fade-out"); // Added fade-out effect
    setTimeout(() => {
      loginModal.style.display = "none";
      overlay.style.display = "none";
      loginModal.classList.remove("pop-in", "pop-out");
      overlay.classList.remove("fade-in", "fade-out");
    }, 300);
  };
}

// Hide register modal and overlay
if (closeRegisterModal) {
  closeRegisterModal.onclick = function () {
    registerModal.classList.add("pop-out");
    loginModal.classList.add("pop-out");
    overlay.classList.add("fade-out");
    setTimeout(() => {
      registerModal.style.display = "none";
      loginModal.style.display = "none";
      overlay.style.display = "none";
      registerModal.classList.remove("pop-in", "pop-out");
      loginModal.classList.remove("pop-in", "pop-out");
      overlay.classList.remove("fade-in", "fade-out");
    }, 300);
  };
}

// Show login required modal and overlay
var expressFeelingsButton = document.getElementById("loginButton");
if (expressFeelingsButton) {
  expressFeelingsButton.onclick = function (event) {
    event.preventDefault();
    loginRequiredModal.style.display = "block";
    overlay.style.display = "flex";
    setTimeout(() => {
      loginRequiredModal.classList.add("pop-in");
      overlay.classList.add("fade-in");
    }, 10);
  };
}

// Close modal and overlay when clicking outside
window.onclick = function (event) {
  if (event.target == overlay) {
    if (
      loginRequiredModal.style.display === "block" ||
      document.querySelector(".flat-ui-dialog.session").style.display ===
        "block"
    ) {
      closeModals();
    }
  }
};

function closeModals() {
  if (loginRequiredModal.style.display === "block") {
    loginRequiredModal.classList.add("pop-out");
    overlay.classList.add("fade-out");
    setTimeout(() => {
      loginRequiredModal.style.display = "none";
      overlay.style.display = "none";
      loginRequiredModal.classList.remove("pop-in", "pop-out");
      overlay.classList.remove("fade-in", "fade-out");
    }, 300);
  } else if (
    document.querySelector(".flat-ui-dialog.session").style.display === "block"
  ) {
    const sessionDialogBox = document.querySelector(".flat-ui-dialog.session");
    sessionDialogBox.classList.add("pop-out");
    overlay.classList.add("fade-in");
    setTimeout(() => {
      sessionDialogBox.style.display = "none";
      overlay.style.display = "none";
      sessionDialogBox.classList.remove("pop-in", "pop-out");
      overlay.classList.remove("fade-in", "fade-out");
      window.location.reload();
    }, 300);
  }
}

// Close login required modal and show login modal
if (openLoginModalButton) {
  openLoginModalButton.onclick = function () {
    loginRequiredModal.classList.add("pop-out");
    setTimeout(() => {
      loginRequiredModal.style.display = "none";
      loginRequiredModal.classList.remove("pop-out");
      loginModal.style.display = "block";
      setTimeout(() => {
        loginModal.classList.add("pop-in");
      }, 10);
    }, 300);
  };
}
function showError(message, type) {
  const dialogBox = document.getElementById(
    type === "login"
      ? "loginDialogBox"
      : type === "register"
      ? "registerDialogBox"
      : "sessionDialogBox"
  );

  const dialogContent = document.getElementById(
    type === "login"
      ? "loginDialogContent"
      : type === "register"
      ? "registerDialogContent"
      : "sessionDialogContent"
  );

  // Update the content of the dialog
  dialogContent.innerHTML = message;
  dialogBox.style.display = "block";
  dialogBox.classList.add("error");
  dialogBox.classList.remove("pop-out");
  dialogBox.classList.add("pop-in");

  // Handle session overlay specifically
  if (type === "session") {
    const overlay = document.getElementById("sessionOverlay");
    overlay.style.display = "flex"; // Make the overlay visible
    overlay.classList.add("show");
    overlay.classList.remove("hide");

    // Close session dialog and overlay on click outside
    function handleOverlayClick(event) {
      if (!dialogBox.contains(event.target)) {
        dialogBox.classList.remove("pop-in");
        dialogBox.classList.add("pop-out");
        overlay.classList.remove("show");
        overlay.classList.add("hide");

        setTimeout(() => {
          dialogBox.style.display = "none";
          dialogBox.classList.remove("pop-out");
          overlay.style.display = "none"; // Hide the overlay after fade-out
          overlay.classList.remove("hide");
          overlay.removeEventListener("click", handleOverlayClick);
          window.location.reload(); // Reload the page after session expires
        }, 300); // Match the pop-out animation duration
      }
    }

    // Add event listener for clicking outside the modal
    overlay.addEventListener("click", handleOverlayClick);
  } else {
    // For login and register dialogs, auto-close after 3 seconds
    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300); // Ensure pop-out animation completes
    }, 3000);
  }
}
function showSuccess(message, type) {
  const successBox = document.getElementById(
    type === "login"
      ? "loginSuccessBox"
      : type === "register"
      ? "registerSuccessBox"
      : "logoutSuccessBox"
  );
  const successContent = document.getElementById(
    type === "login"
      ? "loginSuccessContent"
      : type === "register"
      ? "registerSuccessContent"
      : "logoutSuccessContent"
  );

  successContent.innerHTML = message;
  successBox.style.display = "block";
  successBox.classList.add("success");
  successBox.classList.remove("pop-out");
  successBox.classList.add("pop-in");

  setTimeout(() => {
    successBox.classList.remove("pop-in");
    successBox.classList.add("pop-out");
    setTimeout(() => {
      successBox.style.display = "none";
      successBox.classList.remove("pop-out");
      // Wait for the animation to finish before reloading
      if (type === "login") {
        window.location.reload();
      }
    }, 300);
  }, 3000);

  if (type === "logout") {
    overlay.addEventListener("click", function handleOverlayClick() {
      successBox.classList.add("pop-out");
      overlay.classList.add("fade-out");
      setTimeout(() => {
        successBox.style.display = "none";
        successBox.classList.remove("pop-out");
        overlay.style.display = "none";
        overlay.classList.remove("fade-in", "fade-out");
        overlay.removeEventListener("click", handleOverlayClick);
        window.location.reload();
      }, 300);
    });
  }
}

function parseErrorMessages(errors) {
  for (let field in errors) {
    if (errors.hasOwnProperty(field)) {
      return errors[field][0].message;
    }
  }
  return "An error occurred. Please try again.";
}
document.addEventListener("DOMContentLoaded", function () {
  // Separate references for login and register forms and buttons
  const loginForm = document.getElementById("loginForm");
  const registerForm = document.getElementById("registerForm");
  const loginButton = document.getElementById("loginButton");
  const signupButton = document.getElementById("signupButton");

  // Input fields for login form
  const loginUsernameField = loginForm.querySelector('input[name="username"]');
  const loginPasswordField = loginForm.querySelector('input[name="password"]');

  // Input fields for register form
  const registerFields = {
    student_id: registerForm.querySelector('input[name="student_id"]'),
    username: registerForm.querySelector('input[name="username"]'),
    full_name: registerForm.querySelector('input[name="full_name"]'),
    academic_year_level: registerForm.querySelector(
      'input[name="academic_year_level"]'
    ),
    contact_number: registerForm.querySelector('input[name="contact_number"]'),
    email: registerForm.querySelector('input[name="email"]'),
    password1: registerForm.querySelector('input[name="password1"]'),
    password2: registerForm.querySelector('input[name="password2"]'),
  };

  // Real-time validation for login form
  loginUsernameField.addEventListener("input", function () {
    validateField(loginUsernameField);
  });
  loginPasswordField.addEventListener("input", function () {
    validateField(loginPasswordField);
  });

  // Real-time validation for register form
  Object.values(registerFields).forEach((field) => {
    field.addEventListener("input", function () {
      validateField(field);
    });
  });

  // Separate form submission handlers
  loginForm.addEventListener("submit", function (event) {
    event.preventDefault();
    loginButton.disabled = true; // Disable the button initially

    const formData = new FormData(loginForm);
    let errorMessage = checkEmptyFields(formData, {
      username: "Username",
      password: "Password",
    });

    if (errorMessage) {
      validateFieldOnSubmit(loginUsernameField);
      validateFieldOnSubmit(loginPasswordField);
      showError(errorMessage, "login");
      loginButton.disabled = false; // Re-enable if there's an error
      return;
    }

    // Show the loader and process the login form submission...
  });

  registerForm.addEventListener("submit", function (event) {
    event.preventDefault();
    signupButton.disabled = true; // Disable the button initially

    const formData = new FormData(registerForm);
    let errorMessage = checkEmptyFields(formData, {
      student_id: "Student ID No.",
      username: "Username",
      full_name: "Full Name",
      academic_year_level: "Academic Year Level",
      contact_number: "Contact Number",
      email: "Email",
      password1: "Password",
      password2: "Confirm Password",
    });

    if (errorMessage) {
      Object.values(registerFields).forEach((field) => {
        validateFieldOnSubmit(field);
      });
      showError(errorMessage, "register");
      signupButton.disabled = false; // Re-enable if there's an error
      return;
    }

    // Show the loader and process the register form submission...
  });

  // Validation function for real-time checks
  function validateField(field) {
    if (field.value.trim() === "") {
      field.classList.remove("valid");
      field.classList.add("invalid");
    } else {
      field.classList.remove("invalid");
      field.classList.add("valid");
    }
  }

  // Trigger validation on form submission for empty fields
  function validateFieldOnSubmit(field) {
    if (field.value.trim() === "") {
      field.classList.add("invalid");
    } else {
      field.classList.remove("invalid");
      field.classList.add("valid");
    }
  }

  // Function to check for empty fields
  function checkEmptyFields(formData, fields) {
    let emptyFields = [];
    let allFieldsEmpty = true;

    for (let field in fields) {
      if (formData.get(field) && formData.get(field).trim() !== "") {
        allFieldsEmpty = false;
      } else {
        emptyFields.push(fields[field] + " is required.");
      }
    }

    if (allFieldsEmpty) {
      return "All fields are required.";
    }

    return emptyFields.length ? emptyFields[0] : null;
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const usernameField = document.querySelector('input[name="username"]');
  const passwordField = document.querySelector('input[name="password"]');
  const loginButton = document.getElementById("loginButton");

  // Real-time validation on input
  usernameField.addEventListener("input", validateField);
  passwordField.addEventListener("input", validateField);

  // Form submit event
  document
    .getElementById("loginForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();

      const formData = new FormData(this);
      loginButton.disabled = true; // Disable the button initially

      // Check if fields are empty
      let errorMessage = checkEmptyFields(formData, {
        username: "Username",
        password: "Password",
      });

      // If there is an error, show it and validate fields
      if (errorMessage) {
        validateFieldOnSubmit(usernameField);
        validateFieldOnSubmit(passwordField);
        showError(errorMessage, "login");
        loginButton.disabled = false; // Re-enable if there's an error
        return;
      }

      // Show the loader
      showLoginLoader();

      fetch(this.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams(formData).toString(),
      })
        .then((response) => response.json())
        .then((data) => {
          hideLoginLoader();

          if (data.success) {
            showSuccess("Login successful!", "login");
            setTimeout(() => {
              document.getElementById("loginForm").reset();
              loginModal.classList.add("pop-out");
              overlay.classList.add("fade-in");
              setTimeout(() => {
                loginModal.style.display = "none";
                overlay.style.display = "none";
                loginModal.classList.remove("pop-in", "pop-out");
                overlay.classList.remove("fade-in", "fade-out");
                window.location.href = data.redirect_url;
              }, 300); // Wait for pop-out animation to complete
            }, 1500);
          } else {
            let errorMessage = parseErrorMessages(data.error_message);
            showError(errorMessage, "login");
          }
        })
        .catch((error) => {
          hideLoginLoader();
          showError("An error occurred. Please try again.", "login");
        })
        .finally(() => {
          setTimeout(() => {
            loginButton.disabled = false;
          }, 3600); // Enable button after animations are complete
        });
    });

  // Real-time validation function
  function validateField(event) {
    const field = event.target;
    validateFieldStatus(field);
  }

  // Field validation function
  function validateFieldStatus(field) {
    if (field.value.trim() === "") {
      field.classList.remove("valid");
      field.classList.add("invalid");
    } else {
      field.classList.remove("invalid");
      field.classList.add("valid");
    }
  }

  // Trigger validation on form submission for empty fields
  function validateFieldOnSubmit(field) {
    if (field.value.trim() === "") {
      field.classList.add("invalid");
    } else {
      field.classList.remove("invalid");
      field.classList.add("valid");
    }
  }

  // Show loader
  function showLoginLoader() {
    const loginOverlay = document.getElementById("loginOverlay");
    loginOverlay.style.display = "block";
  }

  // Hide loader
  function hideLoginLoader() {
    const loginOverlay = document.getElementById("loginOverlay");
    loginOverlay.style.display = "none";
  }
});

document.querySelectorAll(".logout-link").forEach((item) => {
  item.addEventListener("click", function (event) {
    event.preventDefault();

    // Disable the logout button to prevent multiple clicks
    this.style.pointerEvents = "none";

    // Send the logout request
    fetch(this.href, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrftoken,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showSuccess("Logout successful!", "logout");
          setTimeout(() => {
            document
              .getElementById("logoutSuccessBox")
              .classList.add("pop-out");
            overlay.classList.add("fade-out");
            setTimeout(() => {
              document.getElementById("logoutSuccessBox").style.display =
                "none";
              overlay.style.display = "none";
              document
                .getElementById("logoutSuccessBox")
                .classList.remove("pop-in", "pop-out");
              overlay.classList.remove("fade-in", "fade-out");
              window.location.href = data.redirect_url;
            }, 300);
          }, 1500);
        } else {
          // Handle failure silently
          window.location.reload(); // Refresh the page on failure
        }
      })
      .catch((error) => {
        // Handle network errors silently
        window.location.reload(); // Refresh the page on error
      });
  });
});

function checkEmptyFields(formData, fields) {
  let emptyFields = [];
  let allFieldsEmpty = true;

  for (let field in fields) {
    if (formData.get(field) && formData.get(field).trim() !== "") {
      allFieldsEmpty = false;
    } else {
      emptyFields.push(fields[field] + " is required.");
    }
  }

  if (allFieldsEmpty) {
    return "All fields are required.";
  }

  return emptyFields.length ? emptyFields[0] : null;
}

// Function to show the policy modal with overlay
function showPolicyModal() {
  const policyModal = document.getElementById("policyModal");
  const policyOverlay = document.getElementById("policyOverlay");

  policyModal.style.display = "block";
  policyOverlay.style.display = "block";

  policyModal.classList.remove("pop-out");
  policyModal.classList.add("pop-in");
}

// Function to close the policy modal
function closePolicyModal() {
  const policyModal = document.getElementById("policyModal");
  const policyOverlay = document.getElementById("policyOverlay");

  policyModal.classList.remove("pop-in");
  policyModal.classList.add("pop-out");
  setTimeout(() => {
    policyModal.style.display = "none";
    policyModal.classList.remove("pop-out");
    policyOverlay.style.display = "none";
  }, 300);
}

// Event listener to show the policy modal when the policy text is clicked
document
  .getElementById("showPolicy")
  .addEventListener("click", showPolicyModal);

// Event listener to close the policy modal when the overlay is clicked
document
  .getElementById("policyOverlay")
  .addEventListener("click", closePolicyModal);

document.querySelectorAll(".v1_124 div").forEach((item) => {
  item.addEventListener("click", function () {
    document
      .querySelectorAll(
        ".v1_127, .v1_129, .v1_131, .v1_133, .v1_135, .v1_137, .v1_139, .v1_141"
      )
      .forEach((span) => {
        span.classList.remove("active");
      });
    this.querySelector("span").classList.add("active");
  });
});

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

//  Profile Modal Codes
document.addEventListener("DOMContentLoaded", function () {
  const usernameField = document.getElementById("username");
  const contactNumberField = document.getElementById("contact-number");
  const emailField = document.getElementById("email");
  const academicYearField = document.getElementById("academic-year");
  const profileIcon = document.getElementById("profileIcon");
  const tooltip = document.getElementById("profileTooltip");
  const avatarModal = document.getElementById("avatarModal");

  // Tooltip animation for profile icon
  profileIcon.addEventListener("mouseenter", function () {
    tooltip.classList.remove("popOut");
    tooltip.classList.add("popIn");
    tooltip.style.visibility = "visible";
  });

  profileIcon.addEventListener("mouseleave", function () {
    tooltip.classList.remove("popIn");
    tooltip.classList.add("popOut");
    tooltip.addEventListener(
      "animationend",
      function () {
        tooltip.style.visibility = "hidden";
      },
      { once: true }
    );
  });

  // Redirect to avatar modal on profile icon click
  profileIcon.addEventListener("click", function () {
    avatarModal.classList.add("slide-downSolid");
    avatarModal.classList.remove("slide-upSolid");
    avatarModal.style.display = "block";
  });

  // Fetch user profile when opening the profile modal
  document.getElementById("profileLink").addEventListener("click", function () {
    fetchUserProfile();
    profileModal.style.display = "block";
  });

  // Avatar refresh button logic
  const refreshAvatarBtn = document.getElementById("refreshAvatarBtn");
  refreshAvatarBtn.addEventListener("click", function () {
    fetchUserProfile();
  });

  // Function to display random profile tips in the footer
  const tips = [
    "Keep your contact info updated for important notifications.",
    "Make sure your academic year is accurate for proper service.",
    "Use a unique email for account recovery.",
    "Double-check your email to receive all communications.",
    "Update your profile to avoid service disruptions.",
    "Review your academic year each term for accuracy.",
    "Update your contact number immediately if it changes.",
    "Ensure your username is unique and memorable.",
    "Use your most active email for notifications.",
    "Verify your contact info regularly for smooth communication.",
    "Check your spam folder for missed notifications.",
    "Ensure your profile picture is appropriate and clear.",
    "Log out of your account after using shared devices.",
    "Keep your mailing address updated for physical notifications.",
    "Make sure your name matches official documents.",
    "Check your profile for any incomplete details.",
    "Update your emergency contacts regularly for safety.",
    "Review your email verification status for security.",
    "Notify support if any personal details seem incorrect.",
    "Ensure your student ID is correct for institutional access.",
    "Refresh your avatar regularly to keep your profile current.",
    "Complete your profile to unlock all features and services.",
    "Review profile settings after every major update.",
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

  setInterval(displayRandomTip, 5000);

  // Fetch user profile data
  function fetchUserProfile() {
    const avatarLoader = document.getElementById("avatarLoader");
    const profileIconImage = document.getElementById("profileIconImage");
    const placeholderUrl = profileIconImage.src;

    // Show loader and hide image
    avatarLoader.style.display = "block";
    profileIconImage.style.display = "none";

    fetch("/get_user_profile/")
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("student-id").value = data.student_id;
        document.getElementById("username").value = data.username;
        document.getElementById("full-name").value = data.full_name;
        document.getElementById("academic-year").value =
          data.academic_year_level;
        document.getElementById("contact-number").value = data.contact_number;

        // Mask and display the email
        document.getElementById("email").value = maskEmail(data.email);

        // Set the profile icon image source
        profileIconImage.src = data.avatar || placeholderUrl;
        profileIconImage.onload = () => {
          avatarLoader.style.display = "none";
          profileIconImage.style.display = "block";
        };
      })
      .catch((error) => {
        console.error("Error fetching profile data:", error);
        avatarLoader.style.display = "none";
        profileIconImage.style.display = "block";
      });
  }

  // Show profile success or error dialogs
  function showProfileSuccess(message) {
    const dialogBox = document.getElementById("profileSuccessDialog");
    const dialogContent = document.getElementById("profileSuccessContent");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    }, 3000);
  }

  function showProfileError(message) {
    const dialogBox = document.getElementById("profileErrorDialog");
    const dialogContent = document.getElementById("profileErrorContent");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    }, 3000);
  }
  const updateProfileBtn = document.getElementById("updateProfileBtn");
  const confirmUpdateDialog = document.getElementById("confirmUpdateDialog");
  const confirmUpdateBtn = document.getElementById("confirmUpdateBtn");
  const cancelUpdateBtn = document.getElementById("cancelUpdateBtn");

  // Show confirmation dialog when "Save changes" is clicked
  updateProfileBtn.addEventListener("click", function (event) {
    event.preventDefault();
    confirmUpdateDialog.style.display = "block";
    confirmUpdateDialog.classList.remove("pop-out");
    confirmUpdateDialog.classList.add("pop-in");
  });

  // Confirm profile update
  confirmUpdateBtn.addEventListener("click", function (event) {
    event.preventDefault();
    confirmUpdateDialog.classList.remove("pop-in");
    confirmUpdateDialog.classList.add("pop-out");

    // Delay hiding the dialog to allow the animation to complete
    setTimeout(() => {
      confirmUpdateDialog.style.display = "none";
    }, 300);

    // Call the updateUserProfile function
    updateUserProfile(event);
  });

  // Cancel profile update
  cancelUpdateBtn.addEventListener("click", function (event) {
    event.preventDefault();
    confirmUpdateDialog.classList.remove("pop-in");
    confirmUpdateDialog.classList.add("pop-out");

    // Delay hiding the dialog to allow the animation to complete
    setTimeout(() => {
      confirmUpdateDialog.style.display = "none";
    }, 300);
  });
  // Function to update user profile
  function updateUserProfile(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const contactNumber = document.getElementById("contact-number").value;
    const academicYear = document.getElementById("academic-year").value;

    // Show the profile update overlay and loader
    const profileUpdateOverlay = document.getElementById(
      "profileupdateOverlay"
    );
    profileUpdateOverlay.style.display = "block";

    fetch("/update_user_profile/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        username: username,
        contact_number: contactNumber,
        academic_year_level: academicYear, // Only include fields that are allowed to be updated
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Hide the overlay and loader
        profileUpdateOverlay.style.display = "none";

        if (data.success) {
          showProfileSuccess("Profile updated successfully!");
        } else {
          showProfileError(data.errors || "Error updating profile.");
        }
      })
      .catch((error) => {
        // Hide the overlay and loader
        profileUpdateOverlay.style.display = "none";
        console.error("Error updating profile:", error);
        showProfileError("Error updating profile. Please try again.");
      });
  }

  document
    .getElementById("profileForm")
    .addEventListener("submit", updateUserProfile);

  // Open modal and fetch profile data
  document.getElementById("profileLink").addEventListener("click", function () {
    fetchUserProfile();
    profileModal.style.display = "block";
  });
  // Email verification logic
  const verifyEmailBtn = document.getElementById("verifyEmailBtn");
  const emailVerifiedLabel = document.getElementById("emailVerifiedLabel");
  const resendCooldownLabel = document.getElementById("resendCooldownLabel");
  const cooldownTimer = document.getElementById("cooldownTimer");
  const verifyemailOverlay = document.getElementById("verifyemailOverlay");
  const changeemailSuccessBox = document.getElementById(
    "changeemailSuccessBox"
  );
  const changeemailErrorBox = document.getElementById("changeemailErrorBox");
  const verifyemailSuccessBox = document.getElementById(
    "verifyemailSuccessBox"
  );
  const verifyemailErrorBox = document.getElementById("verifyemailErrorBox");
  let cooldownInterval;

  const changeEmailBtn = document.getElementById("changeEmailBtn");
  const changeEmailDialog = document.getElementById("changeEmailDialog");
  const verifyNewEmailBtn = document.getElementById("verifyNewEmailBtn");
  const cancelChangeEmailBtn = document.getElementById("cancelChangeEmailBtn");
  const resendEmailCooldownLabel = document.getElementById(
    "resendEmailCooldownLabel"
  );
  let emailCooldownInterval;

  const resendNewEmailCooldownLabel = document.getElementById(
    "resendNewEmailCooldownLabel"
  );
  const cooldownNewEmailTimer = document.getElementById(
    "cooldownNewEmailTimer"
  );

  // Function to show the modal with pop-in animation
  changeEmailBtn.addEventListener("click", function () {
    changeEmailDialog.classList.remove("pop-out");
    changeEmailDialog.classList.add("pop-in");
    changeEmailDialog.style.display = "block";
  });

  // Function to close the modal with pop-out animation
  cancelChangeEmailBtn.addEventListener("click", function () {
    changeEmailDialog.classList.remove("pop-in");
    changeEmailDialog.classList.add("pop-out");

    // Set timeout to hide modal after animation completes
    setTimeout(() => {
      changeEmailDialog.style.display = "none";
    }, 300); // The timeout duration should match the animation duration
  });

  // Cooldown Timer for the new email verification
  function startNewEmailCooldown(seconds) {
    resendNewEmailCooldownLabel.style.display = "inline"; // Show the cooldown label
    cooldownNewEmailTimer.textContent = seconds;

    emailCooldownInterval = setInterval(() => {
      seconds--;
      cooldownNewEmailTimer.textContent = seconds;

      if (seconds <= 0) {
        clearInterval(emailCooldownInterval);
        resendNewEmailCooldownLabel.style.display = "none"; // Hide cooldown when complete
        verifyNewEmailBtn.innerText = "Resend"; // Change button text to "Resend"
        verifyNewEmailBtn.style.display = "inline-block"; // Show the button
      }
    }, 1000);
  }

  // Email validation function
  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Simple regex to validate email format
    return re.test(String(email).toLowerCase());
  }

  // Event listener for the "Verify" button for changing the email
  verifyNewEmailBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default form submission

    const newEmail = document.getElementById("new-email").value;

    // Validate the email format
    if (!validateEmail(newEmail)) {
      showChangeEmailError("Invalid email format.");
      return;
    }

    // Show overlay and loader while processing the request
    const changeemailOverlay = document.getElementById("changeemailOverlay");
    changeemailOverlay.style.display = "block";

    // Send the email change request to the server
    fetch("/request_email_change/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token for Django
      },
      body: JSON.stringify({ new_email: newEmail }),
    })
      .then((response) => response.json())
      .then((data) => {
        changeemailOverlay.style.display = "none"; // Hide the loader and overlay

        if (data.success) {
          // Start the cooldown timer and hide the "Verify" button
          verifyNewEmailBtn.style.display = "none";
          startNewEmailCooldown(60); // Start with 60 seconds countdown
          showChangeEmailSuccess(
            "Verification for email sent! Please check your inbox."
          );
        } else {
          // Show error dialog in case of an error
          showChangeEmailError(data.error || "Failed to update the email.");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        changeemailOverlay.style.display = "none"; // Hide the loader and overlay
        showChangeEmailError(
          "An error occurred while sending the email change request."
        );
      });
  });

  document
    .getElementById("verifyEmailBtn")
    .addEventListener("click", function (event) {
      event.preventDefault(); // Prevent any default form action if it's inside a form

      // Get the email field value (make sure it's unmasked if masked)
      const emailField = document.getElementById("email");
      const email = emailField.value;

      // Perform a check if the email is valid
      if (!validateEmail(email)) {
        showVerifyEmailError("Invalid email format.");
        return;
      }

      // Show loader
      const verifyemailOverlay = document.getElementById("verifyemailOverlay");
      verifyemailOverlay.style.display = "block";

      // Send the email verification request to the server
      fetch("/send_verification_email/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"), // CSRF Token if required (Django setup)
        },
        body: JSON.stringify({ email: email }),
      })
        .then((response) => response.json())
        .then((data) => {
          verifyemailOverlay.style.display = "none"; // Hide loader
          if (data.success) {
            showVerifyEmailSuccess(
              "Verification email sent! Please check your inbox."
            );
          } else {
            showVerifyEmailError(
              data.error || "Failed to send verification email."
            );
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          verifyemailOverlay.style.display = "none"; // Hide loader
          showVerifyEmailError(
            "An error occurred while sending the verification email."
          );
        });
    });

  // Function to mask the email
  function maskEmail(email) {
    const [localPart, domainPart] = email.split("@");
    const maskedLocal = localPart.slice(0, 1) + "*****";
    const maskedDomain = "*****." + domainPart.split(".").pop();
    return maskedLocal + "@" + maskedDomain;
  }
  // Function to start the cooldown timer only after successful email sending
  // Function to start cooldown timer
  function startCooldown(seconds) {
    resendCooldownLabel.style.display = "inline";
    cooldownTimer.textContent = seconds;

    cooldownInterval = setInterval(() => {
      seconds--;
      cooldownTimer.textContent = seconds;

      if (seconds <= 0) {
        clearInterval(cooldownInterval);
        resendCooldownLabel.style.display = "none";
        showResendButton();
      }
    }, 1000);
  }

  // Show the Resend button after cooldown
  function showResendButton() {
    const resendBtn = document.createElement("button");
    resendBtn.innerText = "Resend";
    resendBtn.classList.add("verify-btn");
    resendBtn.addEventListener("click", function (event) {
      event.stopPropagation(); // Stop event propagation
      event.preventDefault(); // Prevent form submission
      startCooldown(60);
      resendBtn.style.display = "none"; // Hide resend during cooldown
      sendVerificationEmail();
    });
    document.querySelector(".email-container").appendChild(resendBtn);
  }

  // Function to send a verification email
  function sendVerificationEmail() {
    const email = document.getElementById("email").value;

    // Show the overlay and loader
    verifyemailOverlay.style.display = "block";

    fetch("/send_verification_email/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({ email: email }),
    })
      .then((response) => response.json())
      .then((data) => {
        verifyemailOverlay.style.display = "none"; // Hide loader
        if (data.success) {
          // Show success dialog with animation
          showVerifyEmailSuccess(
            "Verification email sent! Please check your inbox."
          );
        } else {
          // Show error dialog with animation
          showVerifyEmailError("Error sending verification email.");
        }
      })
      .catch((error) => {
        verifyemailOverlay.style.display = "none"; // Hide loader
        showVerifyEmailError(
          "An error occurred while sending the verification email."
        );
      });
  }

  // Show email verification success dialog
  function showVerifyEmailSuccess(message) {
    const dialogBox = document.getElementById("verifyemailSuccessBox");
    const dialogContent = document.getElementById("verifyemailSuccessContent");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    }, 3000);
  }

  // Show email verification error dialog
  function showVerifyEmailError(message) {
    const dialogBox = document.getElementById("verifyemailErrorBox");
    const dialogContent = document.getElementById("verifyemailErrorContent");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    }, 3000);
  }

  // Show email verification success dialog
  function showChangeEmailSuccess(message) {
    const dialogBox = document.getElementById("changeemailSuccessBox");
    const dialogContent = document.getElementById("changeemailSuccessBox");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    }, 3000);
  }

  // Show email verification error dialog
  function showChangeEmailError(message) {
    const dialogBox = document.getElementById("changeemailErrorBox");
    const dialogContent = document.getElementById("changeemailErrorBox");
    dialogContent.innerHTML = message;
    dialogBox.style.display = "block";
    dialogBox.classList.remove("pop-out");
    dialogBox.classList.add("pop-in");

    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
    }, 3000);
  }

  // Event listener for the Verify button
  verifyEmailBtn.addEventListener("click", function (event) {
    event.stopPropagation(); // Stop event propagation
    event.preventDefault(); // Prevent form submission
    verifyEmailBtn.style.display = "none"; // Hide verify button
    startCooldown(60); // Start 60 seconds cooldown
    sendVerificationEmail(); // Send verification email
  });

  // Check email verification status when modal opens
  function checkEmailVerificationStatus() {
    fetch("/check_email_verification/")
      .then((response) => response.json())
      .then((data) => {
        if (data.is_verified) {
          verifyEmailBtn.style.display = "none"; // Hide verify button
          emailVerifiedLabel.style.display = "inline"; // Show verified label
        } else {
          verifyEmailBtn.style.display = "inline"; // Show verify button
          emailVerifiedLabel.style.display = "none"; // Hide verified label
        }
      })
      .catch((error) =>
        console.error("Error checking email verification:", error)
      );
  }

  document.getElementById("profileLink").addEventListener("click", function () {
    checkEmailVerificationStatus();
  });

  const notificationButton = document.getElementById("notificationButton");
  const notificationDot = document.getElementById("notificationDot");
  const notificationList = document.getElementById("notificationList");
  const notificationItems = document.getElementById("notificationItems");
  const loadMoreButton = document.getElementById("notificationLoadMore");

  let currentPage = 1; // Track the current page for pagination
  let totalPages = 1; // Total pages to be fetched (to be updated after fetching data)
  let renderedNotifications = new Map(); // Store rendered notifications by id

  // Show loader while loading notifications
  function showNotificationLoader() {
    const loader = document.createElement("div");
    loader.className = "loader-placeholder";
    for (let i = 0; i < 3; i++) {
      const loaderItem = document.createElement("div");
      loaderItem.className = "loader-item";
      loaderItem.innerHTML = `
      <div class="loader-item-avatar"></div>
      <div class="loader-item-content"></div>
      <div class="loader-item-timestamp"></div>
    `;
      loader.appendChild(loaderItem);
    }
    notificationItems.appendChild(loader);
  }

  // Remove the loader after notifications are loaded
  function removeNotificationLoader() {
    const loader = document.querySelector(".loader-placeholder");
    if (loader) {
      loader.remove();
    }
  }

  // Fetch notifications from the API with pagination support
  async function fetchNotifications(page = 1) {
    try {
      showNotificationLoader();
      const response = await fetch(`/notifications/fetch/?page=${page}`);
      if (response.ok) {
        const data = await response.json();
        totalPages = data.total_pages;
        return data.notifications;
      } else {
        console.error("Failed to fetch notifications.");
        return [];
      }
    } catch (error) {
      console.error("Error fetching notifications:", error);
      return [];
    } finally {
      removeNotificationLoader();
    }
  }

  // Mark the notification button as clicked in the backend
  async function markNotificationButtonClicked() {
    try {
      const response = await fetch(`/notifications/mark_button_clicked/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
      });
      if (!response.ok) {
        console.error("Failed to mark notification button as clicked.");
      } else {
        notificationDot.style.display = "none"; // Hide the dot after clicking
      }
    } catch (error) {
      console.error("Error marking notification button as clicked:", error);
    }
  }

  // Mark a specific notification as read when clicked (permanent)
  async function markNotificationAsRead(notificationId) {
    try {
      let cleanNotificationId = notificationId
        .replace("status_", "")
        .replace("replies_", "");

      const response = await fetch(
        `/notifications/mark_as_read/${cleanNotificationId}/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
        }
      );

      if (!response.ok) {
        console.error("Failed to mark notification as read.");
      } else {
        // Mark this notification as permanently read in the backend
        renderedNotifications.get(notificationId).is_read = true;
      }
    } catch (error) {
      console.error("Error marking notification as read:", error);
    }
  }

  // Get CSRF token for Django
  function getCSRFToken() {
    return document.querySelector("[name=csrfmiddlewaretoken]").value;
  }

  // Render the notifications in the notification list
  async function renderNotifications(page = 1) {
    const notifications = await fetchNotifications(page);

    if (notifications.length === 0) {
      loadMoreButton.style.display = "none";
      return;
    }

    notifications.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

    let hasUnreadNotifications = false;

    notifications.forEach((notification) => {
      if (!renderedNotifications.has(notification.id)) {
        const item = document.createElement("div");
        item.classList.add("notification-item");
        item.dataset.id = notification.id;

        // If the notification is unread, apply the unread styling
        if (!notification.is_read) {
          item.classList.add("unread");
          hasUnreadNotifications = true; // Track if there are unread notifications
        } else {
          item.classList.add("read");
        }

        // Make the entire notification clickable and mark as read on click
        item.addEventListener("click", async function () {
          const notificationId = item.dataset.id; // Ensure this ID is the notification ID

          // Mark the notification as read
          if (!notification.is_read) {
            await markNotificationAsRead(notificationId); // Pass the notification ID here
            item.classList.remove("unread");
            item.classList.add("read");

            const greenDot = item.querySelector(".notification-dot-green");
            if (greenDot) {
              greenDot.remove();
            }
            item
              .querySelector(".timestamp")
              .classList.remove("timestamp-green");
          }

          // Redirect to the status page
          window.location.href = notification.link;
        });

        // Build notification item structure
        item.innerHTML = `
          <img class="notification-avatar" src="${
            notification.avatar
          }" alt="Avatar">
          <div class="notification-content">
            <div class="message">${notification.message}</div>
            <div class="timestamp ${
              notification.is_read ? "" : "timestamp-green"
            }">
              ${formatTimestamp(notification.timestamp)}
            </div>
          </div>
          ${
            notification.is_read
              ? ""
              : '<div class="notification-dot-green"></div>'
          }
        `;

        notificationItems.appendChild(item);

        renderedNotifications.set(notification.id, notification);
      }
    });

    // Show the "Load More" button if more pages are available
    if (currentPage < totalPages) {
      loadMoreButton.style.display = "block";
    } else {
      loadMoreButton.style.display = "none";
    }

    // Show or hide the red notification dot based on unread notifications
    if (hasUnreadNotifications) {
      notificationDot.style.display = "block";
      notificationDot.classList.add("blink");
    } else {
      notificationDot.style.display = "none";
    }
  }

  // Check the notification status from the backend
  async function checkNotificationStatus() {
    try {
      const response = await fetch(`/notifications/check_status/`);
      if (response.ok) {
        const data = await response.json();
        if (data.has_unread_notifications && !data.has_clicked_notification) {
          notificationDot.style.display = "block";
          notificationDot.classList.add("blink");
        } else {
          notificationDot.style.display = "none";
        }
      }
    } catch (error) {
      console.error("Error checking notification status:", error);
    }
  }

  // Initial notification loading when the button is clicked
  notificationButton.addEventListener("click", async function () {
    if (notificationList.style.display === "none") {
      await renderNotifications(currentPage); // Render the list of notifications
      notificationList.classList.remove("pop-up");
      notificationList.classList.add("animated");
      notificationList.style.display = "block";

      // Mark notification button as clicked and hide the red dot
      await markNotificationButtonClicked(); // Call to mark the notification button clicked
    } else {
      notificationList.classList.remove("animated");
      notificationList.classList.add("pop-up");
      setTimeout(() => {
        notificationList.style.display = "none";
      }, 300);
    }
  });

  // Load more notifications when clicking the "Load More" button
  loadMoreButton.addEventListener("click", async function () {
    currentPage++;
    await renderNotifications(currentPage);
    notificationList.style.maxHeight = "700px";
    notificationList.style.overflowY = "auto";
  });

  // Format the timestamp
  function formatTimestamp(timestamp) {
    if (timestamp.includes("0 minutes ago")) {
      return "Just Now";
    }
    return timestamp;
  }

  // Periodically check for new unread notifications (without WebSocket)
  setInterval(async () => {
    const notifications = await fetchNotifications();
    const hasUnread = notifications.some(
      (notification) => !notification.is_read
    );

    if (hasUnread) {
      notificationDot.style.display = "block";
      notificationDot.classList.add("blink");
    }
  }, 60000); // Check every 60 seconds

  // Close the notification list when clicking outside
  window.addEventListener("click", function (event) {
    if (
      !notificationButton.contains(event.target) &&
      !notificationList.contains(event.target)
    ) {
      if (notificationList.style.display === "block") {
        notificationList.classList.remove("animated");
        notificationList.classList.add("pop-up");

        setTimeout(() => {
          notificationList.style.display = "none";
        }, 300);
      }
    }
  });

  // Initial rendering of notifications when the page loads
  renderNotifications();

  // Initial check for notification status when the page loads
  checkNotificationStatus();
});
