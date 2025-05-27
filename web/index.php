<?php
include 'includes/db.php';
include 'includes/header.php';

$results = [];
$query = '';
$error = null;

if (isset($_GET['q'])) {
    $query = trim($_GET['q']);

    if ($query !== '') {
        try {
            $stmt = $pdo->prepare("
                SELECT id, title, short_title 
                FROM articles_1911 
                WHERE title LIKE :q OR short_title LIKE :q 
                ORDER BY title 
                LIMIT 1000
            ");
            $stmt->execute(['q' => '%' . $query . '%']);
            $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch (PDOException $e) {
            $error = $e->getMessage();
        }
    }
}
?>
<?php if ($error): ?>
    <p style="color: red;">Error: <?= htmlspecialchars($error) ?></p>
<?php endif; ?>

<p>Debug: query = <code><?= htmlspecialchars($query) ?></code>, results = <?= count($results) ?></p>


<section>
    <form method="get">
        <input type="text" name="q" value="<?= htmlspecialchars($query) ?>" placeholder="Search articles..." autofocus>
        <button type="submit">Search</button>
    </form>
</section>

<section>
    <?php if ($query && empty($results)): ?>
        <p>No results found for <strong><?= htmlspecialchars($query) ?></strong>.</p>
    <?php elseif (!empty($results)): ?>
        <table border="1" cellpadding="5" cellspacing="0">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Short Title</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($results as $row): ?>
                    <tr>
                        <td><?= $row['id'] ?></td>
                        <td><?= htmlspecialchars($row['title']) ?></td>
                        <td><?= htmlspecialchars($row['short_title']) ?></td>
                        <td><a href="article.php?id=<?= $row['id'] ?>" target="_blank">View</a></td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php endif; ?>
</section>




<?php include 'includes/footer.php'; ?>

