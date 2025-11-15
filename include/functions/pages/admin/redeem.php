<?php
	require_once("include/classes/admin-redeem-codes.php");
	$paginate = new paginate();
	
	if(isset($_POST['delete']) && isset($_POST['id']))
	{
		// Validate and sanitize ID
		$id = (int)$_POST['id'];
		if($id > 0)
		{
			delete_redeeem_code($id);
		}

		$location = '';
		if(isset($_GET["page_no"]) && is_numeric($_GET["page_no"]) && $_GET["page_no"]>1)
			$location = (int)$_GET["page_no"];
		else $location = 1;

		header("Location: ".$site_url."admin/redeem/".$location);
		die();
	}
?>