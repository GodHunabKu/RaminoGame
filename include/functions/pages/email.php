<?php
	$myEmail = getAccountEmail($_SESSION['id']);
	$message = 0;
	if(isset($_GET['code']) && !empty($_GET['code']) && strlen($_GET['code'])==32)
	{
		if(check_email_token($myEmail, $_GET['code']))
		{
			updateNewEmail();
			header("Location: ".$site_url."user/administration");
			die();
		} else {
			$message = 5;
		}
	} else if(isset($_POST['email']))
	{
		// Validate reCAPTCHA
		if(isset($_POST['g-recaptcha-response']) && !empty($_POST['g-recaptcha-response'])) {
			$verifyResponse = @file_get_contents('https://www.google.com/recaptcha/api/siteverify?secret='.$secret_key.'&response='.$_POST['g-recaptcha-response']);
			if($verifyResponse !== false) {
				$responseData = json_decode($verifyResponse);
				if($responseData && $responseData->success) {
					$email = $_POST['email'];

					if(isValidEmail($email))
					{
						if(!$database->checkUserEmail($email))
						{
							$code = generateSocialID(32);
							update_email_token($_SESSION['id'], $code);
							update_new_email($_SESSION['id'], $email);
							$message = 4;
						} else $message = 1;

					} else $message = 2;
				} else {
					$message = 3;
				}
			} else {
				$message = 3;
			}
		} else {
			$message = 3;
		}
	}

?>