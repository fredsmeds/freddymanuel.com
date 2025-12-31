<?php
header('Content-Type: application/json');

// Load environment variables from .env file
function loadEnv($filePath) {
    if (!file_exists($filePath)) {
        error_log("ENV file not found: $filePath");
        return false;
    }
    $lines = file($filePath, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos(trim($line), '#') === 0) continue;
        if (strpos($line, '=') === false) continue;
        
        list($name, $value) = explode('=', $line, 2);
        $name = trim($name);
        $value = trim($value);
        
        // Remove quotes if present
        $value = trim($value, '"\'');
        
        $_ENV[$name] = $value;
        error_log("ENV: $name loaded");
    }
    return true;
}

// Load .env file
$envLoaded = loadEnv(__DIR__ . '/.env');

// Load PHPMailer
require __DIR__ . '/PHPMailer/src/Exception.php';
require __DIR__ . '/PHPMailer/src/PHPMailer.php';
require __DIR__ . '/PHPMailer/src/SMTP.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // 1. Gmail credentials from environment
    $gmail_user = $_ENV['GMAIL_USER'] ?? '';
    $gmail_pass = $_ENV['GMAIL_PASSWORD'] ?? '';
    $admin_email = $_ENV['ADMIN_EMAIL'] ?? $gmail_user;
    
    // 2. Collect form data
    $name = strip_tags(trim($_POST["name"]));
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    $phone = strip_tags(trim($_POST["phone"]));
    $project = strip_tags(trim($_POST["project-type"]));
    $message = strip_tags(trim($_POST["message"]));
    $privacy = isset($_POST["privacy"]);
    
    // 3. Validation
    if (empty($name) || empty($email) || empty($message) || !$privacy) {
        echo json_encode([
            'success' => false,
            'message' => 'Please fill in all required fields'
        ]);
        exit;
    }
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo json_encode([
            'success' => false,
            'message' => 'Invalid email format'
        ]);
        exit;
    }

    // Check if Gmail credentials are configured
    if (empty($gmail_user) || empty($gmail_pass)) {
        // Log to error file for debugging
        error_log("Gmail credentials missing - User: " . (!empty($gmail_user) ? "OK" : "MISSING") . " | Pass: " . (!empty($gmail_pass) ? "OK" : "MISSING"));
        echo json_encode([
            'success' => false,
            'message' => 'Email system is not properly configured. Please try again later.'
        ]);
        exit;
    }
    
    // 4. Project type mapping
    $project_types = [
        'ai-ml' => 'AI & Machine Learning',
        'web-dev' => 'Web Development & UX/UI',
        'branding' => 'Brand Identity & Strategy',
        'creative-production' => 'Creative Production',
        'art-direction' => 'Art Direction & Consultation',
        'performance' => 'Performance & Acting',
        'other' => 'Something else'
    ];
    $project_text = isset($project_types[$project]) ? $project_types[$project] : ($project ?: 'Not specified');
    
    try {
        // 5. Create PHPMailer instance
        $mail = new PHPMailer(true);
        
        // Enable debug output (comment out in production)
        // $mail->SMTPDebug = 2;
        
        // 6. Gmail SMTP settings
        $mail->isSMTP();
        $mail->Host = 'smtp.gmail.com';
        $mail->SMTPAuth = true;
        $mail->Username = $gmail_user;
        $mail->Password = $gmail_pass;
        $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
        $mail->Port = 587;
        $mail->Timeout = 30;
        $mail->SMTPKeepAlive = true;
        
        // 7. Email to YOU (admin)
        $mail->setFrom($gmail_user, 'Freddy Manuel Portfolio');
        $mail->addAddress($admin_email, 'Freddy Manuel');
        $mail->addReplyTo($email, $name);
        
        $mail->Subject = "New Contact Form: $name";
        $mail->Body = "New message from freddymanuel.com\n\n" .
                      "Name: $name\n" .
                      "Email: $email\n" .
                      "Phone: " . ($phone ?: 'Not provided') . "\n" .
                      "Project: $project_text\n\n" .
                      "Message:\n$message\n\n" .
                      "---\n" .
                      "Sent: " . date('Y-m-d H:i:s');
        
        $mail->send();
        
        // 8. Log to CSV file
        $csvFile = __DIR__ . '/submissions.csv';
        $csvExists = file_exists($csvFile);
        
        $csvData = [
            date('Y-m-d H:i:s'),
            $name,
            $email,
            $phone ?: 'N/A',
            $project_text,
            $message
        ];
        
        $handle = fopen($csvFile, 'a');
        if ($csvExists === false) {
            // Write header if file is new
            fputcsv($handle, ['Timestamp', 'Name', 'Email', 'Phone', 'Project Type', 'Message']);
        }
        fputcsv($handle, $csvData);
        fclose($handle);
        
        // 9. Confirmation email to USER
        $mail->clearAddresses();
        $mail->clearReplyTos();
        $mail->addAddress($email, $name);
        $mail->addReplyTo($gmail_user, 'Freddy Manuel');
        
        $mail->Subject = "Thank you for contacting Freddy Manuel";
        $mail->Body = "Hi $name,\n\n" .
                      "Thank you for reaching out! I'll respond within 48 hours.\n\n" .
                      "Your message:\n$message\n\n" .
                      "Best regards,\n" .
                      "Freddy Manuel Roldán Rivero\n" .
                      "AI Engineer & Conceptual Artist\n\n" .
                      "fmroldanrivero@gmail.com\n" .
                      "https://freddymanuel.com";
        
        $mail->send();
        
        // 9. Success!
        echo json_encode([
            'success' => true,
            'message' => 'Message sent successfully! Check your email for confirmation.'
        ]);
        
    } catch (Exception $e) {
        error_log("PHPMailer Error: " . $e->getMessage());
        echo json_encode([
            'success' => false,
            'message' => 'Failed to send: ' . $e->getMessage()
        ]);
    } catch (Throwable $e) {
        error_log("Unexpected Error: " . $e->getMessage());
        echo json_encode([
            'success' => false,
            'message' => 'An unexpected error occurred. Please try again later.'
        ]);
    }
    
} else {
    echo json_encode([
        'success' => false,
        'message' => 'Invalid request method'
    ]);
}
?>