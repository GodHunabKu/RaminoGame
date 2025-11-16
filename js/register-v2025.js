$(window).on('load', function() {
	function checkPasswordMatch() {
		var password = $("#password").val();
		var confirmPassword = $("#rpassword").val();

		if (password != confirmPassword)
			$("#checkpassword").html(no_password_r);
		else
			$("#checkpassword").html("");
	}

	function checkUsername() {
		var name = $("#username").val();
		var regex = /^[0-9a-zA-Z]*$/;

		if(!regex.test(name))
			$("#checkname").html(no_special_chars);
		else
			$("#checkname").html("");
	}

	function checkUsername2() {
		var name = $("#username").val();
		var n = name.length;
		var type = 1;

		if(n>=5 && n<=16)
		{
			$.post(site_url + "checkusername.php", { type:type, username:name })
				.done(function(result){
					if(result == 1)
						$('#checkname2').html(name + ' ' + not_available);
					else
						$('#checkname2').html("");
				})
				.fail(function() {
					$('#checkname2').html('<span style="color: #dc3545;">Connection error</span>');
				});
		}
	}

	function checkUserEmail() {
		var email = $("#email").val();
		var type = 2;
		if (email.indexOf("@") >= 0)
		{
			$.post(site_url + "checkusername.php", { type:type, email:email })
				.done(function(result){
					if(result == 1)
						$('#checkemail').html(email + ' ' + not_available);
					else
						$('#checkemail').html("");
				})
				.fail(function() {
					$('#checkemail').html('<span style="color: #dc3545;">Connection error</span>');
				});
		}
	}

	// Register event listeners (no need for $(document).ready since we're already in window.load)
	$("#rpassword").keyup(checkPasswordMatch);
	$("#username").keyup(function() {
		checkUsername();
		checkUsername2();
	});
	$("#email").keyup(checkUserEmail);
});
