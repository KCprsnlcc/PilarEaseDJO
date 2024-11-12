// profile.js

document.addEventListener("DOMContentLoaded", function () {
  /* ======================================================
     Helper Functions
  ====================================================== */

  /**
   * Retrieves the CSRF token from browser cookies.
   * Necessary for secure POST and DELETE requests.
   */
  function getCSRFToken() {
    let cookieValue = null;
    const name = "csrftoken";
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  /**
   * Formats a timestamp into a human-readable "time ago" format.
   * @param {string} timestamp - The timestamp to format.
   * @returns {string} - Formatted time ago string.
   */
  function formatTimestamp(timestamp) {
    const now = new Date();
    const createdAt = new Date(timestamp);
    const diffInSeconds = Math.floor((now - createdAt) / 1000);

    const intervals = [
      { label: "year", seconds: 31536000 },
      { label: "month", seconds: 2592000 },
      { label: "week", seconds: 604800 },
      { label: "day", seconds: 86400 },
      { label: "hour", seconds: 3600 },
      { label: "minute", seconds: 60 },
      { label: "second", seconds: 1 },
    ];

    for (let interval of intervals) {
      const count = Math.floor(diffInSeconds / interval.seconds);
      if (count >= 1) {
        return `${count} ${interval.label}${count !== 1 ? "s" : ""} ago`;
      }
    }
    return "Just now";
  }

  /* ======================================================
     Tab Navigation
  ====================================================== */

  const tabs = document.querySelectorAll(".pilarease-profile-tab");
  const tabPanes = document.querySelectorAll(".pilarease-profile-tab-pane");

  tabs.forEach((tab) => {
    tab.addEventListener("click", function () {
      // Remove active class from all tabs
      tabs.forEach((t) => t.classList.remove("pilarease-profile-tab-active"));
      // Add active class to the clicked tab
      this.classList.add("pilarease-profile-tab-active");

      // Hide all tab panes
      tabPanes.forEach((pane) =>
        pane.classList.remove("pilarease-profile-tab-pane-active")
      );
      // Show the associated tab pane
      const target = this.getAttribute("data-tab");
      document
        .getElementById(`pilarease-profile-${target}`)
        .classList.add("pilarease-profile-tab-pane-active");

      // Manage infinite scroll event listeners based on active tab
      if (target === "statuses") {
        window.addEventListener("scroll", handleStatusScroll);
        window.removeEventListener("scroll", handleActivityScroll);
      } else if (target === "activity") {
        window.addEventListener("scroll", handleActivityScroll);
        window.removeEventListener("scroll", handleStatusScroll);
      } else {
        window.removeEventListener("scroll", handleStatusScroll);
        window.removeEventListener("scroll", handleActivityScroll);
      }
    });
  });

  /* ======================================================
     Statuses Section
  ====================================================== */

  let statusPage = 1;
  let statusIsLoading = false;
  let statusHasNext = true;
  const pilareaseProfileStatusContainer = document.getElementById(
    "pilareaseProfileStatusContainer"
  );
  const pilareaseProfileStatusLoader =
    document.getElementById("ProfileCSSLoader");
  const pilareaseProfileStatusOverlay =
    document.getElementById("ProfileCSSOverlay");

  // Initial fetch of statuses
  fetchPilareaseStatuses(statusPage);

  /**
   * Handles the scroll event for infinite scrolling in the Statuses tab.
   */
  function handleStatusScroll() {
    if (
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 &&
      !statusIsLoading &&
      statusHasNext &&
      document
        .getElementById("pilarease-profile-statuses")
        .classList.contains("pilarease-profile-tab-pane-active")
    ) {
      statusPage++;
      fetchPilareaseStatuses(statusPage);
    }
  }

  /**
   * Fetches user statuses from the server and appends them to the DOM.
   * @param {number} page - The page number to fetch.
   */
  function fetchPilareaseStatuses(page) {
    statusIsLoading = true;
    pilareaseProfileStatusLoader.style.display = "block";
    pilareaseProfileStatusOverlay.style.display = "block";

    fetch(`/get_user_statuses/?page=${page}`)
      .then((response) => response.json())
      .then((data) => {
        statusIsLoading = false;
        pilareaseProfileStatusLoader.style.display = "none";
        pilareaseProfileStatusOverlay.style.display = "none";

        data.statuses.forEach((status) => {
          const statusBox = document.createElement("div");
          statusBox.classList.add(
            "pilarease-profile-status-box",
            "animate__animated",
            "animate__fadeInUp"
          );
          statusBox.setAttribute("data-id", status.id);

          // Truncate status description to 250 characters
          let truncatedDescription = status.description.slice(0, 250);
          if (status.description.length > 250) {
            truncatedDescription += "...";
          }

          statusBox.innerHTML = `
  <div class="pilarease-profile-status-header">
    <img src="${status.avatar_url}" alt="${
            status.username
          }'s Avatar" class="pilarease-profile-status-avatar" loading="lazy"/>
    <div>
      <p class="pilarease-profile-status-username">${status.username}</p>
      <span class="pilarease-profile-status-time">${formatTimestamp(
        status.created_at
      )}</span>
    </div>
  </div>
  <h3 class="pilarease-profile-status-title">${status.title}</h3>
  <p class="pilarease-profile-status-description">${truncatedDescription}</p>
  <div class="pilarease-profile-status-actions">
    <button id="reply-${
      status.id
    }" class="pilarease-profile-action-button reply-button">
      <i class="bx bx-comment"></i> Replies (${status.replies})
    </button>
    <button id="view-${
      status.id
    }" class="pilarease-profile-action-button view-button" onclick="viewPilareaseStatus(${
            status.id
          })">
      <i class="bx bx-show"></i> View
    </button>
    ${
      status.can_edit
        ? `<button id="delete-${status.id}" class="pilarease-profile-action-button delete-button" onclick="deletePilareaseStatus(${status.id})">
            <i class="bx bx-trash"></i> Delete
          </button>`
        : ""
    }
  </div>
`;

          pilareaseProfileStatusContainer.appendChild(statusBox);

          statusBox.addEventListener("animationend", function () {
            statusBox.classList.remove("animate__fadeInUp");
          });
        });

        statusHasNext = data.has_next;
      })
      .catch((error) => {
        statusIsLoading = false;
        pilareaseProfileStatusLoader.style.display = "none";
        pilareaseProfileStatusOverlay.style.display = "none";
        console.error("Error fetching user statuses:", error);
      });
  }

  /* ======================================================
     Analytics Section
  ====================================================== */

  const pilareaseProfileStatusChart = document.getElementById(
    "pilareaseProfileStatusChart"
  );

  // Fetch Analytics Data and Render Chart
  fetchPilareaseAnalytics();

  /**
   * Fetches analytics data from the server.
   */
  function fetchPilareaseAnalytics() {
    fetch(`/get_user_analytics/`)
      .then((response) => response.json())
      .then((data) => {
        // Render Chart
        renderStatusChart(data.statuses_over_time);
      })
      .catch((error) => {
        console.error("Error fetching analytics data:", error);
      });
  }

  /**
   * Renders a line chart using Chart.js with the provided data.
   * @param {Array} statusesOverTime - Array of objects containing date and count of statuses and replies.
   */
  function renderStatusChart(statusesOverTime) {
    const ctx = pilareaseProfileStatusChart.getContext("2d");
    const labels = statusesOverTime.map((item) => item.date);
    const statusCounts = statusesOverTime.map((item) => item.status_count);
    const replyCounts = statusesOverTime.map((item) => item.reply_count);

    new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Statuses Posted",
            data: statusCounts,
            backgroundColor: "rgba(14, 35, 38, 0.2)",
            borderColor: "rgba(14, 35, 38, 1)",
            borderWidth: 2,
            pointRadius: 4,
            pointBackgroundColor: "rgba(14, 35, 38, 1)",
            fill: true,
            tension: 0.3,
          },
          {
            label: "Replies Created",
            data: replyCounts,
            backgroundColor: "rgba(104, 158, 75, 0.2)",
            borderColor: "rgba(104, 158, 75, 1)",
            borderWidth: 2,
            pointRadius: 4,
            pointBackgroundColor: "rgba(104, 158, 75, 1)",
            fill: true,
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              color: getComputedStyle(document.documentElement)
                .getPropertyValue("--pilarease-profile-text-color")
                .trim(),
            },
            grid: {
              color: getComputedStyle(document.documentElement)
                .getPropertyValue("--pilarease-profile-light-gray")
                .trim(),
            },
          },
          x: {
            ticks: {
              color: getComputedStyle(document.documentElement)
                .getPropertyValue("--pilarease-profile-text-color")
                .trim(),
            },
            grid: {
              color: getComputedStyle(document.documentElement)
                .getPropertyValue("--pilarease-profile-light-gray")
                .trim(),
            },
          },
        },
        plugins: {
          legend: {
            labels: {
              color: getComputedStyle(document.documentElement)
                .getPropertyValue("--pilarease-profile-text-color")
                .trim(),
            },
          },
        },
      },
    });
  }

  /* ======================================================
     Recent Activity Section
  ====================================================== */

  let activityPage = 1;
  let activityIsLoading = false;
  let activityHasNext = true;
  const pilareaseProfileActivityContainer = document.getElementById(
    "pilareaseProfileActivityContainer"
  );
  const pilareaseProfileActivityLoader =
    document.getElementById("ProfileCSSLoader");
  const pilareaseProfileActivityOverlay =
    document.getElementById("ProfileCSSOverlay");

  // Initial fetch of recent activities
  fetchPilareaseActivities(activityPage);

  /**
   * Handles the scroll event for infinite scrolling in the Recent Activity tab.
   */
  function handleActivityScroll() {
    if (
      window.innerHeight + window.scrollY >= document.body.offsetHeight - 100 &&
      !activityIsLoading &&
      activityHasNext &&
      document
        .getElementById("activity")
        .classList.contains("pilarease-profile-tab-pane-active")
    ) {
      activityPage++;
      fetchPilareaseActivities(activityPage);
    }
  }

  /**
   * Fetches recent activities from the server and appends them to the DOM.
   * @param {number} page - The page number to fetch.
   */
  function fetchPilareaseActivities(page) {
    activityIsLoading = true;
    pilareaseProfileActivityLoader.style.display = "block";
    pilareaseProfileActivityOverlay.style.display = "block";

    fetch(`/get_recent_activity/?page=${page}`)
      .then((response) => response.json())
      .then((data) => {
        activityIsLoading = false;
        pilareaseProfileActivityLoader.style.display = "none";
        pilareaseProfileActivityOverlay.style.display = "none";

        data.activities.forEach((activity) => {
          const activityItem = document.createElement("div");
          activityItem.classList.add(
            "pilarease-profile-activity-item",
            "animate__animated",
            "animate__fadeInUp"
          );

          activityItem.innerHTML = `
            <p><strong>${activity.actor}</strong> ${
            activity.action
          } your status titled "<em>${activity.status_title}</em>".</p>
            <span class="pilarease-profile-activity-time">${formatTimestamp(
              activity.timestamp
            )}</span>
          `;

          pilareaseProfileActivityContainer.appendChild(activityItem);

          // Remove 'animate__fadeInUp' class after animation to prevent re-animation
          activityItem.addEventListener("animationend", function () {
            activityItem.classList.remove("animate__fadeInUp");
          });
        });

        activityHasNext = data.has_next;
      })
      .catch((error) => {
        activityIsLoading = false;
        pilareaseProfileActivityLoader.style.display = "none";
        pilareaseProfileActivityOverlay.style.display = "none";
        console.error("Error fetching recent activities:", error);
      });
  }
  /* ======================================================
     Status Actions
  ====================================================== */

  /**
   * Redirects the user to the status edit page.
   * @param {number} statusId - The ID of the status to edit.
   */

  window.viewPilareaseStatus = function (statusId) {
    window.location.href = `/status/${statusId}/`; // Redirect to the status detail page
  };

  /**
   * Deletes a status after user confirmation and removes it from the DOM with an animation.
   * @param {number} statusId - The ID of the status to delete.
   */
  window.deletePilareaseStatus = function (statusId) {
    if (confirm("Are you sure you want to delete this status?")) {
      fetch(`/delete_status/${statusId}/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({}), // Include body if your Django view expects it
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // Remove the status box from the DOM with fade-out animation
            const statusBox = document.querySelector(
              `.pilarease-profile-status-box[data-id="${statusId}"]`
            );
            if (statusBox) {
              statusBox.classList.add("animate__fadeOut");
              statusBox.addEventListener("animationend", () => {
                statusBox.remove();
              });
            }
          } else {
            alert(data.message || "Failed to delete status.");
          }
        })
        .catch((error) => {
          console.error("Error deleting status:", error);
          alert("An error occurred while deleting the status.");
        });
    }
  };
});
