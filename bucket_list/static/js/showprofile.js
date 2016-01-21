$(document).ready(function() {
	$('#welcome').text('Welcome ' + location.search.replace('?', '').split('=')[1] + 
	'!');
});