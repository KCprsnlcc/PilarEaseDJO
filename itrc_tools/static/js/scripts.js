// static/js/autoManage.js

// static/js/autoManage.js

$(document).ready(function () {
  // Initialize Bootstrap tooltips (if any)
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Modal Elements
  const $modalOverlay = $("#confirmationModal");
  const $modalTitle = $("#modalTitle");
  const $modalBody = $("#modalBody");
  const $confirmModalButton = $("#confirmModal");
  const $cancelModalButton = $("#cancelModal");
  const $closeModalButton = $("#closeModal");

  let currentActionType = null; // e.g., 'enable_auto_accept', 'disable_auto_reject', 'accept_user', 'reject_user'
  let currentCheckbox = null; // The checkbox that triggered the action
  let currentUserId = null; // Relevant for user actions

  // Function to open modal with dynamic content
  function openModal(actionType, $checkbox = null, userId = null) {
    currentActionType = actionType;
    currentCheckbox = $checkbox;
    currentUserId = userId;

    // Update modal content based on actionType
    switch (actionType) {
      case "enable_auto_accept":
        $modalTitle.text("Confirm Enable Auto Accept");
        $modalBody.html(
          "<p>Are you sure you want to enable automatic acceptance of all pending verification requests?</p>"
        );
        break;
      case "enable_auto_reject":
        $modalTitle.text("Confirm Enable Auto Reject");
        $modalBody.html(
          "<p>Are you sure you want to enable automatic rejection of all pending verification requests?</p>"
        );
        break;
      case "disable_auto_accept":
        $modalTitle.text("Confirm Disable Auto Accept");
        $modalBody.html(
          "<p>Are you sure you want to disable automatic acceptance of pending verification requests?</p>"
        );
        break;
      case "disable_auto_reject":
        $modalTitle.text("Confirm Disable Auto Reject");
        $modalBody.html(
          "<p>Are you sure you want to disable automatic rejection of pending verification requests?</p>"
        );
        break;
      case "accept_user":
        $modalTitle.text("Confirm Accept User");
        $modalBody.html("<p>Are you sure you want to accept this user?</p>");
        break;
      case "reject_user":
        $modalTitle.text("Confirm Reject User");
        $modalBody.html("<p>Are you sure you want to reject this user?</p>");
        break;
      default:
        $modalTitle.text("Confirm Action");
        $modalBody.html("<p>Are you sure you want to perform this action?</p>");
    }

    $modalOverlay.addClass("show");
  }

  // Function to close modal and optionally revert checkbox
  function closeModal(revert = false) {
    // Add smooth hide transition and remove after completed
    $modalOverlay.removeClass("show");

    setTimeout(() => {
      if (revert && currentCheckbox) {
        currentCheckbox.prop("checked", !currentCheckbox.prop("checked"));
        updateToggleLabel(currentCheckbox);
      }
      // Re-enable checkbox if it was disabled
      if (currentCheckbox) {
        currentCheckbox.prop("disabled", false);
      }
      currentActionType = null;
      currentCheckbox = null;
      currentUserId = null;
    }, 300); // Match the CSS transition duration
  }
  // Function to update the toggle label based on checkbox state
  function updateToggleLabel($checkbox) {
    const isChecked = $checkbox.is(":checked");
    const $toggleText = $checkbox
      .next(".pilarease-itrc-toggle-label")
      .find(".toggle-text");

    if (isChecked) {
      $toggleText.text("Enabled");
      $toggleText.removeClass("disabled").addClass("enabled");
    } else {
      $toggleText.text("Disabled");
      $toggleText.removeClass("enabled").addClass("disabled");
    }
  }
  // Handle checkbox changes
  $(".pilarease-itrc-toggle-checkbox").on("change", function () {
    const $checkbox = $(this);
    const action = $checkbox.data("action");
    const isChecked = $checkbox.is(":checked");

    let actionType = "";

    if (action === "accept") {
      actionType = isChecked ? "enable_auto_accept" : "disable_auto_accept";
    } else if (action === "reject") {
      actionType = isChecked ? "enable_auto_reject" : "disable_auto_reject";
    }

    // Open confirmation modal
    openModal(actionType, $checkbox);

    // Temporarily disable the checkbox to prevent multiple clicks until confirmation
    $checkbox.prop("disabled", true);
  });

  // Handle confirmation modal buttons
  $confirmModalButton.on("click", function () {
    if (!currentActionType) return;

    // Run specific function based on action type
    switch (currentActionType) {
      case "enable_auto_accept":
        enableAutoAccept();
        break;
      case "disable_auto_accept":
        disableAutoAccept();
        break;
      case "enable_auto_reject":
        enableAutoReject();
        break;
      case "disable_auto_reject":
        disableAutoReject();
        break;
      // Additional cases for other actions
    }

    // Close modal without reverting the checkbox state
    closeModal();
  });

  // Close modal on cancel or close button
  $cancelModalButton.on("click", function () {
    closeModal(true); // Revert checkbox state on cancel
  });
  $closeModalButton.on("click", function () {
    closeModal(true); // Revert checkbox state on close
  });

  // Handle overlay click outside modal content to close
  $modalOverlay.on("click", function (event) {
    if ($(event.target).is($modalOverlay)) {
      closeModal(true); // Revert checkbox state on overlay click
    }
  });
  // Additional: Handle keyboard accessibility for the modal
  $modalOverlay.on("keydown", function (e) {
    if (e.key === "Escape") {
      closeModal(true);
    }
  });

  // Optional: Update labels on page load based on checkbox states
  $(".pilarease-itrc-toggle-checkbox").each(function () {
    updateToggleLabel($(this));
  });
  // Function to enable Auto Accept
  function enableAutoAccept() {
    $.ajax({
      url: window.toggleAutoAcceptUrl,
      type: "POST",
      data: {
        enabled: true,
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success("Auto Accept All has been enabled.");
          location.reload(); // Reload the page upon success
        } else {
          toastr.error("Failed to enable Auto Accept All.");
          closeModal(true); // Revert checkbox state
        }
      },
      error: function () {
        toastr.error("An error occurred while enabling Auto Accept All.");
        closeModal(true); // Revert checkbox state
      },
    });
  }

  // Function to disable Auto Accept
  function disableAutoAccept() {
    $.ajax({
      url: window.toggleAutoAcceptUrl,
      type: "POST",
      data: {
        enabled: false,
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success("Auto Accept All has been disabled.");

          // Update Auto Accept checkbox label
          const $acceptCheckbox = $("#autoAcceptCheckbox");
          updateToggleLabel($acceptCheckbox);
          $acceptCheckbox.prop("disabled", false); // Re-enable checkbox
        } else {
          toastr.error("Failed to disable Auto Accept All.");
          closeModal(true); // Revert checkbox state
        }
      },
      error: function () {
        toastr.error("An error occurred while disabling Auto Accept All.");
        closeModal(true); // Revert checkbox state
      },
    });
  }

  // Function to enable Auto Reject
  function enableAutoReject() {
    $.ajax({
      url: window.toggleAutoRejectUrl,
      type: "POST",
      data: {
        enabled: true,
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success("Auto Reject All has been enabled.");
          location.reload(); // Reload the page upon success
        } else {
          toastr.error("Failed to enable Auto Reject All.");
          closeModal(true); // Revert checkbox state
        }
      },
      error: function () {
        toastr.error("An error occurred while enabling Auto Reject All.");
        closeModal(true); // Revert checkbox state
      },
    });
  }

  // Function to disable Auto Reject
  function disableAutoReject() {
    $.ajax({
      url: window.toggleAutoRejectUrl,
      type: "POST",
      data: {
        enabled: false,
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success("Auto Reject All has been disabled.");
          location.reload(); // Reload the page upon success
        } else {
          toastr.error("Failed to disable Auto Reject All.");
          closeModal(true); // Revert checkbox state
        }
      },
      error: function () {
        toastr.error("An error occurred while disabling Auto Reject All.");
        closeModal(true); // Revert checkbox state
      },
    });
  }
  // Helper Functions to Disable the Opposite Setting
  function disableAutoAccept() {
    $.ajax({
      url: window.toggleAutoAcceptUrl,
      type: "POST",
      data: {
        enabled: false,
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success("Auto Accept All has been disabled.");
          location.reload(); // Reload the page upon success
        } else {
          toastr.error("Failed to disable Auto Accept All.");
          closeModal(true); // Revert checkbox state
        }
      },
      error: function () {
        toastr.error("An error occurred while disabling Auto Accept All.");
        closeModal(true); // Revert checkbox state
      },
    });
  }

  function disableAutoRejectButton(revert = true) {
    const $rejectCheckbox = $("#autoRejectCheckbox");
    if ($rejectCheckbox.is(":checked")) {
      $rejectCheckbox.prop("checked", false);
      updateToggleLabel($rejectCheckbox);
      // Send AJAX request to disable Auto Reject
      $.ajax({
        url: window.toggleAutoRejectUrl,
        type: "POST",
        data: {
          enabled: false,
          csrfmiddlewaretoken: window.csrfToken,
        },
        success: function (response) {
          if (response.success) {
            toastr.info(
              "Auto Reject All has been disabled due to enabling Auto Accept All."
            );
          } else {
            toastr.error("Failed to disable Auto Reject All.");
            if (revert) closeModal(true);
          }
        },
        error: function () {
          toastr.error("An error occurred while disabling Auto Reject All.");
          if (revert) closeModal(true);
        },
      });
    }
  }

  // Function to accept a user
  function acceptUser(userId) {
    $.ajax({
      url: window.manualAcceptUserUrl.replace("0", userId), // Ensure this URL is defined
      type: "POST",
      data: {
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success(response.message);
          // Remove the user row or update it to reflect the new status
          $(`button.accept-user-button[data-user-id="${userId}"]`)
            .closest("tr")
            .fadeOut(500, function () {
              $(this).remove();
            });
        } else {
          toastr.error(response.message);
        }
      },
      error: function () {
        toastr.error("An error occurred while accepting the user.");
      },
    });
  }

  // Function to reject a user
  function rejectUser(userId) {
    // Prompt for remarks using a custom modal instead of prompt for better UX
    const remarks = prompt("Enter remarks for rejection:");
    if (remarks === null) return; // User cancelled

    if (remarks.trim() === "") {
      toastr.error("Rejection remarks cannot be empty.");
      return;
    }

    $.ajax({
      url: window.manualRejectUserUrl.replace("0", userId), // Ensure this URL is defined
      type: "POST",
      data: {
        remarks: remarks,
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success(response.message);
          // Remove the user row or update it to reflect the new status
          $(`button.reject-user-button[data-user-id="${userId}"]`)
            .closest("tr")
            .fadeOut(500, function () {
              $(this).remove();
            });
        } else {
          toastr.error(response.message);
        }
      },
      error: function () {
        toastr.error("An error occurred while rejecting the user.");
      },
    });
  }

  // Event listener for toggle checkboxes - to prevent multiple modals or actions
  // This ensures that only one action is processed at a time
  let isProcessingToggle = false;
  $(".pilarease-itrc-toggle-checkbox").on("click", function (e) {
    if (isProcessingToggle) {
      e.preventDefault();
      return; // Prevent multiple simultaneous actions
    }
    isProcessingToggle = true;

    // The checkbox change event will handle opening the modal
    // So we don't need to do anything else here

    // Reset the processing flag after a short delay to prevent rapid clicks
    setTimeout(() => {
      isProcessingToggle = false;
    }, 500); // Adjust the delay as needed
  });

  // Additional: Handle keyboard accessibility for the modal
  $modalOverlay.on("keydown", function (e) {
    if (e.key === "Escape") {
      closeModal(true); // Revert checkbox state
    }
  });

  // Optional: Update labels on page load based on checkbox states
  $(".pilarease-itrc-toggle-checkbox").each(function () {
    updateToggleLabel($(this));
  });
});

