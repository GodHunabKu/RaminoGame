<?php
	// Load environment variables from .env file
	require_once(__DIR__ . '/include/functions/env.php');
	loadEnv(__DIR__ . '/.env');

	// Site url - add / at the end, eg: http://metin2cms.cf/mt2/ IMPORTANT!!!
	$site_url = env('SITE_URL', 'https://oneshyra.eu/');

	// Game database
	$host = env('DB_HOST', '81.180.203.241');
	$user = env('DB_USER', 'dev');
	$password = env('DB_PASSWORD', '41uGl9eDUJij');

	// Mail settings
	$SMTPAuth = filter_var(env('SMTP_AUTH', 'true'), FILTER_VALIDATE_BOOLEAN);
	$SMTPSecure = env('SMTP_SECURE', 'ssl');
	$EmailHost = env('EMAIL_HOST', 'mail.oneshyra.eu');
	$emailPort = (int)env('EMAIL_PORT', '465');

	$email_username = env('EMAIL_USERNAME', 'support@oneshyra.eu');
	$email_password = env('EMAIL_PASSWORD', 'Bigkebab95');

	// Register
	$safebox_size = (int)env('SAFEBOX_SIZE', '1');

	// reCAPTCHA keys
	$site_key = env('RECAPTCHA_SITE_KEY', '6LetYwgsAAAAAGzhZ9p8slnKhHaugkRmrFze6xBG');
	$secret_key = env('RECAPTCHA_SECRET_KEY', '6LetYwgsAAAAAFlmEnw9xuVU7q_a4al4IQsC-fKI');

	// Mt2cms version (keep for compatibility)
	$mt2cms = '2'; // hardcoded

	// Ranking auto-update (set to true when server is officially online)
	// Disabilitato durante sviluppo per evitare aggiornamenti automatici ogni 5 minuti
	$ranking_auto_update = false; // Cambia in true quando apri ufficialmente
?>
