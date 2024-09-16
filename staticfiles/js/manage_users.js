document.addEventListener("DOMContentLoaded", function () {
  const blockButtons = document.querySelectorAll(".block-button");
  const blockUserModal = document.getElementById("blockUserModal");
  const closeBlockUserModal = document.getElementById("closeBlockUserModal");
  const blockUserForm = document.getElementById("blockUserForm");
  const blockUserIdInput = document.getElementById("blockUserId");

  blockButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const userId = this.dataset.userId;
      blockUserIdInput.value = userId;
      blockUserModal.style.display = "block";
    });
  });

  closeBlockUserModal.addEventListener("click", function () {
    blockUserModal.style.display = "none";
  });

  blockUserForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const userId = blockUserIdInput.value;
    const reason = document.getElementById("reason").value;
    const duration = document.getElementById("duration").value;

    fetch(`/block_user/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        user_id: userId,
        reason: reason,
        duration: duration,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          alert("User blocked successfully!");
          blockUserModal.style.display = "none";
          location.reload();
        } else {
          alert("Error blocking user: " + data.error);
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

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
});
