<?php
/**
 * Script di test per verificare invio email
 * Accedi a: http://tuosito.it/test_email.php
 */

// Load environment and config
require_once(__DIR__ . '/include/functions/env.php');
loadEnv(__DIR__ . '/.env');
require_once(__DIR__ . '/config.php');

// Imposta email di test (MODIFICA CON LA TUA EMAIL!)
$test_email = 'tua-email@example.com'; // <-- CAMBIA QUESTA EMAIL

echo '<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Invio Email</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .config {
            background: #f9f9f9;
            padding: 15px;
            border-left: 4px solid #007bff;
            margin: 20px 0;
        }
        .config p { margin: 5px 0; }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
        }
        .warning {
            background: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }
        button {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        button:hover { background: #0056b3; }
        .debug {
            background: #e7f3ff;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🧪 Test Invio Email - RaminoGame</h1>';

// Mostra configurazione attuale
echo '<div class="config">
        <h3>📋 Configurazione Email Attuale:</h3>
        <p><strong>Host:</strong> ' . htmlspecialchars($EmailHost) . '</p>
        <p><strong>Porta:</strong> ' . $emailPort . '</p>
        <p><strong>Username:</strong> ' . htmlspecialchars($email_username) . '</p>
        <p><strong>Password:</strong> ' . (empty($email_password) ? '❌ NON CONFIGURATA' : '✅ Configurata (' . str_repeat('*', strlen($email_password)) . ')') . '</p>
        <p><strong>SMTP Auth:</strong> ' . ($SMTPAuth ? '✅ Abilitato' : '❌ Disabilitato') . '</p>
        <p><strong>SMTP Secure:</strong> ' . htmlspecialchars($SMTPSecure) . '</p>
      </div>';

// Test invio email
if(isset($_POST['send_test'])) {
    echo '<h2>📤 Invio Email di Test...</h2>';

    require 'include/mailer/PHPMailer.php';
    require 'include/mailer/SMTP.php';
    require 'include/mailer/Exception.php';
    use PHPMailer\PHPMailer\PHPMailer;

    $mail = new PHPMailer();
    $mail->IsSMTP();
    $mail->SMTPDebug = 2; // ATTIVA DEBUG COMPLETO
    $mail->Debugoutput = function($str, $level) {
        echo '<div class="debug">📝 [Level ' . $level . '] ' . htmlspecialchars($str) . '</div>';
    };

    $mail->Timeout = 30;
    $mail->CharSet = 'UTF-8';
    $mail->SMTPAuth = $SMTPAuth;
    $mail->SMTPSecure = $SMTPSecure;
    $mail->Host = $EmailHost;
    $mail->Port = $emailPort;
    $mail->Username = $email_username;
    $mail->Password = $email_password;

    $mail->SetFrom($email_username, 'RaminoGame Test');
    $mail->AddReplyTo($email_username, 'RaminoGame Test');

    $mail->Subject = '🧪 Test Email - ' . date('Y-m-d H:i:s');
    $mail->AltBody = 'Questa è un\'email di test da RaminoGame';

    $html_content = '
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
            .container { background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }
            h1 { color: #007bff; }
            .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>✅ Test Email Funzionante!</h1>
            <p>Questa è un\'email di test dal sistema RaminoGame.</p>
            <div class="info">
                <p><strong>Inviata il:</strong> ' . date('d/m/Y H:i:s') . '</p>
                <p><strong>Server:</strong> ' . $EmailHost . ':' . $emailPort . '</p>
                <p><strong>Da:</strong> ' . $email_username . '</p>
            </div>
            <p>Se vedi questa email, significa che la configurazione SMTP è corretta! 🎉</p>
        </div>
    </body>
    </html>';

    $mail->MsgHTML($html_content);
    $mail->AddAddress($test_email, 'Test User');

    echo '<h3>🚀 Tentativo di invio a: ' . htmlspecialchars($test_email) . '</h3>';

    if($mail->Send()) {
        echo '<div class="success">
                <h3>✅ EMAIL INVIATA CON SUCCESSO!</h3>
                <p>Controlla la tua casella email (anche lo spam): <strong>' . htmlspecialchars($test_email) . '</strong></p>
                <p>Se l\'email è arrivata, significa che anche le funzioni di reset password e password magazzino stanno funzionando correttamente!</p>
              </div>';
    } else {
        echo '<div class="error">
                <h3>❌ ERRORE NELL\'INVIO EMAIL</h3>
                <p><strong>Dettagli errore:</strong></p>
                <p>' . htmlspecialchars($mail->ErrorInfo) . '</p>
                <p><strong>Possibili soluzioni:</strong></p>
                <ul>
                    <li>Verifica che le credenziali email siano corrette</li>
                    <li>Controlla che l\'host SMTP sia raggiungibile</li>
                    <li>Verifica che la porta ' . $emailPort . ' sia aperta</li>
                    <li>Controlla se il firewall blocca le connessioni SMTP</li>
                    <li>Verifica che l\'account email permetta l\'accesso SMTP</li>
                </ul>
              </div>';
    }

} else {
    // Form di test
    echo '<div class="warning">
            <p><strong>⚠️ IMPORTANTE:</strong> Prima di eseguire il test, modifica la variabile <code>$test_email</code> all\'inizio di questo file con il tuo indirizzo email!</p>
            <p>Email di test attuale: <strong>' . htmlspecialchars($test_email) . '</strong></p>
          </div>';

    echo '<form method="post">
            <p>Questo script invierà un\'email di test per verificare che la configurazione SMTP sia corretta.</p>
            <p>Verrà attivato il debug completo (SMTPDebug = 2) per vedere tutti i dettagli della connessione.</p>
            <button type="submit" name="send_test">📧 Invia Email di Test</button>
          </form>';
}

echo '  </div>
</body>
</html>';
?>
