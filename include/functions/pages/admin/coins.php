<?php
	if(isset($_POST['account']) && isset($_POST['name']) && isset($_POST['coins']) && isset($_POST['type']))
	{
		// Validate and sanitize inputs
		$account_type = (int)$_POST['account'];
		$coins = (int)$_POST['coins'];
		$coin_type = (int)$_POST['type'];
		$name = strip_tags($_POST['name']);

		// Validate coins amount (must be positive)
		if($coins <= 0) {
			$added = 3; // Invalid amount
		} else {
			if($account_type == 1)
				$account_id = getAccountIDbyName($name);
			else
				$account_id = getAccountIDbyChar($name);

			$added = 0;
			if($account_id)
			{
				if($coin_type == 1)
					addCoins($account_id, $coins);
				else
					addjCoins($account_id, $coins);
				$added = 1;
			} else $added = 2;
		}
	}
?>