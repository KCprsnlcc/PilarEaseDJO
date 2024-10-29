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
  let currentUserId = null; // Relevant for user actions

  // Function to open modal with dynamic content
  function openModal(actionType, userId = null) {
    currentActionType = actionType;
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

    // Show modal
    $modalOverlay.fadeIn(200);
  }

  // Function to close modal
  function closeModal() {
    $modalOverlay.fadeOut(200);
    currentActionType = null;
    currentUserId = null;
  }

  // Attach a single event listener to toggle buttons
  $(".pilarease-itrc-toggle-button").on("click", function () {
    if (isProcessingToggle) return; // Prevent multiple simultaneous actions
    isProcessingToggle = true;

    const $button = $(this);
    const action = $button.data("action"); // 'accept' or 'reject'
    const isEnabled = $button.attr("data-enabled") === "true";

    if (!isEnabled) {
      // Attempting to enable the setting - show confirmation modal
      const actionType =
        action === "accept" ? "enable_auto_accept" : "enable_auto_reject";
      openModal(actionType);
    } else {
      // Attempting to disable the setting - show confirmation modal
      const actionType =
        action === "accept" ? "disable_auto_accept" : "disable_auto_reject";
      openModal(actionType);
    }

    // Reset the processing flag after a short delay to prevent rapid clicks
    setTimeout(() => {
      isProcessingToggle = false;
    }, 500); // Adjust the delay as needed
  });

  // Attach event listeners to action buttons
  $confirmModalButton.on("click", function () {
    if (!currentActionType) return;

    switch (currentActionType) {
      case "enable_auto_accept":
        enableAutoAccept();
        break;
      case "enable_auto_reject":
        enableAutoReject();
        break;
      case "disable_auto_accept":
        disableAutoAccept();
        break;
      case "disable_auto_reject":
        disableAutoReject();
        break;
      case "accept_user":
        acceptUser(currentUserId);
        break;
      case "reject_user":
        rejectUser(currentUserId);
        break;
      default:
        // Unknown action
        toastr.error("Unknown action.");
    }

    closeModal();
  });

  // Close modal on cancel or close button
  $cancelModalButton.on("click", closeModal);
  $closeModalButton.on("click", closeModal);

  // Close modal when clicking outside the modal content
  $modalOverlay.on("click", function (event) {
    if ($(event.target).is($modalOverlay)) {
      closeModal();
    }
  });

  // Function to enable Auto Accept
  function enableAutoAccept() {
    $.ajax({
      url: window.toggleAutoAcceptUrl, // Ensure this URL is defined in your template
      type: "POST",
      data: {
        enabled: true,
        csrfmiddlewaretoken: window.csrfToken, // Ensure CSRF token is defined
      },
      success: function (response) {
        if (response.success) {
          toastr.success("Auto Accept All has been enabled.");

          // Update Auto Accept button to Enabled state
          const $acceptButton = $("#autoAcceptButton");
          $acceptButton
            .removeClass("disabled")
            .addClass("enabled")
            .html("Enabled")
            .attr("data-enabled", "true");

          // If Auto Reject is enabled, disable it
          const $rejectButton = $("#autoRejectButton");
          if ($rejectButton.attr("data-enabled") === "true") {
            disableAutoRejectButton($rejectButton);
          }
        } else {
          toastr.error("Failed to enable Auto Accept All.");
        }
      },
      error: function () {
        toastr.error("An error occurred while enabling Auto Accept All.");
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

          // Update Auto Accept button to Disabled state
          const $acceptButton = $("#autoAcceptButton");
          $acceptButton
            .removeClass("enabled")
            .addClass("disabled")
            .html("Disabled")
            .attr("data-enabled", "false");
        } else {
          toastr.error("Failed to disable Auto Accept All.");
        }
      },
      error: function () {
        toastr.error("An error occurred while disabling Auto Accept All.");
      },
    });
  }

  // Function to enable Auto Reject
  function enableAutoReject() {
    $.ajax({
      url: window.toggleAutoRejectUrl, // Ensure this URL is defined in your template
      type: "POST",
      data: {
        enabled: true,
        csrfmiddlewaretoken: window.csrfToken,
      },
      success: function (response) {
        if (response.success) {
          toastr.success("Auto Reject All has been enabled.");

          // Update Auto Reject button to Enabled state
          const $rejectButton = $("#autoRejectButton");
          $rejectButton
            .removeClass("disabled")
            .addClass("enabled")
            .html("Enabled")
            .attr("data-enabled", "true");

          // If Auto Accept is enabled, disable it
          const $acceptButton = $("#autoAcceptButton");
          if ($acceptButton.attr("data-enabled") === "true") {
            disableAutoAcceptButton($acceptButton);
          }
        } else {
          toastr.error("Failed to enable Auto Reject All.");
        }
      },
      error: function () {
        toastr.error("An error occurred while enabling Auto Reject All.");
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

          // Update Auto Reject button to Disabled state
          const $rejectButton = $("#autoRejectButton");
          $rejectButton
            .removeClass("enabled")
            .addClass("disabled")
            .html("Disabled")
            .attr("data-enabled", "false");
        } else {
          toastr.error("Failed to disable Auto Reject All.");
        }
      },
      error: function () {
        toastr.error("An error occurred while disabling Auto Reject All.");
      },
    });
  }

  // Helper Functions to Disable the Opposite Setting
  function disableAutoAcceptButton($button) {
    disableAutoAccept();
  }

  function disableAutoRejectButton($button) {
    disableAutoReject();
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

  // Event listener for toggle buttons - to prevent multiple modals or actions
  // This ensures that only one action is processed at a time
  let isProcessingToggle = false;
  $(".pilarease-itrc-toggle-button").on("click", function () {
    if (isProcessingToggle) return; // Prevent multiple simultaneous actions
    isProcessingToggle = true;

    const $button = $(this);
    const action = $button.data("action"); // 'accept' or 'reject'
    const isEnabled = $button.attr("data-enabled") === "true";

    if (!isEnabled) {
      // Attempting to enable the setting - show confirmation modal
      const actionType =
        action === "accept" ? "enable_auto_accept" : "enable_auto_reject";
      openModal(actionType);
    } else {
      // Attempting to disable the setting - show confirmation modal
      const actionType =
        action === "accept" ? "disable_auto_accept" : "disable_auto_reject";
      openModal(actionType);
    }

    isProcessingToggle = false;
  });

  // Additional: Handle keyboard accessibility for the modal
  $modalOverlay.on("keydown", function (e) {
    if (e.key === "Escape") {
      closeModal();
    }
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

  // Add User Modal Handling
  const addUserButton = document.getElementById("addUserButton");
  const addUserModalOverlay = document.getElementById("addUserModalOverlay");
  const closeAddUserModal = document.getElementById("closeAddUserModal");
  const cancelAddUser = document.getElementById("cancelAddUser");

  addUserButton.onclick = function () {
    addUserModalOverlay.style.display = "flex";
  };

  closeAddUserModal.onclick = function () {
    addUserModalOverlay.style.display = "none";
  };

  cancelAddUser.onclick = function () {
    addUserModalOverlay.style.display = "none";
  };

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
