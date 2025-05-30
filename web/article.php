<?php
include 'includes/db.php';
include 'includes/header.php';
$id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
$stmt = $pdo->prepare("SELECT title, content FROM articles_1911_2 WHERE id = ?");
$stmt->execute([$id]);
$article = $stmt->fetch(PDO::FETCH_ASSOC);


?>

<div class="container">
<article>
    <?php if ($article): ?>
        <h2><?= htmlspecialchars($article['title']) ?></h2>
        <div><?= nl2br(htmlspecialchars($article['content'])) ?></div>
    <?php else: ?>
        <p>Article not found.</p>
    <?php endif; ?>
</article>

</div>

<?php include 'includes/footer.php'; ?>

