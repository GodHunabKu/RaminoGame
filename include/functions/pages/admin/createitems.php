<?php
	$jsonBonuses = file_get_contents('include/db/bonuses.json');
	$jsonBonuses = json_decode($jsonBonuses,true);
	
	$form_bonuses = '';
	foreach($jsonBonuses as $bonus)
		$form_bonuses .= '<option value='.intval($bonus['id']).'>'.htmlspecialchars(str_replace("[n]", 'XXX', $bonus[$language_code]), ENT_QUOTES, 'UTF-8').'</option>';
?>