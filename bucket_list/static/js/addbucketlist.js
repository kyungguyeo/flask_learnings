$(document).ready(function() {
	// $('.jumbotron .form-group p').prepend($('<h3>/',{'text': "Hello " + window.location.search.split("=")[1] + "!"})) //Add a greeting
	$('#AddBucketList').click(function() {
		$('#addlisthere')
			.append($('<div/>',{'class':'card card-inverse card-primary text-xs-center col-lg-6'})
				.append($('<div/>',{'class':'card-block'})
					.append($('<h4/>',{'class':'card-title','text':$('input').val()}))
					.append($('<div/>',{'class':'btn-group','role':'group'})
						.append($('<button/>',{'class':'btn btn-success', 'text': "It's Done!", 'type':"button"}).on("click", function() {
							$(this).parent().parent().parent().remove();
						}))
						.append($('<button/>',{'class':'btn btn-danger', 'text': 'Remove', 'type':"button"}).on("click", function() {
							$(this).parent().parent().parent().remove();
						}))
						)
					.append($('<footer/>',{'text': $.datepicker.formatDate('M d, yy', new Date()), 'class':'text-muted'}))
				)
			)		
	});
})

