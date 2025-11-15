<?php
	$jsondataDonate = file_get_contents('include/db/donate.json');
	$jsondataDonate = json_decode($jsondataDonate, true);
	
	$jsondataCurrency = file_get_contents('include/db/currency.json');
	$jsondataCurrency = json_decode($jsondataCurrency,true);
	
	if(!$jsondataDonate)
		$jsondataDonate = array();
	
	if(isset($_POST['submit']) && isset($_POST['donation_method']))
	{
		$new_link = array();
		$new_link['name'] = htmlspecialchars($_POST['donation_method'], ENT_QUOTES, 'UTF-8');
		$new_link['list'] = array();

		array_push($jsondataDonate, $new_link);

		$json_new = json_encode($jsondataDonate);
		file_put_contents('include/db/donate.json', $json_new);

		header("Location: ".$site_url.'admin/donate');
		die();
	} else if(isset($_GET['del']))
	{
		// Validate index is numeric and exists
		$del_index = (int)$_GET['del'];
		if(isset($jsondataDonate[$del_index]))
		{
			unset($jsondataDonate[$del_index]);

			$json_new = json_encode($jsondataDonate);
			file_put_contents('include/db/donate.json', $json_new);
		}

		header("Location: ".$site_url.'admin/donate');
		die();
	}  else if(isset($_POST['submit_delete_price']) && isset($_POST['id']) && isset($_POST['price_id']))
	{
		$id = (int)$_POST['id'];
		$price_id = (int)$_POST['price_id'];

		if(isset($jsondataDonate[$id]['list'][$price_id]))
		{
			unset($jsondataDonate[$id]['list'][$price_id]);

			$json_new = json_encode($jsondataDonate);
			file_put_contents('include/db/donate.json', $json_new);
		}

		header("Location: ".$site_url.'admin/donate');
		die();
	} else if(isset($_POST['submit_price']) && isset($_POST['id']) && isset($_POST['price']) && isset($_POST['md']) && isset($_POST['currency']))
	{
		$id = (int)$_POST['id'];

		if(isset($jsondataDonate[$id]))
		{
			$new_price = array();
			$new_price['price'] = floatval($_POST['price']);
			$new_price['md'] = (int)$_POST['md'];
			$new_price['currency'] = htmlspecialchars($_POST['currency'], ENT_QUOTES, 'UTF-8');

			array_push($jsondataDonate[$id]['list'], $new_price);

			$json_new = json_encode($jsondataDonate);
			file_put_contents('include/db/donate.json', $json_new);
		}

		header("Location: ".$site_url.'admin/donate');
		die();
	}
?>