$(document).ready(function() {
	$(".nav-folder").hide();
});
function navtoggle(id) {
	$("#navdiv-"+id).toggle();
	navbutton = $("#navbutton-"+id)
	if(navbutton.attr("class") == "nav-closed") {
		navbutton.attr("class", "nav-open")
	}
	else {
		navbutton.attr("class", "nav-closed")
	}
}