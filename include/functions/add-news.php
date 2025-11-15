<?php
		if(isset($_POST['title']) && isset($_POST['content']))
			if(!empty($_POST['title']) && !empty($_POST['content']))
				$paginate->add($_POST['title'], $_POST['content'], $_POST['category']);
			
		print '<form method="post" action="">';
		print '<p><a class="btn btn-danger" data-bs-toggle="collapse" href="#add" aria-expanded="false" aria-controls="add"><i class="fa fa-plus fa-2" aria-hidden="true"></i> '.$lang['new-article'].'</a></p>';
		print '<div class="collapse" id="add"><div class="card card-block">';
		print '<p>'.$lang['title'].':</p>';
		print '<input name="title" type="text" class="form-control -webkit-transition" placeholder="'.$lang['title'].'" required>';
		print '<p>Categorie:</p>';
?>
		<select class="form-control" name="category">
			<option value="1" selected="selected">Updates</option>
			<option value="2">Events</option>
			<option value="0">Other</option>
		</select>
<?php
		print '<p>'.$lang['content'].':</p>';
		print '<textarea class="ckeditor" name="content"></textarea>';
		print '</br><input type="submit" class="btn-big btn-success btn-sm btn" value="'.$lang['new-article'].'">';
		print '</div></div>';
		print '</form>';
		print '<hr>';
?>