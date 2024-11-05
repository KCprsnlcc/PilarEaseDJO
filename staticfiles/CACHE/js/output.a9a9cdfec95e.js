document.addEventListener("DOMContentLoaded",function(){const notificationButton=document.getElementById("pilareaseAdminNotificationButton");const notificationDot=document.getElementById("pilareaseAdminNotificationDot");const notificationList=document.getElementById("pilareaseAdminNotificationList");const notificationItems=document.getElementById("pilareaseAdminNotificationItems");const loadMoreButton=document.getElementById("pilareaseAdminNotificationLoadMore");const seeAllLink=document.querySelector(".pilarease-admin-notification-header .pilarease-admin-see-all");let currentPage=1;let totalPages=1;let renderedNotifications=new Map();function showNotificationLoader(){const loader=document.createElement("div");loader.className="pilarease-admin-loader-placeholder";for(let i=0;i<3;i++){const loaderItem=document.createElement("div");loaderItem.className="pilarease-admin-loader-item";loaderItem.innerHTML=`
        <div class="pilarease-admin-loader-item-avatar"></div>
        <div class="pilarease-admin-loader-item-content"></div>
        <div class="pilarease-admin-loader-item-timestamp"></div>
      `;loader.appendChild(loaderItem);}
notificationItems.appendChild(loader);}
function removeNotificationLoader(){const loader=document.querySelector(".pilarease-admin-loader-placeholder");if(loader){loader.remove();}}
async function fetchNotifications(page=1){try{showNotificationLoader();const response=await fetch(`/admin/fetch_counselor_notifications/?page=${page}`);if(response.ok){const data=await response.json();totalPages=data.total_pages;return data.notifications;}else{console.error("Failed to fetch notifications.");return[];}}catch(error){console.error("Error fetching notifications:",error);return[];}finally{removeNotificationLoader();}}
async function markNotificationAsRead(notificationId){try{const response=await fetch(`/admin/mark_counselor_notification_as_read/${notificationId}/`,{method:"POST",headers:{"Content-Type":"application/json","X-CSRFToken":getCSRFToken(),},});if(!response.ok){console.error("Failed to mark notification as read.");}else{renderedNotifications.get(notificationId).is_read=true;}}catch(error){console.error("Error marking notification as read:",error);}}
function getCSRFToken(){const csrfToken=document.querySelector("[name=csrfmiddlewaretoken]");return csrfToken?csrfToken.value:"";}
async function renderNotifications(page=1){const notifications=await fetchNotifications(page);if(notifications.length===0){loadMoreButton.style.display="none";return;}
notifications.sort((a,b)=>new Date(b.timestamp)-new Date(a.timestamp));let hasUnreadNotifications=false;notifications.forEach((notification)=>{if(!renderedNotifications.has(notification.id)){const item=document.createElement("div");item.classList.add("pilarease-admin-notification-item");item.dataset.id=notification.id;if(!notification.is_read){item.classList.add("unread");hasUnreadNotifications=true;}else{item.classList.add("read");}
item.addEventListener("click",async function(){const notificationId=item.dataset.id;if(!notification.is_read){await markNotificationAsRead(notificationId);item.classList.remove("unread");item.classList.add("read");const greenDot=item.querySelector(".pilarease-admin-notification-dot-green");if(greenDot){greenDot.remove();}
item.querySelector(".timestamp").classList.remove("timestamp-green");}
window.location.href=notification.link;});item.innerHTML=`
  <img class="pilarease-admin-notification-avatar" src="${
    notification.avatar
  }" alt="Avatar">
  <div class="pilarease-admin-notification-content">
    <div class="message">${notification.message}</div>
    <div class="timestamp ${notification.is_read ? "" : "timestamp-green"}">
      ${formatTimestamp(notification.timestamp)}
    </div>
  </div>
  ${
    notification.is_read
      ? ""
      : '<div class="pilarease-admin-notification-dot-green"></div>'
  }
`;notificationItems.appendChild(item);renderedNotifications.set(notification.id,notification);}});if(currentPage<totalPages){loadMoreButton.style.display="block";}else{loadMoreButton.style.display="none";}
if(hasUnreadNotifications){notificationDot.style.display="block";notificationDot.classList.add("blink");}else{notificationDot.style.display="none";}}
setInterval(async()=>{const notifications=await fetchNotifications();const hasUnread=notifications.some((notification)=>!notification.is_read);if(hasUnread){notificationDot.style.display="block";notificationDot.classList.add("blink");}},60000);window.addEventListener("click",function(event){if(!notificationButton.contains(event.target)&&!notificationList.contains(event.target)){if(notificationList.style.display==="block"){notificationList.classList.remove("animated");notificationList.classList.add("pop-up");setTimeout(()=>{notificationList.style.display="none";},300);}}});notificationButton.addEventListener("click",async function(){if(notificationList.style.display==="none"){await renderNotifications(currentPage);notificationList.classList.remove("pop-up");notificationList.classList.add("animated");notificationList.style.display="block";notificationDot.style.display="none";}else{notificationList.classList.remove("animated");notificationList.classList.add("pop-up");setTimeout(()=>{notificationList.style.display="none";},300);}});loadMoreButton.addEventListener("click",async function(){currentPage++;await renderNotifications(currentPage);notificationList.style.maxHeight="700px";notificationList.style.overflowY="auto";});if(seeAllLink){seeAllLink.addEventListener("click",function(){window.location.href="/admin/notifications/";});}
function formatTimestamp(timestamp){return moment(timestamp).fromNow();}
renderNotifications();});;