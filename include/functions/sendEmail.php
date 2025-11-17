<?php
	require 'include/mailer/PHPMailer.php';
	require 'include/mailer/SMTP.php';
	require 'include/mailer/Exception.php';
	use PHPMailer\PHPMailer\PHPMailer;

	$mail             = new PHPMailer();

	// Use sendmail instead of SMTP (works on shared hosting without firewall issues)
	$mail->isSendmail();

	$mail->CharSet    = 'UTF-8';					// for special chars

	$mail->SetFrom($email_username, $site_title);
	$mail->AddReplyTo($email_username, $site_title);

	$mail->Subject    = $subject;

	$mail->AltBody    = $alt_message;

	$mail->MsgHTML($html_mail);

	$mail->AddAddress($sendEmail, $sendName);

	if(!$mail->Send()) {
		print '<div class="alert alert-danger alert-dismissible fade show" role="alert">
			<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
			
			</button>Please contact an administrator!</br>'.$mail->ErrorInfo.'</div>';
	}
