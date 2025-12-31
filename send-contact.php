<?php
header('Content-Type: application/json');
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/php_errors.log');

// Load PHPMailer - MANUAL METHOD
require __DIR__ . '/PHPMailer/src/Exception.php';
require __DIR__ . '/PHPMailer/src/PHPMailer.php';
require __DIR__ . '/PHPMailer/src/SMTP.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

// ===== CONFIGURATION =====
$GMAIL_USERNAME = 'fmroldanrivero@gmail.com';
$GMAIL_APP_PASSWORD = 'ndjidenozkbhdxr'; // Gmail App Password (no spaces)
$TO_EMAIL = 'fmroldanrivero@gmail.com';
$FROM_EMAIL = 'fmroldanrivero@gmail.com';
$FROM_NAME = 'Freddy Manuel Portfolio';

// Sanitize function
function sanitize_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

// Check POST request
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode([
        'success' => false,
        'message' => 'Invalid request method'
    ]);
    exit;
}

// Get and sanitize form data
$name = isset($_POST['name']) ? sanitize_input($_POST['name']) : '';
$email = isset($_POST['email']) ? sanitize_input($_POST['email']) : '';
$phone = isset($_POST['phone']) ? sanitize_input($_POST['phone']) : '';
$project = isset($_POST['project-type']) ? sanitize_input($_POST['project-type']) : 'Not specified';
$message = isset($_POST['message']) ? sanitize_input($_POST['message']) : '';
$privacy = isset($_POST['privacy']);

// Validation
$errors = [];

if (empty($name)) {
    $errors[] = 'Name is required';
}

if (empty($email)) {
    $errors[] = 'Email is required';
} elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Invalid email format';
}

if (empty($message)) {
    $errors[] = 'Message is required';
}

if (!$privacy) {
    $errors[] = 'You must agree to the Privacy Policy and Terms of Use';
}

// Return validation errors
if (!empty($errors)) {
    echo json_encode([
        'success' => false,
        'message' => implode(', ', $errors)
    ]);
    exit;
}

// Project type mapping
$project_types = [
    'ai-ml' => 'AI & Machine Learning',
    'web-dev' => 'Web Development & UX/UI',
    'branding' => 'Brand Identity & Strategy',
    'creative-production' => 'Creative Production',
    'art-direction' => 'Art Direction & Consultation',
    'performance' => 'Performance & Acting',
    'other' => 'Something else'
];
$project_text = isset($project_types[$project]) ? $project_types[$project] : $project;

try {
    // ===== EMAIL TO ADMIN (YOU) =====
    $mail_admin = new PHPMailer(true);
    
    // SMTP Configuration
    $mail_admin->isSMTP();
    $mail_admin->Host = 'smtp.gmail.com';
    $mail_admin->SMTPAuth = true;
    $mail_admin->Username = $GMAIL_USERNAME;
    $mail_admin->Password = $GMAIL_APP_PASSWORD;
    $mail_admin->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail_admin->Port = 587;
    $mail_admin->CharSet = 'UTF-8';
    
    // Enable verbose debug output (disable in production)
    // $mail_admin->SMTPDebug = 2; // Uncomment for debugging
    
    // Email settings
    $mail_admin->setFrom($FROM_EMAIL, $FROM_NAME);
    $mail_admin->addAddress($TO_EMAIL, 'Freddy Manuel');
    $mail_admin->addReplyTo($email, $name);
    
    $mail_admin->Subject = "New Contact Form Submission: $name";
    $mail_admin->Body = 
        "You have received a new message from freddymanuel.com\n\n" .
        "═══════════════════════════════════\n" .
        "CONTACT DETAILS\n" .
        "═══════════════════════════════════\n\n" .
        "Name: $name\n" .
        "Email: $email\n" .
        "Phone: " . ($phone ?: 'Not provided') . "\n" .
        "Project Type: $project_text\n\n" .
        "═══════════════════════════════════\n" .
        "MESSAGE\n" .
        "═══════════════════════════════════\n\n" .
        "$message\n\n" .
        "═══════════════════════════════════\n" .
        "Sent: " . date('l, F j, Y - g:i A') . "\n" .
        "IP Address: " . $_SERVER['REMOTE_ADDR'] . "\n" .
        "═══════════════════════════════════";
    
    $mail_admin->send();
    
    // ===== CONFIRMATION EMAIL TO USER =====
    $mail_user = new PHPMailer(true);
    
    // SMTP Configuration
    $mail_user->isSMTP();
    $mail_user->Host = 'smtp.gmail.com';
    $mail_user->SMTPAuth = true;
    $mail_user->Username = $GMAIL_USERNAME;
    $mail_user->Password = $GMAIL_APP_PASSWORD;
    $mail_user->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail_user->Port = 587;
    $mail_user->CharSet = 'UTF-8';
    
    // Email settings
    $mail_user->setFrom($FROM_EMAIL, $FROM_NAME);
    $mail_user->addAddress($email, $name);
    $mail_user->addReplyTo($TO_EMAIL, 'Freddy Manuel');
    
    $mail_user->Subject = "Thank you for contacting Freddy Manuel";
    $mail_user->Body = 
        "Hi $name,\n\n" .
        "Thank you for reaching out! I've received your message and will respond within 48 hours.\n\n" .
        "═══════════════════════════════════\n" .
        "YOUR MESSAGE\n" .
        "═══════════════════════════════════\n\n" .
        "Project Type: $project_text\n\n" .
        "$message\n\n" .
        "═══════════════════════════════════\n\n" .
        "Best regards,\n\n" .
        "Freddy Manuel Roldán Rivero\n" .
        "AI Engineer & Conceptual Artist\n\n" .
        "Email: fmroldanrivero@gmail.com\n" .
        "Portfolio: https://freddymanuel.com\n" .
        "LinkedIn: https://www.linkedin.com/in/freddyrivero-aiengineer/\n" .
        "GitHub: https://github.com/fredsmeds\n\n" .
        "═══════════════════════════════════";
    
    $mail_user->send();
    
    // Success response
    echo json_encode([
        'success' => true,
        'message' => 'Message sent successfully! Check your email for confirmation.'
    ]);
    
} catch (Exception $e) {
    // Log the detailed error
    error_log("PHPMailer Error: " . $e->getMessage());
    if (isset($mail_admin)) {
        error_log("SMTP Error Info: " . $mail_admin->ErrorInfo);
    }
    
    // Return user-friendly error
    echo json_encode([
        'success' => false,
        'message' => 'Failed to send message. Please try emailing directly: fmroldanrivero@gmail.com'
    ]);
}
?>