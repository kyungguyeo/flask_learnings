$(function(){
	$('#btnSignIn').click(function(){
		
		$.ajax({
			url: '/signIn',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				window.location.href = response;
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});
