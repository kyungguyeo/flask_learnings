$(document).ready(function() {
	$('[id=taskcomplete]').click(function() {
		$(this).parent().parent().parent().parent().remove();
	})

	$('[id=taskremove]').click(function() {
		$(this).parent().parent().parent().parent().remove();
	})
})