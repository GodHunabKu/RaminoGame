<?php
	if(isset($_POST['username']) && isset($_POST['password']))
	{
		$username = strip_tags($_POST['username']);
		$password = strip_tags($_POST['password']);
		
		$login_info = $database->doLogin($username,$password);
		// Security: Regenerate session ID to prevent session fixation attacks
		if(isset($login_info[0]) && $login_info[0] == 1) {
			session_regenerate_id(true);
		}
	}
?>