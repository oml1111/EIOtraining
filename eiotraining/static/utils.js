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
	document.head.appendChild(addStylesNode.childNodes[0])
	addStylesNode.parentElement.removeChild(addStylesNode);
}