<div class="container">
	<div class="page-hd">
		<div class="bd-c">
			<h2 class="pre-social"><?php print $lang['redeem-codes']; ?></h2>
		</div>
	</div>
	<div class="padding-container">
		<?php if($received>=0) { ?>
		<div class="alert alert-<?php if(!$received || $received==4) print 'danger'; else print 'success'; ?> alert-dismissible fade show" role="alert">
			<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
				
			</button>
			<?php
				if(!$received)
					print $lang['incorrect-redeem'];
				else if($received==1 || $received==2)
				{
					print $lang['collected_md'].' '.$coins.' '; 
					if($received==1)
						print $lang['md'].' (MD)';
					else print $lang['jd'].' (JD)';
					print '.';
				} else if($received==3)
					print $lang['successfully_added'];
				else
					print $lang['no_space'];
			?>
		</div>
		<?php } ?>
			
		<form action="" method="POST">
			<div class="input-group">
				<input type="text" class="form-control form-control-lg" style="margin-top: 12px;" value="" name="code" required>
				<span class="input-group-btn">
					<button class="btn btn-danger btn-lg" type="submit" data-placement="button" style="margin-top: 15px;">
						<i class="fa fa-check" aria-hidden="true"></i> <?php print $lang['redeem-my-code']; ?>
					</button>
				</span>
			</div>
		</form>
	</div>
</div>