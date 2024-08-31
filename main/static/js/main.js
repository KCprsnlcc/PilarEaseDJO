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
  const statusModalOverlay = document.getElementById("statusModalOverlay");
  const closeStatusModal = document.getElementById("closeStatusModal");
  const statusComposerButton = document.getElementById("statuscomposer");

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

      const csrfToken = document.querySelector(
        "[name=csrfmiddlewaretoken]"
      ).value;

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
          if (data.success) {
            forgotPasswordSuccessBox(data.message);
          } else {
            forgotPasswordErrorBox(data.error);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          forgotPasswordErrorBox("Network error. Please try again.");
        });
    });

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
  // Update the token and character count
  function updateCounters() {
    const descriptionElement = document.getElementById("description");
    const characterCount = descriptionElement.textContent.length;
    const tokenCount = countTokens(descriptionElement.textContent);

    document.getElementById(
      "characterCount"
    ).textContent = `${characterCount} characters`;
    document.getElementById("tokenCount").textContent = `${tokenCount} tokens`;

    if (tokenCount > 512) {
      document.getElementById(
        "tokenCount"
      ).textContent = `512 tokens (Max reached)`;
    }
  }

  // // Show the diary suggestion dialog
  // function showSuggestDiary() {
  //   const suggestDiaryDialog = document.getElementById("suggestDiaryDialog");
  //   suggestDiaryDialog.classList.remove("pop-out");
  //   suggestDiaryDialog.classList.add("pop-in");
  //   suggestDiaryDialog.style.display = "block";
  // }

  // // Close the diary suggestion dialog
  // document
  //   .getElementById("closeDiarySuggestionBtn")
  //   .addEventListener("click", function () {
  //     const suggestDiaryDialog = document.getElementById("suggestDiaryDialog");
  //     suggestDiaryDialog.classList.remove("pop-in");
  //     suggestDiaryDialog.classList.add("pop-out");
  //     setTimeout(() => {
  //       suggestDiaryDialog.style.display = "none";
  //     }, 300);
  //   });

  // // Redirect to the diary module when clicked
  // document
  //   .getElementById("openDiaryBtn")
  //   .addEventListener("click", function () {
  //     window.location.href = "/diary_module_url"; // Replace with the actual diary module URL
  //   });

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
                            ? `<button id="delete-${status.id}" class="delete-button status"><i class='bx bxs-trash bx-tada bx-flip-horizontal'></i></button>`
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
        } else {
          showStatusError(data.message);
        }
      })
      .catch((error) => {
        console.error("Error deleting status:", error);
        showStatusError("Error deleting status. Please try again.");
      });
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

  function displayNewStatus(status) {
    const container = document.getElementById("boxContainer");
    const newBox = document.createElement("div");
    newBox.classList.add("box5", "pop");
    newBox.innerHTML = `
            <div class="avatar-content">
                <img src="${
                  status.avatar_url
                }" alt="Avatar" class="circle-avatar-placeholder" />
                <p class="username-placeholder">${status.username}</p>
            </div>
            <div class="content">
                <h2 class="title-placeholder">${status.title}</h2>
                <p class="description-placeholder">${truncateText(
                  status.description
                )}</p>
                <span class="time-stamp time-stamp-placeholder">${
                  status.created_at
                } ago</span>
                <span class="feelings feelings-placeholder">${getEmotionIcon(
                  status.emotion
                )} ${mapEmotion(status.emotion)}</span>
                <span class="replies replies-placeholder">${status.replies} ${
      status.replies === 1 ? "Reply" : "Replies"
    }</span>
            </div>
             ${
               status.can_delete
                 ? `<button id="delete-${status.id}" class="delete-button status"><i class='bx bxs-trash bx-tada bx-flip-horizontal'></i></button>`
                 : ""
             }
          `;
    container.prepend(newBox); // Prepend to show the new status at the top

    newBox.addEventListener("animationend", function () {
      newBox.classList.remove("pop");
    });
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

  function closeStatusComposerModal(callback) {
    statusModal.classList.remove("pop-in");
    statusModal.classList.add("pop-out");
    statusModalOverlay.classList.remove("fade-in");
    statusModalOverlay.classList.add("fade-out");
    setTimeout(() => {
      statusModal.style.display = "none";
      statusModal.classList.remove("pop-out");
      statusModalOverlay.style.display = "none";
      statusModalOverlay.classList.remove("fade-out");
      if (callback) {
        callback();
      }
    }, 300); // Animation duration
  }
  function clearStatusComposerModal() {
    selectedEmotion = null;
    statusTitle.value = "";
    statusDescription.innerHTML = "";
    statusDescription.classList.add("placeholder");
    feelingIcons.forEach((i) => i.classList.remove("active"));
    clearFormData();
  }

  // Clear the modal fields when opened
  if (statusComposerButton) {
    statusComposerButton.addEventListener("click", function () {
      loadFormData();
      statusModal.style.display = "block";
      statusModalOverlay.style.display = "block";
      setTimeout(() => {
        statusModal.classList.add("pop-in");
        statusModalOverlay.classList.add("fade-in");
      }, 10);
    });
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

  avatarImages.forEach((img) => {
    img.addEventListener("click", function () {
      avatarImages.forEach((i) => i.classList.remove("selected"));
      this.classList.add("selected");
      selectedAvatar = this.src;
      saveAvatarBtn.style.display = "inline-block";
    });
  });

  document.querySelector(".upload-area").addEventListener("click", function () {
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
          aspectRatio: 528 / 560,
          viewMode: 1,
        });
      };
      reader.readAsDataURL(uploadedFile);
    }
  });

  cropImageBtn.addEventListener("click", function () {
    if (cropper) {
      cropper.getCroppedCanvas().toBlob((blob) => {
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
              document.getElementById("currentAvatar").src = data.avatar_url;
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
                document.getElementById("currentAvatar").src = data.avatar_url;
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

  const profileIcon = document.getElementById("profileIcon");
  const tooltip = document.getElementById("profileTooltip");

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

  profileIcon.addEventListener("click", function () {
    fetchUserProfile();
    avatarModal.classList.add("slide-downSolid");
    avatarModal.classList.remove("slide-upSolid");
    avatarModal.style.display = "block";
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
    showError("Passwords do not match.");
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
        showSuccess("Password updated successfully!");
        passwordForm.reset();
        updateStrengthBar(0);
      } else {
        showError("Please check your current password.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      showError("Please check your current password.");
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

function showSuccess(message) {
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

function showError(message) {
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

  dialogContent.innerHTML = message;
  dialogBox.style.display = "block";
  dialogBox.classList.add("error");
  dialogBox.classList.remove("pop-out");
  dialogBox.classList.add("pop-in");

  if (type === "session") {
    overlay.style.display = "flex";
    overlay.classList.add("fade-in");
    overlay.addEventListener("click", function handleOverlayClick() {
      dialogBox.classList.add("pop-out");
      overlay.classList.add("fade-out"); // Updated to fade-out
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
        overlay.style.display = "none";
        overlay.classList.remove("fade-in", "fade-out");
        overlay.removeEventListener("click", handleOverlayClick);
        window.location.reload();
      }, 300);
    });
  }

  if (type !== "session") {
    setTimeout(() => {
      dialogBox.classList.remove("pop-in");
      dialogBox.classList.add("pop-out");
      setTimeout(() => {
        dialogBox.style.display = "none";
        dialogBox.classList.remove("pop-out");
      }, 300);
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

document
  .getElementById("registerForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
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
      showError(errorMessage, "register");
      return;
    }
    fetch(this.action, {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showSuccess("Registration successful!", "register");
          setTimeout(() => {
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

            document.getElementById("registerForm").reset();
          }, 1500);
        } else {
          let errorMessage = parseErrorMessages(data.error_message);
          showError(errorMessage, "register");
        }
      })
      .catch((error) => {
        showError("An error occurred. Please try again.", "register");
      });
  });

document
  .getElementById("loginForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    let errorMessage = checkEmptyFields(formData, {
      username: "Username",
      password: "Password",
    });
    if (errorMessage) {
      showError(errorMessage, "login");
      return;
    }
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
            }, 300);
          }, 1500);
        } else {
          let errorMessage = parseErrorMessages(data.error_message);
          showError(errorMessage, "login");
        }
      })
      .catch((error) => {
        showError("An error occurred. Please try again.", "login");
      });
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

