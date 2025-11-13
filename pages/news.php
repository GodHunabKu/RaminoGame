  <div class="xy-news-header">
    <div class="left">
      <h3 class="mb-0"><?php print $lang['news']; ?></h3>
    </div>
    <div class="right">
      <ul class="xy-nh-ul">
		<?php
			$cat = 0;
			if(isset($_GET['category']) && (int)$_GET['category']>0 && (int)$_GET['category']<=2)
				$cat = $_GET['category'];
			$categories = array("All news", "Updates", "Events");
			
			foreach($categories as $key=>$value)
				if($key==$cat)
					print '<li><a href="'.$site_url.'news/'.$key.'/1" class="active">'.$value.'</a></li>';
				else
					print '<li><a href="'.$site_url.'news/'.$key.'/1">'.$value.'</a></li>';
		?>
      </ul>
    </div>
  </div>

	<?php 
		if($offline) print '</br><h2 class="pre-social"><strong><font color="red">'.$lang['server-offline'].'</font></strong></h2>';
		if(!$offline && $database->is_loggedin())
			if($web_admin>=$jsondataPrivileges['news'])
				include 'include/functions/add-news.php';

		if (version_compare($php_version = phpversion(), '5.6.0', '<')) {
	?>
	<div class="alert alert-danger alert-dismissible fade show" role="alert">
		<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
			
		</button>
		<span>Metin2CMS works with a PHP version >= 5.6.0. At this time, the server is running version <?php print $php_version; ?>.</span>
	</div>
	<?php
		}
		$query = "SELECT * FROM news ORDER BY id DESC";
		if($cat)
			$query = "SELECT * FROM news WHERE category = ".$cat." ORDER BY id DESC";
		$records_per_page=intval(getJsonSettings("news"));
		
		$newquery = $paginate->paging($query,$records_per_page);
		$paginate->dataview($newquery, $lang['sure?'], $web_admin, $jsondataPrivileges['news'], $site_url, $lang['read-more']);

		$paginate->paginglink($query,$records_per_page,$lang['first-page'],$lang['last-page'],$site_url,$cat);
	?>