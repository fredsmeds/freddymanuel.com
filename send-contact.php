<?php
header('Content-Type: application/json');

// Enable error reporting for debugging (remove in production)
error_reporting(E_ALL);
ini_set('display_errors', 0);

// Configuration
$to_email = 'fmroldanrivero@gmail.com';
$from_email = 'noreply@freddymanuel.com'; // Should match your domain

// Function to sanitize input
function sanitize_input($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data);
    return $data;
}

// Check if form was submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    // Get and sanitize form data
    $name = isset($_POST['name']) ? sanitize_input($_POST['name']) : '';
    $email = isset($_POST['email']) ? sanitize_input($_POST['email']) : '';
    $phone = isset($_POST['phone']) ? sanitize_input($_POST['phone']) : '';
    $project = isset($_POST['project']) ? sanitize_input($_POST['project']) : 'Not specified';
    $message = isset($_POST['message']) ? sanitize_input($_POST['message']) : '';
    $privacy = isset($_POST['privacy']) ? true : false;
    
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
    
    // If there are validation errors
    if (!empty($errors)) {
        echo json_encode([
            'success' => false,
            'message' => implode(', ', $errors)
        ]);
        exit;
    }
    
    // Prepare project type text
    $project_types = [
        'ai-ml' => 'AI & Machine Learning',
        'web-dev' => 'Web Development',
        'branding' => 'Branding & Identity',
        'creative-production' => 'Creative Production',
        'art-direction' => 'Art Direction',
        'performance' => 'Performance/Acting',
        'other' => 'Other'
    ];
    $project_text = isset($project_types[$project]) ? $project_types[$project] : $project;
    
    // --- EMAIL TO ADMIN ---
    $admin_subject = "New Contact Form Submission from $name";
    
    $admin_message = "You have received a new message from your portfolio contact form.\n\n";
    $admin_message .= "Name: $name\n";
    $admin_message .= "Email: $email\n";
    $admin_message .= "Phone: " . ($phone ?: 'Not provided') . "\n";
    $admin_message .= "Project Type: $project_text\n\n";
    $admin_message .= "Message:\n$message\n\n";
    $admin_message .= "---\n";
    $admin_message .= "Sent from freddymanuel.com contact form\n";
    $admin_message .= "Date: " . date('Y-m-d H:i:s') . "\n";
    
    $admin_headers = "From: $from_email\r\n";
    $admin_headers .= "Reply-To: $email\r\n";
    $admin_headers .= "X-Mailer: PHP/" . phpversion();
    
    $admin_sent = mail($to_email, $admin_subject, $admin_message, $admin_headers);
    
    // --- CONFIRMATION EMAIL TO USER ---
    $user_subject = "Thank you for contacting Freddy Manuel";
    
    $user_message = "Hi $name,\n\n";
    $user_message .= "Thank you for reaching out. I have received your message and will respond within 48 hours.\n\n";
    $user_message .= "Here's a copy of your message:\n\n";
    $user_message .= "---\n\n";
    $user_message .= "Project Type: $project_text\n\n";
    $user_message .= "Message:\n$message\n\n";
    $user_message .= "---\n\n";
    $user_message .= "Best regards,\n";
    $user_message .= "Freddy Manuel Roldán Rivero\n";
    $user_message .= "AI Engineer & Conceptual Artist\n\n";
    $user_message .= "Email: fmroldanrivero@gmail.com\n";
    $user_message .= "Portfolio: https://freddymanuel.com\n";
    $user_message .= "LinkedIn: https://www.linkedin.com/in/freddyrivero-aiengineer/\n";
    $user_message .= "GitHub: https://github.com/fredsmeds\n";
    
    $user_headers = "From: $from_email\r\n";
    $user_headers .= "Reply-To: $to_email\r\n";
    $user_headers .= "X-Mailer: PHP/" . phpversion();
    
    $user_sent = mail($email, $user_subject, $user_message, $user_headers);
    
    // Check if emails were sent
    if ($admin_sent) {
        echo json_encode([
            'success' => true,
            'message' => 'Message sent successfully!'
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'message' => 'Failed to send message. Please try emailing directly: fmroldanrivero@gmail.com'
        ]);
    }
    
} else {
    // Not a POST request
    echo json_encode([
        'success' => false,
        'message' => 'Invalid request method'
    ]);
}
?>
