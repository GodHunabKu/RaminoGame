<?php
	$jsondataDownload = file_get_contents('include/db/download.json');
	$jsondataDownload = json_decode($jsondataDownload, true);
	
	if(!$jsondataDownload)
		$jsondataDownload = array();
	
	if(isset($_POST['submit']) && isset($_POST['download_server']) && isset($_POST['download_link']))
	{
		$new_link = array();
		$new_link['name'] = htmlspecialchars($_POST['download_server'], ENT_QUOTES, 'UTF-8');
		$new_link['link'] = filter_var($_POST['download_link'], FILTER_SANITIZE_URL);

		array_push($jsondataDownload, $new_link);

		$json_new = json_encode($jsondataDownload);
		file_put_contents('include/db/download.json', $json_new);

		header("Location: ".$site_url.'admin/download');
		die();
	} else if(isset($_GET['del']))
	{
		// Validate index is numeric and exists
		$del_index = (int)$_GET['del'];
		if(isset($jsondataDownload[$del_index]))
		{
			unset($jsondataDownload[$del_index]);

			$json_new = json_encode($jsondataDownload);
			file_put_contents('include/db/download.json', $json_new);
		}

		header("Location: ".$site_url.'admin/download');
		die();
	}
?>