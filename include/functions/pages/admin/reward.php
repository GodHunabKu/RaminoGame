<?php
	if(isset($_POST['add']))
	{
		if(isset($_POST['account']) && isset($_POST['name']) && isset($_POST['vnum']) && isset($_POST['count']))
		{
			// Validate and sanitize inputs
			$account_type = (int)$_POST['account'];
			$name = strip_tags($_POST['name']);
			$vnum = (int)$_POST['vnum'];
			$count = max(1, (int)$_POST['count']); // Minimum 1
			$socket0 = isset($_POST['socket0']) ? (int)$_POST['socket0'] : 0;
			$socket1 = isset($_POST['socket1']) ? (int)$_POST['socket1'] : 0;
			$socket2 = isset($_POST['socket2']) ? (int)$_POST['socket2'] : 0;

			if($account_type == 1)
				$account_id = getAccountIDbyName($name);
			else
				$account_id = getAccountIDbyChar($name);

			$added = 0;
			if($account_id)
			{
				add_item_award($account_id, $vnum, $count, $socket0, $socket1, $socket2);
				$added = 1;
			} else $added = 2;
		}
	} else if(isset($_POST['add2']) && isset($_POST['vnum']) && isset($_POST['count'])){
		// Validate inputs for mass reward
		$vnum = (int)$_POST['vnum'];
		$count = max(1, (int)$_POST['count']);
		$socket0 = isset($_POST['socket0']) ? (int)$_POST['socket0'] : 0;
		$socket1 = isset($_POST['socket1']) ? (int)$_POST['socket1'] : 0;
		$socket2 = isset($_POST['socket2']) ? (int)$_POST['socket2'] : 0;

		$online_players = getOnlinePlayers_minute(10);
		$added = 0;

		foreach($online_players as $player)
		{
			add_item_award($player['account_id'], $vnum, $count, $socket0, $socket1, $socket2);
			$added = 1;
		}
	}
?>