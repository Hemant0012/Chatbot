<?php
// Enable CORS if you're accessing from a different domain (optional)
// header("Access-Control-Allow-Origin: *");
// header("Access-Control-Allow-Methods: POST");
// header("Access-Control-Allow-Headers: Content-Type");

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo "⚠️ Invalid request method.";
    exit;
}

$action = $_POST['action'] ?? '';
if ($action !== 'chat') {
    echo "⚠️ Invalid action.";
    exit;
}

$question = trim($_POST['question'] ?? '');
$url = trim($_POST['url'] ?? '');

if (empty($question) || empty($url)) {
    echo "❌ Please enter both a question and a valid URL.";
    exit;
}

$payload = json_encode([
    "question" => $question,
    "url" => $url,
]);

$ch = curl_init("http://127.0.0.1:8000/chat");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Accept: application/json',
]);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

if (curl_errno($ch)) {
    echo "⚠️ Curl Error: " . curl_error($ch);
    curl_close($ch);
    exit;
}
curl_close($ch);

// If backend returned an error status
if ($httpCode !== 200) {
    echo "⚠️ AI backend error (HTTP $httpCode).";
    exit;
}

// Try parsing JSON
$result = json_decode($response, true);
if (json_last_error() !== JSON_ERROR_NONE) {
    echo "⚠️ Failed to parse AI response: " . json_last_error_msg();
    exit;
}

// Return answer
echo $result['answer'] ?? "⚠️ No answer received from AI.";
