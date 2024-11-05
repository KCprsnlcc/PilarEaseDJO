document.addEventListener("DOMContentLoaded",function(){const notificationButton=document.getElementById("notificationButton");const notificationDot=document.getElementById("notificationDot");const notificationList=document.getElementById("notificationList");const notificationItems=document.getElementById("notificationItems");const loadMoreButton=document.getElementById("notificationLoadMore");let currentPage=1;let totalPages=1;let renderedNotifications=new Map();function showNotificationLoader(){const loader=document.createElement("div");loader.className="loader-placeholder";notificationItems.appendChild(loader);}
function removeNotificationLoader(){const loader=document.querySelector(".loader-placeholder");if(loader){loader.remove();}}
async function fetchNotifications(page=1){try{showNotificationLoader();const response=await fetch(`/admin/fetch_counselor_notifications/?page=${page}`);if(response.ok){const data=await response.json();totalPages=data.total_pages;return data.notifications;}else{console.error("Failed to fetch notifications.");return[];}}catch(error){console.error("Error fetching notifications:",error);return[];}finally{removeNotificationLoader();}}
async function markNotificationAsRead(notificationId){try{const response=await fetch(`/admin/mark_counselor_notification_as_read/${notificationId}/`,{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":getCSRFToken(),},});if(!response.ok){console.error("Failed to mark notification as read.");}else{renderedNotifications.get(notificationId).is_read=true;}}catch(error){console.error("Error marking notification as read:",error);}}
function getCSRFToken(){return document.querySelector("[name=csrfmiddlewaretoken]").value;}
async function renderNotifications(page=1){const notifications=await fetchNotifications(page);if(notifications.length===0){loadMoreButton.style.display="none";return;}
notifications.forEach((notification)=>{if(!renderedNotifications.has(notification.id)){const item=document.createElement("div");item.classList.add("notification-item");item.dataset.id=notification.id;if(!notification.is_read){item.classList.add("unread");}else{item.classList.add("read");}
item.addEventListener("click",async function(){const notificationId=item.dataset.id;if(!notification.is_read){await markNotificationAsRead(notificationId);item.classList.remove("unread");item.classList.add("read");}
window.location.href=notification.link;});item.innerHTML=`
          <img class="notification-avatar" src="${
            notification.avatar
          }" alt="Avatar">
          <div class="notification-content">
            <div class="message">${notification.message}</div>
            <div class="timestamp">${notification.timestamp}</div>
          </div>
          ${
            notification.is_read
              ? ""
              : '<div class="notification-dot-green"></div>'
          }
        `;notificationItems.appendChild(item);renderedNotifications.set(notification.id,notification);}});if(currentPage<totalPages){loadMoreButton.style.display="block";}else{loadMoreButton.style.display="none";}}
notificationButton.addEventListener("click",async function(){if(notificationList.style.display==="none"){await renderNotifications(currentPage);notificationList.style.display="block";notificationDot.style.display="none";}else{notificationList.style.display="none";}});loadMoreButton.addEventListener("click",async function(){currentPage++;await renderNotifications(currentPage);});renderNotifications();});;