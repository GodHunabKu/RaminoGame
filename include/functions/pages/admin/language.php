<?php
	if(isset($_POST['default-language']))
	{
		$edited = false;
		
		if(isset($json_languages['languages'][$_POST['default-language']]) && $_POST['default-language'] != $json_languages['settings']['default'])
		{
			$json_languages['settings']['default'] = $_POST['default-language'];
			$edited = true;
		}
		
		if($edited)
		{
			$json_new = json_encode($json_languages);
			file_put_contents('include/db/languages.json', $json_new);
		}
		
		header("Location: ".$site_url.'admin/language');
		die();
	} else if(isset($_POST['delete']))
	{
		$edited = false;
		// Sanitize filename to prevent path traversal
		$lang_code = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['delete']);

		if(isset($json_languages['languages'][$lang_code]) && $lang_code != $json_languages['settings']['default'])
		{
			$lang_file = 'include/languages/' . $lang_code . '.php';
			// Double check the file exists and is in the correct directory
			if(file_exists($lang_file) && realpath($lang_file) === realpath(dirname(__FILE__) . '/../../../languages/' . $lang_code . '.php'))
			{
				unset($json_languages['languages'][$lang_code]);
				unlink($lang_file);
				$edited = true;
			}
		}
		
		if($edited)
		{
			$json_new = json_encode($json_languages);
			file_put_contents('include/db/languages.json', $json_new);
		}
		
		header("Location: ".$site_url.'admin/language');
		die();
	} else if(isset($_POST['install']) && isset($_POST['name']))
	{
		$edited = false;
		// Sanitize language code
		$lang_code = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['install']);
		$file = 'update.zip';
		$download = file_get_contents_curl('https://new.metin2cms.cf/v2/languages/' . $lang_code . '.zip', 2, 10);
		file_put_contents($file, $download);

		if(file_exists($file)) {
			$tryUpdate = ZipExtractUpdate();
			if($tryUpdate[0])
			{
				if(!isset($json_languages['languages'][$lang_code]))
				{
					$json_languages['languages'][$lang_code] = htmlspecialchars($_POST['name'], ENT_QUOTES, 'UTF-8');
					$edited = true;
				}
				
				if($edited)
				{
					$json_new = json_encode($json_languages);
					file_put_contents('include/db/languages.json', $json_new);
				}
			}
		}
		
		header("Location: ".$site_url.'admin/language');
		die();
	}
?>