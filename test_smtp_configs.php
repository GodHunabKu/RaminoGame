<?php
/**
 * Script di test automatico per trovare la configurazione SMTP corretta
 * Testa diverse configurazioni comuni per trovare quella funzionante
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

// Configurazioni da testare
$configurations = [
    [
        'name' => 'Localhost con SSL (porta 465)',
        'host' => 'localhost',
        'port' => 465,
        'secure' => 'ssl',
        'auth' => true
    ],
    [
        'name' => 'Localhost con TLS (porta 587)',
        'host' => 'localhost',
        'port' => 587,
        'secure' => 'tls',
        'auth' => true
    ],
    [
        'name' => 'mail.oneshyra.eu con SSL (porta 465)',
        'host' => 'mail.oneshyra.eu',
        'port' => 465,
        'secure' => 'ssl',
        'auth' => true
    ],
    [
        'name' => 'mail.oneshyra.eu con TLS (porta 587)',
        'host' => 'mail.oneshyra.eu',
        'port' => 587,
        'secure' => 'tls',
        'auth' => true
    ],
    [
        'name' => 'oneshyra.eu con SSL (porta 465)',
        'host' => 'oneshyra.eu',
        'port' => 465,
        'secure' => 'ssl',
        'auth' => true
    ],
    [
        'name' => 'oneshyra.eu con TLS (porta 587)',
        'host' => 'oneshyra.eu',
        'port' => 587,
        'secure' => 'tls',
        'auth' => true
    ],
    [
        'name' => 'Localhost senza crittografia (porta 25)',
        'host' => 'localhost',
        'port' => 25,
        'secure' => '',
        'auth' => false
    ]
];

?>
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Configurazioni SMTP - RaminoGame</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1000px;
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
        h1 { color: #333; margin-top: 0; }
        h2 { color: #555; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .config-test {
            background: #f9f9f9;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
            border-left: 4px solid #6c757d;
        }
        .config-test.testing {
            border-left-color: #ffc107;
            background: #fff3cd;
        }
        .config-test.success {
            border-left-color: #28a745;
            background: #d4edda;
        }
        .config-test.failed {
            border-left-color: #dc3545;
            background: #f8d7da;
        }
        .config-name {
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .config-details {
            font-size: 13px;
            color: #666;
            margin-bottom: 10px;
        }
        .result {
            margin-top: 10px;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        .result.success {
            background: #28a745;
            color: white;
        }
        .result.failed {
            background: #dc3545;
            color: white;
        }
        .error-details {
            margin-top: 5px;
            font-size: 12px;
            opacity: 0.9;
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
        button:disabled {
            background: #6c757d;
            cursor: not-allowed;
        }
        .recommendation {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
        .current-config {
            background: #e7f3ff;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(0,0,0,.1);
            border-radius: 50%;
            border-top-color: #007bff;
            animation: spin 1s ease-in-out infinite;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>🧪 Test Automatico Configurazioni SMTP</h1>

        <div class="current-config">
            <h3>📋 Configurazione Attuale (.env):</h3>
            <p><strong>Host:</strong> <?php echo htmlspecialchars($EmailHost); ?></p>
            <p><strong>Porta:</strong> <?php echo $emailPort; ?></p>
            <p><strong>Secure:</strong> <?php echo htmlspecialchars($SMTPSecure); ?></p>
            <p><strong>Username:</strong> <?php echo htmlspecialchars($email_username); ?></p>
            <p><strong>Email test:</strong> <?php echo htmlspecialchars($test_email); ?></p>
        </div>

        <?php if(isset($_POST['test_all'])): ?>
            <h2>🔍 Test delle Configurazioni</h2>
            <p>Testando <?php echo count($configurations); ?> configurazioni diverse...</p>

            <?php
            $working_configs = [];

            foreach($configurations as $index => $config) {
                echo '<div class="config-test testing" id="config-' . $index . '">';
                echo '<div class="config-name">⚙️ ' . htmlspecialchars($config['name']) . '</div>';
                echo '<div class="config-details">';
                echo 'Host: ' . htmlspecialchars($config['host']) . ' | ';
                echo 'Porta: ' . $config['port'] . ' | ';
                echo 'Sicurezza: ' . ($config['secure'] ? htmlspecialchars($config['secure']) : 'nessuna') . ' | ';
                echo 'Auth: ' . ($config['auth'] ? 'Sì' : 'No');
                echo '</div>';

                // Test connessione
                $mail = new PHPMailer();
                $mail->IsSMTP();
                $mail->SMTPDebug = 0;
                $mail->Timeout = 10;
                $mail->CharSet = 'UTF-8';
                $mail->SMTPAuth = $config['auth'];

                if($config['secure']) {
                    $mail->SMTPSecure = $config['secure'];
                }

                $mail->Host = $config['host'];
                $mail->Port = $config['port'];

                if($config['auth']) {
                    $mail->Username = $email_username;
                    $mail->Password = $email_password;
                }

                $mail->SetFrom($email_username, 'Test SMTP');
                $mail->Subject = 'Test Configurazione SMTP - ' . date('H:i:s');
                $mail->Body = 'Test configurazione: ' . $config['name'];
                $mail->AddAddress($test_email);

                $start = microtime(true);
                $result = @$mail->Send();
                $duration = round((microtime(true) - $start) * 1000);

                if($result) {
                    echo '<div class="result success">';
                    echo '✅ <strong>SUCCESSO!</strong> Email inviata in ' . $duration . 'ms';
                    echo '</div>';
                    echo '</div>';

                    $working_configs[] = $config;

                    // Evidenzia come successo
                    echo '<script>document.getElementById("config-' . $index . '").className = "config-test success";</script>';

                    // Ferma il test dopo il primo successo
                    break;
                } else {
                    echo '<div class="result failed">';
                    echo '❌ <strong>FALLITO</strong> (Timeout dopo ' . $duration . 'ms)';
                    echo '<div class="error-details">' . htmlspecialchars($mail->ErrorInfo) . '</div>';
                    echo '</div>';
                    echo '</div>';

                    // Evidenzia come fallito
                    echo '<script>document.getElementById("config-' . $index . '").className = "config-test failed";</script>';
                }

                // Flush output per vedere i risultati in tempo reale
                @ob_flush();
                @flush();
            }

            // Raccomandazioni finali
            if(count($working_configs) > 0) {
                echo '<div class="recommendation">';
                echo '<h3>✅ Configurazione Funzionante Trovata!</h3>';
                echo '<p><strong>Usa questa configurazione nel tuo file .env:</strong></p>';
                $best = $working_configs[0];
                echo '<pre style="background: white; padding: 15px; border-radius: 5px;">';
                echo 'EMAIL_HOST=' . $best['host'] . "\n";
                echo 'EMAIL_PORT=' . $best['port'] . "\n";
                echo 'SMTP_SECURE=' . $best['secure'] . "\n";
                echo 'SMTP_AUTH=' . ($best['auth'] ? 'true' : 'false') . "\n";
                echo 'EMAIL_USERNAME=support@oneshyra.eu' . "\n";
                echo 'EMAIL_PASSWORD=Bigkebab95';
                echo '</pre>';
                echo '<p><strong>✉️ Controlla la tua email:</strong> ' . htmlspecialchars($test_email) . '</p>';
                echo '</div>';
            } else {
                echo '<div class="recommendation" style="background: #f8d7da; border-color: #f5c6cb; color: #721c24;">';
                echo '<h3>❌ Nessuna Configurazione SMTP Funzionante</h3>';
                echo '<p><strong>Tutte le configurazioni SMTP sono fallite.</strong></p>';
                echo '<p>Opzioni:</p>';
                echo '<ol>';
                echo '<li><strong>Usa sendmail() invece di SMTP</strong> - Funziona sempre su hosting condivisi</li>';
                echo '<li><strong>Contatta il supporto hosting</strong> - Chiedi di sbloccare le porte SMTP (465, 587)</li>';
                echo '<li><strong>Verifica le credenziali email</strong> - Assicurati che username e password siano corretti</li>';
                echo '</ol>';
                echo '<p><strong>Vuoi che modifichi il codice per usare sendmail()?</strong></p>';
                echo '</div>';
            }
            ?>

        <?php else: ?>
            <p>Questo script testerà automaticamente <?php echo count($configurations); ?> configurazioni SMTP diverse per trovare quella funzionante.</p>

            <h3>🔧 Configurazioni che verranno testate:</h3>
            <ul>
                <?php foreach($configurations as $config): ?>
                    <li><?php echo htmlspecialchars($config['name']); ?></li>
                <?php endforeach; ?>
            </ul>

            <form method="post">
                <button type="submit" name="test_all">🚀 Avvia Test Automatico</button>
            </form>
        <?php endif; ?>
    </div>
</body>
</html>
