<?php
	$jsondataReferrals = file_get_contents('include/db/referrals.json');
	$jsondataReferrals = json_decode($jsondataReferrals, true);
	
	if(isset($_POST['submit']))
	{
		$edited = false;

		if(isset($_POST['status']))
		{
			$status = filter_var($_POST['status'], FILTER_VALIDATE_BOOLEAN, FILTER_NULL_ON_FAILURE);
			if($status !== null && $jsondataFunctions['active-referrals'] != $status)
			{
				$jsondataFunctions['active-referrals'] = $status;

				$json_new = json_encode($jsondataFunctions);
				file_put_contents('include/db/functions.json', $json_new);
			}
		}

		foreach($_POST as $key=>$value)
		{
			// Skip submit button
			if($key === 'submit' || $key === 'status') continue;

			if(isset($jsondataReferrals[$key]))
			{
				// Sanitize value (assume numeric for referral values)
				$sanitized_value = is_numeric($value) ? (int)$value : htmlspecialchars($value, ENT_QUOTES, 'UTF-8');

				if($jsondataReferrals[$key] != $sanitized_value)
				{
					$jsondataReferrals[$key] = $sanitized_value;
					$edited = true;
				}
			}
		}
		
		if($edited)
		{
			$json_new = json_encode($jsondataReferrals);
			file_put_contents('include/db/referrals.json', $json_new);
		}
		
		header("Location: ".$site_url.'admin/referrals');
		die();
	}
?>