// Function to fetch user profile data
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
      document.getElementById("academic-year").value = data.academic_year_level;
      document.getElementById("contact-number").value = data.contact_number;
      document.getElementById("email").value = data.email;
      // Set the profile icon image source
      profileIconImage.src = data.avatar || placeholderUrl;
      // Hide loader once image is loaded
      profileIconImage.onload = () => {
        avatarLoader.style.display = "none";
        profileIconImage.style.display = "block";
      };
    })
    .catch((error) => {
      console.error("", error);
      // Hide loader in case of error
      avatarLoader.style.display = "none";
      profileIconImage.style.display = "block";
    });
}
// Function to show success dialog
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

// Function to show error dialog
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
document.getElementById("profileLink").addEventListener("click", function () {
  fetchUserProfile();
  profileModal.style.display = "block";
});
const refreshAvatarBtn = document.getElementById("refreshAvatarBtn");
refreshAvatarBtn.addEventListener("click", function () {
  fetchUserProfile();
});

// Function to update user profile data
function updateUserProfile(event) {
  event.preventDefault(); // Prevent the form from submitting in the traditional way

  const username = document.getElementById("username").value;
  const contactNumber = document.getElementById("contact-number").value;
  const email = document.getElementById("email").value;
  const academicYear = document.getElementById("academic-year").value;

  fetch("/update_user_profile/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // Include CSRF token
    },
    body: JSON.stringify({
      username: username,
      contact_number: contactNumber,
      email: email,
      academic_year_level: academicYear,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        showProfileSuccess("Profile updated successfully!");
      } else {
        // Check for specific errors
        if (data.errors.username) {
          showProfileError(data.errors.username);
        } else if (data.errors.email) {
          showProfileError(data.errors.email);
        } else if (data.errors.password) {
          showProfileError(data.errors.password);
        } else {
          showProfileError("Error updating profile. Please try again.");
        }
      }
    })
    .catch((error) => {
      console.error("", error);
      showProfileError("Error updating profile. Please try again.");
    });
}

