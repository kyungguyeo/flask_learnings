$(document).ready(function() {
	var $filename = window.location.href.substr(window.location.href.lastIndexOf("/") + 1);
	if ($filename == 'showSignUp') {
		$('a:eq(2)').addClass('active');
	} else if ($filename == 'showSignIn') {
		$('a:eq(1)').addClass('active');
	} else if ($filename == '') {
		$('a:eq(0)').addClass('active');
	};
});

