document.addEventListener("DOMContentLoaded",function(){document.querySelectorAll(".curved-line path").forEach(function(path){var controlPointX1=Math.random()*50;var controlPointY1=Math.random()*50;var controlPointX2=100-Math.random()*50;var controlPointY2=Math.random()*50;var endPointX=Math.random()*100;var endPointY=Math.random()*100;var d=`M0,0 C${controlPointX1},${controlPointY1} ${controlPointX2},${controlPointY2} ${endPointX},${endPointY}`;path.setAttribute("d",d);});const loginForm=document.getElementById("adminLoginForm");const errorElement=document.querySelector(".error");loginForm.addEventListener("submit",function(event){const username=document.getElementById("username").value.trim();const password=document.getElementById("password").value.trim();if(errorElement){errorElement.textContent="";errorElement.style.display="none";}
let hasError=false;let errorMessage="";if(username===""){hasError=true;errorMessage="Username is required.";}else if(password===""){hasError=true;errorMessage="Password is required.";}
if(hasError){event.preventDefault();if(errorElement){errorElement.textContent=errorMessage;errorElement.style.display="block";errorElement.style.animation="fadeIn 0.5s";}}});});;