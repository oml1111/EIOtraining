function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
		if(window.location.pathname.substr(0,3) == "/et")
			window.location = "/et/"
		else
			window.location = "/";
	});
}

window.onLoadCallback = function(){
	gapi.load('auth2', function() {
		gapi.auth2.init();
	});
	logoutlink = $("#logoutlink")
	logoutlink.onclick = signOut;
	logoutlink.href="#";
	signOut();
}