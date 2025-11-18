<?php
/**
 * Test invio email con sendmail() invece di SMTP
 * Questo metodo funziona sempre su hosting condivisi
 */

// Load environment and config
require_once(__DIR__ . '/include/functions/env.php');
loadEnv(__DIR__ . '/.env');
require_once(__DIR__ . '/config.php');

// Load PHPMailer classes
require 'include/mailer/PHPMailer.php';
require 'include/mailer/SMTP.php';
require 'include/mailer/Exception.php';
use PHPMailer\PHPMailer\PHPMailer;

// Email di test - MODIFICA QUI
$test_email = 'metalrambo95@hotmail.it';

?>
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Sendmail - RaminoGame</title>
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
        .info {
            background: #e7f3ff;
            padding: 15px;
            border-left: 4px solid #007bff;
            margin: 20px 0;
        }
        .success {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            margin: 20px 0;
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #dc3545;
            margin: 20px 0;
        }
        .debug {
            background: #f9f9f9;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            font-family: monospace;
            font-size: 12px;
            border-left: 3px solid #6c757d;
        }
        button {
            background: #28a745;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 20px;
        }
        button:hover { background: #218838; }
        .comparison {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }
        .method {
            padding: 15px;
            border-radius: 5px;
            border: 2px solid #ddd;
        }
        .method.active {
            border-color: #28a745;
            background: #d4edda;
        }
        .method h3 { margin-top: 0; }
    </style>
</head>
<body>
    <div class="card">
        <h1>📧 Test Sendmail vs SMTP</h1>

        <div class="comparison">
            <div class="method">
                <h3>❌ SMTP (Attuale)</h3>
                <ul>
                    <li>Usa connessione esterna</li>
                    <li>Porta 465/587 spesso bloccata</li>
                    <li>Timeout connessione</li>
                    <li><strong>NON FUNZIONA</strong></li>
                </ul>
            </div>
            <div class="method active">
                <h3>✅ Sendmail (Nuovo)</h3>
                <ul>
                    <li>Usa server mail locale</li>
                    <li>Nessuna porta da aprire</li>
                    <li>Veloce e diretto</li>
                    <li><strong>SEMPRE FUNZIONA</strong></li>
                </ul>
            </div>
        </div>

        <div class="info">
            <h3>🔧 Configurazione Test:</h3>
            <p><strong>Metodo:</strong> Sendmail (PHP mail locale)</p>
            <p><strong>Da:</strong> <?php echo htmlspecialchars($email_username); ?></p>
            <p><strong>A:</strong> <?php echo htmlspecialchars($test_email); ?></p>
            <p><strong>Server:</strong> localhost (sendmail interno)</p>
        </div>

        <?php if(isset($_POST['send_test'])): ?>
            <h2>📤 Test Invio con Sendmail...</h2>

            <?php
            $mail = new PHPMailer();

            // ===================================
            // USA SENDMAIL INVECE DI SMTP
            // ===================================
            $mail->isSendmail(); // <-- QUESTO È IL CAMBIAMENTO CHIAVE!

            // Configura debug
            $mail->SMTPDebug = 0; // Disattivato per sendmail
            $mail->CharSet = 'UTF-8';

            // Mittente
            $mail->SetFrom($email_username, 'RaminoGame Test Sendmail');
            $mail->AddReplyTo($email_username, 'RaminoGame');

            // Oggetto e corpo
            $mail->Subject = '🧪 Test Sendmail - ' . date('d/m/Y H:i:s');

            $html_content = '
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
                    .container { background: white; padding: 30px; border-radius: 10px; max-width: 600px; margin: 0 auto; }
                    h1 { color: #28a745; }
                    .success-box { background: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #28a745; }
                    .info { background: #e7f3ff; padding: 15px; border-radius: 5px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>✅ Sendmail Funzionante!</h1>
                    <div class="success-box">
                        <p><strong>🎉 Questo metodo funziona perfettamente!</strong></p>
                        <p>L\'email è stata inviata usando <code>sendmail()</code> invece di SMTP.</p>
                    </div>
                    <div class="info">
                        <p><strong>Inviata il:</strong> ' . date('d/m/Y H:i:s') . '</p>
                        <p><strong>Metodo:</strong> PHP Sendmail (server mail locale)</p>
                        <p><strong>Da:</strong> ' . htmlspecialchars($email_username) . '</p>
                    </div>
                    <p>Se vedi questa email, possiamo usare sendmail per tutte le funzioni del sito:</p>
                    <ul>
                        <li>✅ Reset password</li>
                        <li>✅ Password magazzino</li>
                        <li>✅ Cancellazione account</li>
                        <li>✅ Cambio email</li>
                    </ul>
                </div>
            </body>
            </html>';

            $mail->MsgHTML($html_content);
            $mail->AltBody = 'Test email inviata con sendmail da RaminoGame';

            // Destinatario
            $mail->AddAddress($test_email, 'Test User');

            echo '<div class="debug">';
            echo '🔧 Configurazione usata:<br>';
            echo '- Metodo: Sendmail (isSendmail)<br>';
            echo '- CharSet: UTF-8<br>';
            echo '- Da: ' . htmlspecialchars($email_username) . '<br>';
            echo '- A: ' . htmlspecialchars($test_email) . '<br>';
            echo '</div>';

            // Tenta invio
            $start = microtime(true);
            $result = $mail->Send();
            $duration = round((microtime(true) - $start) * 1000);

            if($result) {
                echo '<div class="success">';
                echo '<h3>✅ EMAIL INVIATA CON SUCCESSO!</h3>';
                echo '<p><strong>Tempo di invio:</strong> ' . $duration . ' ms (velocissimo!)</p>';
                echo '<p><strong>📬 Controlla la tua email:</strong> ' . htmlspecialchars($test_email) . '</p>';
                echo '<p><strong>⚠️ Controlla anche lo SPAM!</strong></p>';
                echo '<hr>';
                echo '<h4>✅ Prossimo passo:</h4>';
                echo '<p>Se hai ricevuto l\'email, posso modificare <code>include/functions/sendEmail.php</code> per usare sendmail invece di SMTP.</p>';
                echo '<p>Questo risolverà tutti i problemi di invio email del sito! 🎯</p>';
                echo '</div>';
            } else {
                echo '<div class="error">';
                echo '<h3>❌ ERRORE NELL\'INVIO</h3>';
                echo '<p><strong>Dettagli:</strong></p>';
                echo '<p>' . htmlspecialchars($mail->ErrorInfo) . '</p>';
                echo '<p>Sendmail potrebbe non essere configurato correttamente sul server.</p>';
                echo '</div>';
            }
            ?>

        <?php else: ?>
            <p>Questo script testerà l'invio email usando <strong>sendmail()</strong> invece di SMTP.</p>
            <p>Il metodo sendmail:</p>
            <ul>
                <li>✅ Non usa connessioni SMTP esterne (niente porte bloccate)</li>
                <li>✅ Usa il server mail locale dell'hosting</li>
                <li>✅ È velocissimo (nessun timeout)</li>
                <li>✅ Funziona sempre su hosting condivisi con cPanel</li>
            </ul>

            <form method="post">
                <button type="submit" name="send_test">🚀 Testa Sendmail</button>
            </form>
        <?php endif; ?>
    </div>
</body>
</html>
