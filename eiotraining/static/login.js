function signOut() {
	document.cookie = "user=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	document.cookie = "password_hash=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
		alert('User signed out.');
		location.reload();
	});
}

window.onLoadCallback = function(){
	gapi.load('auth2', function() {
		gapi.auth2.init();
	});
	logoutlink = $("#logoutlink")
	logoutlink.attr("href", "#")
	logoutlink.attr("onclick", "signOut();")
}

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
	response = xhr.responseText;
	alert("Backend authentication done:" + response);
	if(response == "Success")
	  window.location = "/problemset";
	else {
	  signOut();
	}
  };
  xhr.send('idtoken=' + id_token);

}