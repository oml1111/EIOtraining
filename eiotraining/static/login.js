function onSignIn(googleUser) {
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
	if(response == "Success") {
		if(window.location.pathname.substr(0,3) == "/et")
			window.location = "/et/"
		else
			window.location = "/";
	}
	else {
	  signOut();
	}
  };
  xhr.send('idtoken=' + id_token);

}

window.onLoadCallback = function(){
	alert("Callback Done!");
}