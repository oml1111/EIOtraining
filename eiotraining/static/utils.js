function toggle(id) {
	$("#"+id).toggle();
}

function getNews() {
	user=$("#username").val();
	
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/getnews');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	
	xhr.onload = function() {
		response = xhr.responseText;
		$("").innerHTML = response;
	}
	xhr.send('user=' + user);
}