<?php
/**
 * Verifica configurazione SMTP completa
 * Mostra ESATTAMENTE cosa sta usando il sito
 */

require_once(__DIR__ . '/include/functions/env.php');
loadEnv(__DIR__ . '/.env');
require_once(__DIR__ . '/config.php');

?>
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifica Configurazione SMTP</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
            background: #1a1a1a;
            color: #0F0;
        }
        .card {
            background: #000;
            padding: 30px;
            border-radius: 10px;
            border: 2px solid #0F0;
            box-shadow: 0 0 20px rgba(0, 255, 0, 0.3);
        }
        h1 {
            color: #0F0;
            text-shadow: 0 0 10px #0F0;
        }
        .section {
            background: #0a0a0a;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #0F0;
        }
        .key {
            color: #00FF00;
            font-weight: bold;
        }
        .value {
            color: #FFFF00;
        }
        .success {
            color: #00FF00;
        }
        .error {
            color: #FF0000;
        }
        .warning {
            color: #FFA500;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border: 1px solid #0F0;
        }
        th {
            background: #003300;
            color: #0F0;
        }
        td {
            background: #001a00;
        }
        .test-btn {
            background: #0F0;
            color: #000;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin: 20px 0;
        }
        .test-btn:hover {
            background: #0C0;
            box-shadow: 0 0 20px #0F0;
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🔍 VERIFICA CONFIGURAZIONE SMTP</h1>

        <div class="section">
            <h2>📋 Configurazioni Caricate da .env / config.php</h2>
            <table>
                <tr>
                    <th>Variabile</th>
                    <th>Valore</th>
                    <th>Status</th>
                </tr>
                <tr>
                    <td class="key">$EmailHost</td>
                    <td class="value"><?php echo htmlspecialchars($EmailHost); ?></td>
                    <td class="<?php echo !empty($EmailHost) ? 'success' : 'error'; ?>">
                        <?php echo !empty($EmailHost) ? '✅ OK' : '❌ VUOTO'; ?>
                    </td>
                </tr>
                <tr>
                    <td class="key">$emailPort</td>
                    <td class="value"><?php echo htmlspecialchars($emailPort); ?></td>
                    <td class="<?php echo !empty($emailPort) ? 'success' : 'error'; ?>">
                        <?php echo !empty($emailPort) ? '✅ OK' : '❌ VUOTO'; ?>
                    </td>
                </tr>
                <tr>
                    <td class="key">$SMTPSecure</td>
                    <td class="value"><?php echo htmlspecialchars($SMTPSecure); ?></td>
                    <td class="<?php echo !empty($SMTPSecure) ? 'success' : 'error'; ?>">
                        <?php echo !empty($SMTPSecure) ? '✅ OK' : '❌ VUOTO'; ?>
                    </td>
                </tr>
                <tr>
                    <td class="key">$SMTPAuth</td>
                    <td class="value"><?php echo $SMTPAuth ? 'true' : 'false'; ?></td>
                    <td class="<?php echo $SMTPAuth ? 'success' : 'error'; ?>">
                        <?php echo $SMTPAuth ? '✅ Abilitato' : '❌ Disabilitato'; ?>
                    </td>
                </tr>
                <tr>
                    <td class="key">$email_username</td>
                    <td class="value"><?php echo htmlspecialchars($email_username); ?></td>
                    <td class="<?php echo !empty($email_username) ? 'success' : 'error'; ?>">
                        <?php echo !empty($email_username) ? '✅ OK' : '❌ VUOTO'; ?>
                    </td>
                </tr>
                <tr>
                    <td class="key">$email_password</td>
                    <td class="value"><?php echo empty($email_password) ? '❌ VUOTA' : '✅ Configurata (' . str_repeat('*', strlen($email_password)) . ')'; ?></td>
                    <td class="<?php echo !empty($email_password) ? 'success' : 'error'; ?>">
                        <?php echo !empty($email_password) ? '✅ OK' : '❌ VUOTA'; ?>
                    </td>
                </tr>
            </table>
        </div>

        <div class="section">
            <h2>🔧 Test Connessione SMTP</h2>
            <?php
            // Test connessione socket
            $host = $EmailHost;
            $port = $emailPort;

            echo "<p><strong>Test connessione a:</strong> <span class='value'>{$host}:{$port}</span></p>";

            $errno = 0;
            $errstr = '';
            $timeout = 5;

            $startTime = microtime(true);
            $connection = @fsockopen($host, $port, $errno, $errstr, $timeout);
            $duration = round((microtime(true) - $startTime) * 1000);

            if ($connection) {
                echo "<p class='success'>✅ CONNESSIONE RIUSCITA! (Tempo: {$duration}ms)</p>";
                echo "<p class='success'>✅ La porta {$port} è APERTA e raggiungibile</p>";
                fclose($connection);
            } else {
                echo "<p class='error'>❌ CONNESSIONE FALLITA! (Timeout dopo {$duration}ms)</p>";
                echo "<p class='error'>❌ Errore: [{$errno}] {$errstr}</p>";
                echo "<p class='warning'>⚠️ La porta {$port} potrebbe essere BLOCCATA dal firewall</p>";
            }
            ?>
        </div>

        <div class="section">
            <h2>📧 Test Invio Email</h2>
            <?php if(isset($_POST['test_email'])): ?>
                <?php
                require 'include/mailer/PHPMailer.php';
                require 'include/mailer/SMTP.php';
                require 'include/mailer/Exception.php';
                use PHPMailer\PHPMailer\PHPMailer;

                $mail = new PHPMailer();
                $mail->IsSMTP();
                $mail->SMTPDebug = 0;
                $mail->Timeout = 10;
                $mail->CharSet = 'UTF-8';
                $mail->SMTPAuth = $SMTPAuth;
                $mail->SMTPSecure = $SMTPSecure;
                $mail->Host = $EmailHost;
                $mail->Port = $emailPort;
                $mail->Username = $email_username;
                $mail->Password = $email_password;

                $mail->SetFrom($email_username, 'Test SMTP');
                $mail->Subject = 'Test Email SMTP - ' . date('H:i:s');
                $mail->Body = 'Test configurazione SMTP';
                $mail->AddAddress($_POST['email'], 'Test');

                echo "<p><strong>Tentativo invio a:</strong> <span class='value'>" . htmlspecialchars($_POST['email']) . "</span></p>";

                $startTime = microtime(true);
                if($mail->Send()) {
                    $duration = round((microtime(true) - $startTime) * 1000);
                    echo "<p class='success'>✅ EMAIL INVIATA CON SUCCESSO! (Tempo: {$duration}ms)</p>";
                    echo "<p class='success'>✅ SMTP funziona correttamente!</p>";
                    echo "<p class='warning'>⚠️ Controlla SPAM/Posta indesiderata</p>";
                } else {
                    $duration = round((microtime(true) - $startTime) * 1000);
                    echo "<p class='error'>❌ INVIO FALLITO! (Timeout dopo {$duration}ms)</p>";
                    echo "<p class='error'>❌ Errore: " . htmlspecialchars($mail->ErrorInfo) . "</p>";
                }
                ?>
            <?php else: ?>
                <form method="post">
                    <p><strong>Email destinatario:</strong></p>
                    <input type="email" name="email" value="metalrambo95@hotmail.it" style="width: 100%; padding: 10px; background: #001a00; border: 2px solid #0F0; color: #0F0; font-size: 16px; margin: 10px 0;">
                    <button type="submit" name="test_email" class="test-btn">🧪 TESTA INVIO EMAIL</button>
                </form>
            <?php endif; ?>
        </div>

        <div class="section">
            <h2>💡 Consigli del Developer</h2>
            <p><strong>"Check the SMTP settings from homepage for reset/forgot password."</strong></p>
            <ul>
                <li class="success">✅ Tutte le configurazioni sono nel file <strong>config.php</strong></li>
                <li class="success">✅ Le variabili vengono caricate dal file <strong>.env</strong></li>
                <li class="warning">⚠️ Se il test di connessione fallisce, il firewall blocca la porta SMTP</li>
                <li class="warning">⚠️ Se il test email fallisce, le credenziali potrebbero essere sbagliate</li>
            </ul>
        </div>

        <div class="section">
            <h2>🔥 Cosa fare se NON funziona:</h2>
            <ol>
                <li><strong>Se connessione fallisce:</strong> Chiedi all'hosting di aprire porta <?php echo $emailPort; ?></li>
                <li><strong>Se invio fallisce:</strong> Verifica username/password email in cPanel</li>
                <li><strong>Alternative:</strong>
                    <ul>
                        <li>Prova porta <strong>587 con TLS</strong> invece di 465 con SSL</li>
                        <li>Usa <strong>localhost</strong> invece di <?php echo $EmailHost; ?></li>
                        <li>Usa <strong>sendmail()</strong> invece di SMTP</li>
                    </ul>
                </li>
            </ol>
        </div>
    </div>
</body>
</html>
