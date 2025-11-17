<?php
	// Reindirizzamento POST
	if(isset($_POST['search']) && strlen($_POST['search'])>=3)
	{
		header("Location: ".$site_url."ranking/guilds/1/".$_POST['search']);
		die();
	} else if(isset($_POST['search']) && $_POST['search']=='')
	{
		header("Location: ".$site_url."ranking/guilds/1");
		die();
	}
	
	// Estrazione della variabile di ricerca (player_name dal router .htaccess)
	$search = null;
	if(isset($_GET['player_name']))
	{
		$new_search = strip_tags($_GET['player_name']);
		if(strlen($new_search)>=3)
			$search = $new_search;
	}

	// *****************************************************************
	// SOLUZIONE BUG PAGINAZIONE: Assicurati che $_GET["page_no"] sia settato
	// Se il router non lo setta quando l'URL è /ranking/guilds, imposta a 1
	if (!isset($_GET['page_no'])) {
	    $_GET['page_no'] = 1;
	}
	// *****************************************************************
	
	require_once("include/classes/guilds.php");
	$paginate = new paginate();
?>