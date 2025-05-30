<?php
include 'includes/db.php';

if (!isset($_GET['id']) || !is_numeric($_GET['id'])) {
    http_response_code(400);
    echo 'Invalid request';
    exit;
}

$id = (int) $_GET['id'];

$stmt = $pdo->prepare("SELECT title, content FROM articles_1911_2 WHERE id = ?");
$stmt->execute([$id]);
$article = $stmt->fetch(PDO::FETCH_ASSOC);

if (!$article) {
    http_response_code(404);
    echo 'Article not found';
    exit;
}

echo "<h2>" . htmlspecialchars($article['title']) . "</h2>";
echo "<div>" . nl2br(htmlspecialchars($article['content'])) . "</div>";

