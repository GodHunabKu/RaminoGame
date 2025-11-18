<?php
/**
 * Test DEBUG per Password Magazzino
 * Replica esattamente il flusso del pulsante reale
 */

session_start();

// Se non sei loggato, simula un login (SOLO PER TEST - da rimuovere dopo)
if(!isset($_SESSION['id'])) {
    echo '<h1>⚠️ Devi essere loggato per testare</h1>';
    echo '<p>Fai login normalmente, poi torna su questa pagina</p>';
    exit;
}

// Load environment and config
require_once(__DIR__ . '/include/functions/env.php');
loadEnv(__DIR__ . '/.env');
require_once(__DIR__ . '/config.php');
require_once(__DIR__ . '/include/functions/basic.php');
require_once(__DIR__ . '/include/functions/header.php');

// Recupera dati account
$account_name = getAccountName($_SESSION['id']);
$myEmail = getAccountEmail($_SESSION['id']);

?>
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DEBUG Password Magazzino</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        h1 { color: #333; }
        .step {
            background: #e7f3ff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #007bff;
        }
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
        .debug {
            background: #f9f9f9;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            white-space: pre-wrap;
        }
        button {
            background: #007bff;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔍 DEBUG Password Magazzino</h1>

        <div class="step">
            <strong>✅ Account loggato:</strong><br>
            Username: <?php echo htmlspecialchars($account_name); ?><br>
            Email: <?php echo htmlspecialchars($myEmail); ?><br>
            Session ID: <?php echo $_SESSION['id']; ?>
        </div>

        <?php if(isset($_POST['test_magazzino'])): ?>

            <h2>📤 Esecuzione Test...</h2>

            <?php
            // STEP 1: Recupera password safebox
            echo '<div class="step">';
            echo '<strong>STEP 1:</strong> Recupero password safebox...<br>';
            $code = getPlayerSafeBoxPassword($_SESSION['id']);

            if($code && $code != '' && $code != '000000') {
                echo '✅ Password trovata: ' . htmlspecialchars($code);
                echo '</div>';

                // STEP 2: Prepara variabili email
                echo '<div class="step">';
                echo '<strong>STEP 2:</strong> Preparazione variabili email...<br>';
                $alt_message = 'Password Magazzino';
                $subject = 'Password Magazzino';
                $sendName = $account_name;
                $sendEmail = $myEmail;

                echo '✅ Subject: ' . htmlspecialchars($subject) . '<br>';
                echo '✅ To: ' . htmlspecialchars($sendEmail) . '<br>';
                echo '✅ Name: ' . htmlspecialchars($sendName);
                echo '</div>';

                // STEP 3: Genera HTML email
                echo '<div class="step">';
                echo '<strong>STEP 3:</strong> Generazione HTML email...<br>';
                $html_mail = sendCode($account_name, $code, 2);
                echo '✅ HTML generato (lunghezza: ' . strlen($html_mail) . ' caratteri)';
                echo '</div>';

                // STEP 4: Invio email con DEBUGGING
                echo '<div class="step">';
                echo '<strong>STEP 4:</strong> Invio email con sendmail...<br>';

                require 'include/mailer/PHPMailer.php';
                require 'include/mailer/SMTP.php';
                require 'include/mailer/Exception.php';
                use PHPMailer\PHPMailer\PHPMailer;

                $mail = new PHPMailer();

                // USA SENDMAIL (come nel file modificato)
                $mail->isSendmail();
                $mail->CharSet = 'UTF-8';

                // Debug completo
                $mail->SMTPDebug = 0;
                $mail->Debugoutput = function($str, $level) {
                    echo '<div class="debug">📝 [Level ' . $level . '] ' . htmlspecialchars($str) . '</div>';
                };

                $mail->SetFrom($email_username, $site_title);
                $mail->AddReplyTo($email_username, $site_title);
                $mail->Subject = $subject;
                $mail->AltBody = $alt_message;
                $mail->MsgHTML($html_mail);
                $mail->AddAddress($sendEmail, $sendName);

                echo '📧 Tentativo invio...<br>';

                if($mail->Send()) {
                    echo '</div>';
                    echo '<div class="success">';
                    echo '<h3>✅ EMAIL INVIATA CON SUCCESSO!</h3>';
                    echo '<p><strong>Destinatario:</strong> ' . htmlspecialchars($sendEmail) . '</p>';
                    echo '<p><strong>Password Magazzino:</strong> ' . htmlspecialchars($code) . '</p>';
                    echo '<p><strong>⚠️ CONTROLLA:</strong></p>';
                    echo '<ul>';
                    echo '<li>Inbox di ' . htmlspecialchars($sendEmail) . '</li>';
                    echo '<li><strong>SPAM/JUNK folder</strong> (molto probabile!)</li>';
                    echo '<li>Posta indesiderata</li>';
                    echo '</ul>';
                    echo '<p><strong>💡 Nota:</strong> Le email da sendmail spesso finiscono in SPAM la prima volta. Cerca "Password Magazzino" o "' . htmlspecialchars($site_title) . '"</p>';
                    echo '</div>';
                } else {
                    echo '</div>';
                    echo '<div class="error">';
                    echo '<h3>❌ ERRORE INVIO EMAIL</h3>';
                    echo '<p><strong>Dettagli errore:</strong></p>';
                    echo '<p>' . htmlspecialchars($mail->ErrorInfo) . '</p>';
                    echo '<p><strong>Possibili cause:</strong></p>';
                    echo '<ul>';
                    echo '<li>Sendmail non configurato correttamente sul server</li>';
                    echo '<li>Email mittente non valida</li>';
                    echo '<li>Server mail locale disabilitato</li>';
                    echo '</ul>';
                    echo '</div>';
                }

            } else {
                echo '❌ Password safebox non trovata o = 000000<br>';
                echo 'Valore ricevuto: ' . var_export($code, true);
                echo '</div>';

                echo '<div class="warning">';
                echo '<h3>⚠️ Password Magazzino Non Configurata</h3>';
                echo '<p>Devi prima impostare una password per il magazzino nel gioco.</p>';
                echo '<p>Crea un personaggio e imposta la password del magazzino in-game.</p>';
                echo '</div>';
            }
            ?>

        <?php else: ?>

            <div class="warning">
                <p><strong>ℹ️ Informazioni:</strong></p>
                <p>Questo test replica <strong>esattamente</strong> il flusso del pulsante "Richiedi Password Magazzino" nella pagina amministrazione.</p>
                <p>Ti mostrerà:</p>
                <ul>
                    <li>✅ Se la password del magazzino esiste</li>
                    <li>✅ Se l'HTML email viene generato</li>
                    <li>✅ Se l'email viene inviata con successo</li>
                    <li>❌ Eventuali errori dettagliati</li>
                </ul>
            </div>

            <form method="post">
                <button type="submit" name="test_magazzino">🧪 Testa Invio Password Magazzino</button>
            </form>

        <?php endif; ?>
    </div>
</body>
</html>
