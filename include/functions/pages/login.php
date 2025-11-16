<?php
	if(isset($_POST['username']) && isset($_POST['password']))
	{
		$username = strip_tags($_POST['username']);
		$password = strip_tags($_POST['password']);
		
		if(isset($_POST['g-recaptcha-response']) && !empty($_POST['g-recaptcha-response'])) {
			$verifyResponse = @file_get_contents('https://www.google.com/recaptcha/api/siteverify?secret='.$secret_key.'&response='.$_POST['g-recaptcha-response']);

			if($verifyResponse !== false) {
				$responseData = json_decode($verifyResponse);

				if($responseData && $responseData->success) {
				   $login_info = $database->doLogin($username,$password);
				   // Security: Regenerate session ID to prevent session fixation attacks
				   if(isset($login_info[0]) && $login_info[0] == 1) {
					   session_regenerate_id(true);
				   }
				} else $login_info = array(6);
			} else {
				$login_info = array(6);
			}
		} else $login_info = array(6);
	}
?>