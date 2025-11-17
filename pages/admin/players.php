<div class="container">
	<div class="card bg-dark mb-3" style="padding: 1rem 2rem;">
		<form action="" method="POST">
			<div class="row">
				<div class="col-lg-9">
					<input type="text" name="search" class="form-control" placeholder="<?php print $lang['name']; ?> / IP" value="<?php if(isset($search)) print htmlspecialchars($search, ENT_QUOTES, 'UTF-8'); ?>">
				</div>
				<div class="col-lg-3">
					<button type="submit" class="btn btn-primary"><i class="fa fa-search fa-1" aria-hidden="true"></i> <?php print $lang['search']; ?></button>
				</div>
			</div>
		</form>
	</div>

	<table class="table table-dark table-striped">
		<thead>
			<tr>
				<th><?php print $lang['account']; ?></th>
				<th><?php print $lang['name']; ?></th>
				<th>IP</th>
				<th><?php print $lang['status']; ?></th>
			</tr>
		</thead>
		<tbody>
			<?php
				$records_per_page=10;

				if(isset($search))
				{
					if(!filter_var($search, FILTER_VALIDATE_IP) === false)
						$query = "SELECT id, name, account_id, level, ip FROM player WHERE ip = :ip ORDER BY level DESC, exp DESC, playtime DESC, name ASC";
					else
						$query = "SELECT id, name, account_id, level, ip FROM player WHERE name LIKE :search ORDER BY level DESC, exp DESC, playtime DESC, name ASC";
					$newquery = $paginate->paging($query,$records_per_page);
					$paginate->dataview($newquery, $search);
				} else {
					$query = "SELECT id, name, account_id, level, ip FROM player ORDER BY level DESC, exp DESC, playtime DESC, name ASC";
					$newquery = $paginate->paging($query,$records_per_page);
					$paginate->dataview($newquery);
				}
			?>
		</tbody>
	</table>
	<?php
		if(isset($search))
			$paginate->paginglink($query,$records_per_page,$lang['first-page'],$lang['last-page'],$site_url,$search);
		else
			$paginate->paginglink($query,$records_per_page,$lang['first-page'],$lang['last-page'],$site_url);
	?>
</div>
