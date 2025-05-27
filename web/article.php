<?php
include 'includes/db.php';

$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$stmt = $pdo->prepare("SELECT title, content FROM articles_1911 WHERE id = ?");
$stmt->execute([$id]);
$article = $stmt->fetch(PDO::FETCH_ASSOC);

include 'includes/header.php';
?>

<article>
    <?php if ($article): ?>
        <h2><?= htmlspecialchars($article['title']) ?></h2>
        <div><?= nl2br(htmlspecialchars($article['content'])) ?></div>
    <?php else: ?>
        <p>Article not found.</p>
    <?php endif; ?>
</article>

<?php include 'includes/footer.php'; ?>