// notifications.js

$(document).ready(function () {
  if (window.toastMessages && window.toastMessages.length > 0) {
    // Configure Toastr options
    toastr.options = {
      closeButton: true,
      progressBar: true,
      positionClass: "toast-top-right",
      timeOut: "5000",
      extendedTimeOut: "1000",
      showEasing: "swing",
      hideEasing: "linear",
      showMethod: "fadeIn",
      hideMethod: "fadeOut",
    };

    // Iterate over each message and display it
    window.toastMessages.forEach(function (message) {
      // Ensure the message type is valid; default to 'info'
      const type = message.tags || "info";
      toastr[type](message.message);
    });
  }
});
document.addEventListener("DOMContentLoaded", function () {
  // Select/Deselect All Checkboxes
  const selectAllCheckbox = document.getElementById("select-all");
  const userCheckboxes = document.querySelectorAll(
    ".pilarease-itrc-user-checkbox"
  );

  selectAllCheckbox.addEventListener("change", function () {
    userCheckboxes.forEach((cb) => (cb.checked = this.checked));
  });

  // Handle Bulk Action Form Submission
  const bulkActionForm = document.getElementById("bulk-action-form");
  const bulkActionSelect = document.getElementById("bulk-action-select");
  const bulkActionModalOverlay = document.getElementById(
    "bulkActionModalOverlay"
  );
  const closeBulkActionModal = document.getElementById("closeBulkActionModal");
  const cancelBulkAction = document.getElementById("cancelBulkAction");
  const confirmBulkAction = document.getElementById("confirmBulkAction");

  bulkActionForm.addEventListener("submit", function (e) {
    e.preventDefault();
    const selectedAction = bulkActionSelect.value;
    const selectedUsers = Array.from(
      document.querySelectorAll(".pilarease-itrc-user-checkbox:checked")
    ).map((cb) => cb.value);

    if (!selectedAction) {
      toastr.error("Please select a bulk action to perform.");
      return;
    }

    if (selectedUsers.length === 0) {
      toastr.error("Please select at least one user to perform this action.");
      return;
    }

    // Show the confirmation modal
    bulkActionModalOverlay.style.display = "flex";
  });

  // Confirm Bulk Action
  confirmBulkAction.onclick = function () {
    const selectedAction = bulkActionSelect.value;
    const selectedUsers = Array.from(
      document.querySelectorAll(".pilarease-itrc-user-checkbox:checked")
    ).map((cb) => cb.value);

    // Create a hidden form dynamically to submit the selected action and users
    const form = document.createElement("form");
    form.method = "post";
    form.action = manageUsersBulkActionUrl; // Defined in HTML

    // CSRF Token
    const csrfToken = csrfTokenValue; // Defined in HTML
    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    // Bulk Action
    const actionInput = document.createElement("input");
    actionInput.type = "hidden";
    actionInput.name = "bulk_action";
    actionInput.value = selectedAction;
    form.appendChild(actionInput);

    // Selected Users
    selectedUsers.forEach((userId) => {
      const userInput = document.createElement("input");
      userInput.type = "hidden";
      userInput.name = "selected_users";
      userInput.value = userId;
      form.appendChild(userInput);
    });

    document.body.appendChild(form);
    form.submit();
  };

  // Close Modal on Cancel or Close Button
  closeBulkActionModal.onclick = function () {
    bulkActionModalOverlay.style.display = "none";
  };

  cancelBulkAction.onclick = function () {
    bulkActionModalOverlay.style.display = "none";
  };

  // Close Modal when clicking outside the modal content
  window.onclick = function (event) {
    if (event.target == bulkActionModalOverlay) {
      bulkActionModalOverlay.style.display = "none";
    }
    if (event.target == addUserModalOverlay) {
      addUserModalOverlay.style.display = "none";
    }
  };

  // // Add User Modal Handling
  // const addUserButton = document.getElementById("addUserButton");
  // const addUserModalOverlay = document.getElementById("addUserModalOverlay");
  // const closeAddUserModal = document.getElementById("closeAddUserModal");
  // const cancelAddUser = document.getElementById("cancelAddUser");

  // addUserButton.onclick = function () {
  //   addUserModalOverlay.style.display = "flex";
  // };

  // closeAddUserModal.onclick = function () {
  //   addUserModalOverlay.style.display = "none";
  // };

  // cancelAddUser.onclick = function () {
  //   addUserModalOverlay.style.display = "none";
  // };

  // Activate Button Click Handler
  document.querySelectorAll(".activate-button").forEach(function (button) {
    button.addEventListener("click", function () {
      const userId = this.getAttribute("data-user-id");
      if (confirm("Are you sure you want to activate this user?")) {
        fetch(`/itrc/activate-user/${userId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfTokenValue, // Defined in HTML
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              toastr.success(data.message);
              location.reload();
            } else {
              toastr.error(data.message);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            toastr.error("An error occurred while activating the user.");
          });
      }
    });
  });

  // Deactivate Button Click Handler
  document.querySelectorAll(".deactivate-button").forEach(function (button) {
    button.addEventListener("click", function () {
      const userId = this.getAttribute("data-user-id");
      if (confirm("Are you sure you want to deactivate this user?")) {
        fetch(`/itrc/deactivate-user/${userId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfTokenValue, // Defined in HTML
            "Content-Type": "application/json",
          },
          body: JSON.stringify({}),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              toastr.success(data.message);
              location.reload();
            } else {
              toastr.error(data.message);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            toastr.error("An error occurred while deactivating the user.");
          });
      }
    });
  });

  // Edit Button Click Handler (Optional Enhancement)
  document.querySelectorAll(".edit-button").forEach(function (button) {
    button.addEventListener("click", function () {
      const userId = this.getAttribute("data-user-id");
      window.location.href = `/itrc/edit-user/${userId}/`; // Ensure this URL is defined
    });
  });

  // Role Dropdown Change Handler
  document
    .querySelectorAll(".pilarease-itrc-role-dropdown")
    .forEach(function (dropdown) {
      dropdown.addEventListener("change", function () {
        const userId = this.getAttribute("data-user-id");
        const newRole = this.value;

        fetch(`/itrc/change-role/${userId}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": csrfTokenValue, // Defined in HTML
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ role: newRole }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              toastr.success(data.message);
              location.reload();
            } else {
              toastr.error(data.message);
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            toastr.error("An error occurred while changing the user's role.");
          });
      });
    });
});
// static/js/notifications.js

$(document).ready(function () {
  // Function to get CSRF token from a meta tag
  function getCSRFToken() {
    return $('meta[name="csrf-token"]').attr("content");
  }

  // URLs passed from Django template
  const MARK_AS_READ_URL_TEMPLATE = window.markAsReadUrl; // e.g., "/notifications/mark-as-read/0/"
  const MARK_ALL_AS_READ_URL = window.markAllAsReadUrl; // e.g., "/notifications/mark-all-as-read/"

  // Mark individual notifications as read on click
  $(".notification-item").on("click", function () {
    const notificationId = $(this).data("id");
    const link = $(this).find(".message").data("link"); // Assuming you store the link as a data attribute

    // Construct the URL by replacing the placeholder with the actual ID
    const url = MARK_AS_READ_URL_TEMPLATE.replace("/0/", `/${notificationId}/`);

    // Mark as read via AJAX
    $.ajax({
      url: url,
      type: "POST",
      data: {
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (response.success) {
          // Update the notification item class
          $(`.notification-item[data-id="${notificationId}"]`)
            .removeClass("unread")
            .addClass("read");
        }
      },
      error: function (xhr, errmsg, err) {
        console.error("Error marking notification as read:", errmsg);
      },
    });

    // Redirect to the notification link if it exists
    if (link) {
      window.location.href = link;
    }
  });

  // Mark all notifications as read
  $("#markAllAsRead").on("click", function () {
    $.ajax({
      url: MARK_ALL_AS_READ_URL,
      type: "POST",
      data: {
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (response.success) {
          // Update all notification items
          $(".notification-item").removeClass("unread").addClass("read");
        }
      },
      error: function (xhr, errmsg, err) {
        console.error("Error marking all notifications as read:", errmsg);
      },
    });
  });
});
// itrc_tools/static/js/add_user_validation.js

$(document).ready(function () {
  // Function to get CSRF token from a meta tag
  function getCSRFToken() {
    return $('meta[name="csrf-token"]').attr("content");
  }

  // Real-time validation for username uniqueness
  $("#id_username").on("blur", function () {
    const username = $(this).val().trim();
    const $errorDiv = $(this)
      .closest(".itrc-add-user-form-group")
      .find(".itrc-add-user-error");

    if (username.length < 3) {
      $errorDiv.text("Username must be at least 3 characters long.");
      $(this).addClass("itrc-add-user-input-error");
      return;
    }

    $.ajax({
      url: "/itrc/check-unique/", // Define this URL in your URLs
      type: "POST",
      data: {
        field: "username",
        value: username,
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (!response.is_unique) {
          $errorDiv.text("This username is already taken.");
          $("#id_username").addClass("itrc-add-user-input-error");
        } else {
          $errorDiv.text("");
          $("#id_username").removeClass("itrc-add-user-input-error");
        }
      },
      error: function () {
        $errorDiv.text("An error occurred while validating the username.");
        $("#id_username").addClass("itrc-add-user-input-error");
      },
    });
  });

  // Real-time validation for email uniqueness
  $("#id_email").on("blur", function () {
    const email = $(this).val().trim().toLowerCase();
    const $errorDiv = $(this)
      .closest(".itrc-add-user-form-group")
      .find(".itrc-add-user-error");

    if (email === "") {
      $errorDiv.text("Email is required.");
      $(this).addClass("itrc-add-user-input-error");
      return;
    }

    $.ajax({
      url: "/itrc/check-unique/",
      type: "POST",
      data: {
        field: "email",
        value: email,
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (!response.is_unique) {
          $errorDiv.text("This email is already registered.");
          $("#id_email").addClass("itrc-add-user-input-error");
        } else {
          $errorDiv.text("");
          $("#id_email").removeClass("itrc-add-user-input-error");
        }
      },
      error: function () {
        $errorDiv.text("An error occurred while validating the email.");
        $("#id_email").addClass("itrc-add-user-input-error");
      },
    });
  });

  // Real-time validation for student ID uniqueness
  $("#id_student_id").on("blur", function () {
    const student_id = $(this).val().trim();
    const $errorDiv = $(this)
      .closest(".itrc-add-user-form-group")
      .find(".itrc-add-user-error");

    if (student_id === "") {
      $errorDiv.text("Student ID is required.");
      $(this).addClass("itrc-add-user-input-error");
      return;
    }

    $.ajax({
      url: "/itrc/check-unique/",
      type: "POST",
      data: {
        field: "student_id",
        value: student_id,
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (!response.is_unique) {
          $errorDiv.text("This student ID is already in use.");
          $("#id_student_id").addClass("itrc-add-user-input-error");
        } else {
          $errorDiv.text("");
          $("#id_student_id").removeClass("itrc-add-user-input-error");
        }
      },
      error: function () {
        $errorDiv.text("An error occurred while validating the student ID.");
        $("#id_student_id").addClass("itrc-add-user-input-error");
      },
    });
  });
});

$(document).ready(function () {
  // Real-time validation for username
  $("#id_username").on("input", function () {
    const username = $(this).val();
    if (username.length < 3) {
      $(this).addClass("itrc-edit-user-input-error");
      $(this)
        .next(".itrc-edit-user-error")
        .text("Username must be at least 3 characters long.");
    } else {
      $(this).removeClass("itrc-edit-user-input-error");
      $(this).next(".itrc-edit-user-error").text("");
    }
  });

  // Similarly, add validation for other fields as needed
});
// itrc_tools/static/js/edit_user_validation.js

$(document).ready(function () {
  // Function to get CSRF token from a meta tag
  function getCSRFToken() {
    return $('meta[name="csrf-token"]').attr("content");
  }

  // Real-time validation for username uniqueness
  $("#id_username").on("blur", function () {
    const username = $(this).val().trim();
    const $errorDiv = $(this)
      .closest(".itrc-edit-user-form-group")
      .find(".itrc-edit-user-error");

    // If the username hasn't changed, skip validation
    const originalUsername = $(this).data("original");
    if (username.toLowerCase() === originalUsername.toLowerCase()) {
      $errorDiv.text("");
      $(this).removeClass("itrc-edit-user-input-error");
      return;
    }

    if (username.length < 3) {
      $errorDiv.text("Username must be at least 3 characters long.");
      $(this).addClass("itrc-edit-user-input-error");
      return;
    }

    $.ajax({
      url: "/itrc/check-unique/",
      type: "POST",
      data: {
        field: "username",
        value: username,
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (!response.is_unique) {
          $errorDiv.text("This username is already taken.");
          $("#id_username").addClass("itrc-edit-user-input-error");
        } else {
          $errorDiv.text("");
          $("#id_username").removeClass("itrc-edit-user-input-error");
        }
      },
      error: function () {
        $errorDiv.text("An error occurred while validating the username.");
        $("#id_username").addClass("itrc-edit-user-input-error");
      },
    });
  });

  // Real-time validation for email uniqueness
  $("#id_email").on("blur", function () {
    const email = $(this).val().trim().toLowerCase();
    const $errorDiv = $(this)
      .closest(".itrc-edit-user-form-group")
      .find(".itrc-edit-user-error");

    // If the email hasn't changed, skip validation
    const originalEmail = $(this).data("original");
    if (email === originalEmail.toLowerCase()) {
      $errorDiv.text("");
      $(this).removeClass("itrc-edit-user-input-error");
      return;
    }

    if (email === "") {
      $errorDiv.text("Email is required.");
      $(this).addClass("itrc-edit-user-input-error");
      return;
    }

    $.ajax({
      url: "/itrc/check-unique/",
      type: "POST",
      data: {
        field: "email",
        value: email,
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (!response.is_unique) {
          $errorDiv.text("This email is already registered.");
          $("#id_email").addClass("itrc-edit-user-input-error");
        } else {
          $errorDiv.text("");
          $("#id_email").removeClass("itrc-edit-user-input-error");
        }
      },
      error: function () {
        $errorDiv.text("An error occurred while validating the email.");
        $("#id_email").addClass("itrc-edit-user-input-error");
      },
    });
  });

  // Real-time validation for student ID uniqueness
  $("#id_student_id").on("blur", function () {
    const student_id = $(this).val().trim();
    const $errorDiv = $(this)
      .closest(".itrc-edit-user-form-group")
      .find(".itrc-edit-user-error");

    // If the student ID hasn't changed, skip validation
    const originalStudentID = $(this).data("original");
    if (student_id.toLowerCase() === originalStudentID.toLowerCase()) {
      $errorDiv.text("");
      $(this).removeClass("itrc-edit-user-input-error");
      return;
    }

    if (student_id === "") {
      $errorDiv.text("Student ID is required.");
      $(this).addClass("itrc-edit-user-input-error");
      return;
    }

    $.ajax({
      url: "/itrc/check-unique/",
      type: "POST",
      data: {
        field: "student_id",
        value: student_id,
        csrfmiddlewaretoken: getCSRFToken(),
      },
      success: function (response) {
        if (!response.is_unique) {
          $errorDiv.text("This student ID is already in use.");
          $("#id_student_id").addClass("itrc-edit-user-input-error");
        } else {
          $errorDiv.text("");
          $("#id_student_id").removeClass("itrc-edit-user-input-error");
        }
      },
      error: function () {
        $errorDiv.text("An error occurred while validating the student ID.");
        $("#id_student_id").addClass("itrc-edit-user-input-error");
      },
    });
  });

  // Optional: Password Strength Indicator
  $("#id_password").on("input", function () {
    const password = $(this).val();
    const $errorDiv = $(this)
      .closest(".itrc-edit-user-form-group")
      .find(".itrc-edit-user-error");

    // Simple password strength check
    const strength = getPasswordStrength(password);

    if (password.length > 0 && strength < 3) {
      $errorDiv.text(
        "Password is too weak. Consider adding numbers and special characters."
      );
      $(this).addClass("itrc-edit-user-input-error");
    } else {
      $errorDiv.text("");
      $(this).removeClass("itrc-edit-user-input-error");
    }
  });

  function getPasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[\W]/.test(password)) strength++;
    return strength;
  }
});
