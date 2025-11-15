<?php
	if(isset($_POST['submit']))
	{
		$edited = false;

		foreach($_POST as $key=>$link)
		{
			// Skip submit button
			if($key === 'submit') continue;

			// Sanitize link value
			$sanitized_link = filter_var($link, FILTER_SANITIZE_URL);

			if(isset($jsondata['general'][$key]))
			{
				if($jsondata['general'][$key] != $sanitized_link)
				{
					$jsondata['general'][$key] = $sanitized_link;
					$edited = true;
				}
			}
			else if(isset($jsondata['links'][$key]))
			{
				if($jsondata['links'][$key] != $sanitized_link)
				{
					$jsondata['links'][$key] = $sanitized_link;
					$edited = true;
				}
			}
			else if(isset($jsondata['social-links'][$key]))
			{
				if($jsondata['social-links'][$key] != $sanitized_link)
				{
					$jsondata['social-links'][$key] = $sanitized_link;
					$edited = true;
				}
			}
		}
		if($edited)
		{
			$json_new = json_encode($jsondata);
			file_put_contents('include/db/settings.json', $json_new);
		}
		header("Location: ".$site_url.'admin/links');
		die();
	}
?>