$(document).ready(function() {
	$('#taskcomplete').click(function() {
		$(this).parent().parent().parent().remove();
	})

	$('#taskremove').click(function() {
		
		$(this).parent().parent().parent().remove();
		$.ajax({
	        type: "DELETE",
	        data: {column1 : col1, column2 : col2}, // post values
	        success:function(result){
	            window.location.href = $SCRIPT_ROOT + '/main';
	        }
	    });
	})
})