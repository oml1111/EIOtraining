function onSignIn(googleUser) {
  alert("Logged to Google!");
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log('Name: ' + profile.getName());
  console.log('Image URL: ' + profile.getImageUrl());
  console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
  
  var id_token = googleUser.getAuthResponse().id_token;
  
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/googlelogin');
  xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
  
  xhr.onload = function() {
	alert("Backend authentication done:" + "xhr.responseText");
  };
  xhr.send('idtoken=' + id_token);


  window.location = "/problemset";
}
