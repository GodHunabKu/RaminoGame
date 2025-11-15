<?php
	if(isset($_POST['username']) && isset($_POST['password']))
	{
		$username = strip_tags($_POST['username']);
		$password = strip_tags($_POST['password']);
		
		if(isset($_POST['g-recaptcha-response']) && !empty($_POST['g-recaptcha-response'])) {
			$verifyResponse = file_get_contents('https://www.google.com/recaptcha/api/siteverify?secret='.$secret_key.'&response='.$_POST['g-recaptcha-response']);
			$responseData = json_decode($verifyResponse);
			
			if($responseData->success)
			   $login_info = $database->doLogin($username,$password);
			else $login_info = array(6);
		} else $login_info = array(6);
	}
?>