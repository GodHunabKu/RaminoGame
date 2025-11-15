<?php
	session_start();
	
	header('Cache-control: private');
	
	$current_page = isset($_GET['p']) ? $_GET['p'] : null;
	
	include 'config.php';
	
	if (substr($site_url, -1)!='/')
		$site_url.='/';
	
	$site_domain = $_SERVER['HTTP_HOST'];
	
	include 'include/functions/version.php';
	
	include 'include/functions/language.php';
	
	require_once("include/classes/user.php");
	
	$jsondata = file_get_contents('include/db/settings.json');
	$jsondata = json_decode($jsondata,true);
	$jsondataRanking = file_get_contents('include/db/ranking.json');
	$jsondataRanking = json_decode($jsondataRanking,true);
	$loadedStats = file_get_contents('include/db/stats.json');
	$loaded_stats = json_decode($loadedStats,true);
	$jsondataFunctions = file_get_contents('include/db/functions.json');
	$jsondataFunctions = json_decode($jsondataFunctions, true);
	include 'include/functions/json.php';
	$site_title = getJsonSettings("title");
	$paypal_email = getJsonSettings("paypal");
	$forum=getJsonSettings("forum", "links");
	$support=getJsonSettings("support", "links");
	$item_shop=getJsonSettings("item-shop", "links");
	if($item_shop!="")
		$shop_url = $item_shop;
	else if(is_dir('shop')) 
		$shop_url = $site_url.'shop'; 
	else $shop_url = '';
	$top10backup_date=getJsonSettings("date", "top10backup");
	
	include 'include/functions/social-links.php';
	$social_links=getJsonSettings("", "social-links");

	$offline = 0;
	
	$database = new USER($host, $user, $password);
	
	include 'include/functions/pages.php';
	
	$jsondataPrivileges['news']=9;

	if(!$offline)
	{
		include 'include/functions/basic.php';
		
		if($database->is_loggedin())
		{
			if(($_SESSION['fingerprint']!=md5($_SERVER['HTTP_USER_AGENT'].'x'.$_SERVER['REMOTE_ADDR'])) || ($_SESSION['password']!=securityPassword(getAccountPassword($_SESSION['id']))) || !checkStatus($_SESSION['id']))
			{
				$database->doLogout();
				header("Location: ".$site_url);
				die();
			}
			$web_admin = web_admin_level();
		} else $web_admin = 0;

		if($web_admin)
		{
			$jsondataPrivileges = file_get_contents('include/db/privileges.json');
			$jsondataPrivileges = json_decode($jsondataPrivileges,true);
		}
		
		if($database->is_loggedin() && $web_admin>=$jsondataPrivileges['news'])
		{
			$delete = isset($_GET['delete']) ? $_GET['delete'] : null;
			if(is_numeric($delete))
			{
				$paginate->delete_article($delete);
				header("Location: ".$site_url);
				die();
			}
		}
		
		$statistics = false;
		foreach($jsondataFunctions as $key => $status)
			if($key != 'active-registrations' && $key != 'players-debug' && $key != 'active-referrals' && $status)
			{
				$statistics = true;
				break;
			}
		
		if($current_page=="logout")
		{
			$database->doLogout();
			header("Location: ".$site_url);
			die();
		}
		
		include 'include/functions/functions.php';

		if($page=='admin')
		{
			$admin_page = isset($_GET['a']) ? $_GET['a'] : null;
			include 'include/functions/admin-pages.php';

			checkPrivileges($a_page, $web_admin);

			include 'include/functions/admin-functions.php';
		}

		$last_modified_time_ranking = filemtime('include/db/ranking.json');
		if ((time() - $last_modified_time_ranking) > 5 * 60) {
			$top = topPlayers(5);
			if(count($top))
				$top[0]['guild_name'] = get_player_guild($top[0]['id']);
			foreach($top as &$player)
				$player['empire'] = get_player_empire($player['account_id']);
			$jsondataRanking['top10backup']['players'] = $top;

			$top = topGuilds(5);
			if(count($top)) {
				$data = getPlayerNameAndJob($top[0]['master']);
				$top[0]['master_name'] = $data['name'];
				$top[0]['master_job'] = $data['job'];
			}
			foreach($top as &$guild)
				$guild['empire'] = get_player_empire(getAccountID($row['master']));
			$jsondataRanking['top10backup']['guilds'] = $top;

			file_put_contents('include/db/ranking.json', json_encode($jsondataRanking));
		}

		$last_modified_time_stats = filemtime('include/db/stats.json');
		if ((time() - $last_modified_time_stats) > 30) {
			$loaded_stats = array_reduce(array_keys($jsondataFunctions), function($carry, $key) use ($jsondataFunctions) {
				$status = $jsondataFunctions[$key];
				$carry[$key] = ($key != 'active-registrations' && $key != 'players-debug' && $key != 'active-referrals' && $status) ? getStatistics($key) : 0;
				return $carry;
			}, []);

			file_put_contents('include/db/stats.json', json_encode($loaded_stats));
			$last_modified_time_stats = time() + 1;
		}
		//work
		include 'include/functions/top10backup.php';
	}
	else
	{
		$web_admin = 0;
		if($page!='news' && $page!='read')
		{
			header("Location: ".$site_url);
			die();
		}
		$offline_date=date_format(date_create($top10backup_date), 'd.m.Y');
		$offline_players=getJsonSettings("players", "top10backup");
		$offline_guilds=getJsonSettings("guilds", "top10backup");
	}

	if(isset($_GET['api']) && isset($_GET['key']) && $_GET['api']=='metin2cms')
	{
		$apidata = file_get_contents('include/db/api.json');
		$apidata = json_decode($apidata,true);
		
		if($_GET['key']==$apidata['key'])
			die('ok');
		else
			die();
	}