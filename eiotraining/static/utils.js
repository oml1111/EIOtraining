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
		$("#newsfeed").html(response);
	}
	xhr.send('user=' + user);
}

{
	var addStylesNode = document.getElementById("deferred-styles");
	var replacement = document.createElement("link");
	replacement.type = "text/css"
	replacement.rel = "stylesheet"
	replacement.href = "/static/style.css"
	document.head.appendChild(replacement)
	addStylesNode.parentElement.removeChild(addStylesNode);
}