document
  .getElementById("profileForm")
  .addEventListener("submit", updateUserProfile);

const notificationButton = document.getElementById("notificationButton");
const notificationList = document.getElementById("notificationList");
const notificationCount = document.getElementById("notificationCount");

function fetchNotifications() {
  // Fetch notifications from the server (this is just a mock example)
  return [
    {
      message: "You uploaded a status, click to view it.",
    },
    {
      message: "USERNAME replied to your status, click to see it.",
    },
  ];
}

function renderNotifications() {
  const notifications = fetchNotifications();
  notificationList.innerHTML = "";
  notifications.forEach((notification) => {
    const item = document.createElement("div");
    item.classList.add("notification-item");
    item.innerHTML = `<a href="${notification.link}">${notification.message}</a>`;
    notificationList.appendChild(item);
  });
  notificationCount.innerText = notifications.length;
  if (notifications.length > 0) {
    notificationCount.style.display = "block";
  } else {
    notificationCount.style.display = "none";
  }
}

notificationButton.addEventListener("click", function () {
  if (notificationList.style.display === "none") {
    renderNotifications();
    notificationList.style.display = "block";
  } else {
    notificationList.style.display = "none";
  }
});

window.addEventListener("click", function (event) {
  if (
    !notificationButton.contains(event.target) &&
    !notificationList.contains(event.target)
  ) {
    notificationList.style.display = "none";
  }
});

renderNotifications();
