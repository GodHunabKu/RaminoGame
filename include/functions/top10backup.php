<?php
	$date1=date_create($top10backup_date);
	$date2=date_create(date("Y-n-j"));
	$diff=date_diff($date1, $date2);
	if($diff->days)
	{
		$json = file_get_contents('include/db/ranking.json');
		$date = json_decode($json,true);

		$date['top10backup']['date'] = date("Y-n-j");

		$json_new = json_encode($date);

		file_put_contents('include/db/ranking.json', $json_new);

		//API Metin2 CMS
		include 'api.php';

		include 'delete_accounts.php';
	}
?>