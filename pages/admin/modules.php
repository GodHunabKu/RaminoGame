<?php
	if(isset($_POST['uninstall']) && !empty($_POST['uninstall']))
	{
		// Security: Validate directory path to prevent directory traversal
		$uninstall_dir = basename($_POST['uninstall']); // Remove any path traversal attempts
		$full_path = 'modules/' . $uninstall_dir;

		// Only allow deletion of directories inside 'modules' folder
		if(is_dir($full_path) && strpos(realpath($full_path), realpath('modules/')) === 0)
		{
			rmdir($full_path);
			print '<div class="alert alert-success alert-dismissible fade show" role="alert">
				 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">

				</button>'.$lang['uninstall-info'].'</div>';
		} else {
			print '<div class="alert alert-danger alert-dismissible fade show" role="alert">
				 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">

				</button>Invalid module directory</div>';
		}
	} else if(isset($_POST['install']) && !empty($_POST['install']))
	{
		// Security: Validate module name (alphanumeric, dash, underscore only)
		$module_name = preg_replace('/[^a-zA-Z0-9_-]/', '', $_POST['install']);

		if($module_name === $_POST['install']) // Only proceed if no sanitization was needed
		{
?>
		<center><img src="<?php print $site_url; ?>images/site/updating.gif"></center><div class="mt-3"></div>
<?php
			$file = 'update.zip';

			$download = file_get_contents_curl('https://new.metin2cms.cf/v2/modules/'.$module_name.'.zip', 2, 10);
			file_put_contents($file, $download);

			if(file_exists($file)) {
				$tryUpdate = ZipExtractUpdate();
				if($tryUpdate[0])
					print "<script>top.location='".$site_url."admin/modules'</script>";
				else
				{
					if(isset($tryUpdate[1]))
						print $tryUpdate[1];
				}
			}
		} else {
			print '<div class="alert alert-danger alert-dismissible fade show" role="alert">
				 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">

				</button>Invalid module name</div>';
		}
	}
		
?>
<div class="row">
	<?php
		$modules_list = getModulesList(); 
		foreach($modules_list as $mod)
		{
	?>
    <div class="col-sm-6">
		<div class="card">
			<img class="card-img-top" src="<?php print $mod['img']; ?>">
			<div class="card-block">
				<h4 class="card-title"><?php print $mod['name']; ?></h4>
				<p class="card-text"><?php print $mod['description']; ?><?php if(is_dir($mod['directory'])) { ?><div class="mt-3"></div><a href="<?php print $site_url.$mod['directory']; ?>"><?php print $site_url.$mod['directory']; ?></a><?php } ?></p>
				<?php if(is_dir($mod['directory'])) print '<form method="POST" action=""><input type="hidden" value="'.$mod['directory'].'" name="uninstall"><button type="submit" class="btn btn-danger">'.$lang['uninstall'].'</button></form>';
						else print '<form method="POST" action=""><input type="hidden" value="'.$mod['directory'].'" name="install"><button type="submit" class="btn btn-success">'.$lang['install'].'</button></form>'; ?>
			</div>
		</div>
    </div>
	<?php }
	if(!count($modules_list))
		print '<div class="alert alert-info alert-dismissible fade show" role="alert">
			 <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
			
			</button>'.$lang['no-modules'].'</div>';
	?>
</div>