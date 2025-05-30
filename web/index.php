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
                SELECT id, title, short_title, volume, page 
                FROM articles_1911_2 
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
$page_offsets = [
    1 => 31,
    2 => 11,
    3 => 17,
    4 => 13,
    5 => 16,
    6 => 16,
    7 => 16,
    8 => 16,
    9 => 16,
    10 => 16,
    11 => 16,
    12 => 16,
    13 => 16,
    14 => 16,
    15 => 16,
    16 => 16,
    17 => 16,
    18 => 16,
    20 => 16,
    21 => 16,
    22 => 16,
    23 => 16,
    24 => 16,
    25 => 16,
    26 => 16,
    27 => 16,
    28 => 16,

];
?>
<?php if ($error): ?>
    <p style="color: red;">Error: <?= htmlspecialchars($error) ?></p>
<?php endif; ?>


<p>Debug: query = <code><?= htmlspecialchars($query) ?></code>, results = <?= count($results) ?></p>

<section class="info-banner">
    <p>
        This is a project to digitize the 1911 Encyclopædia Britannica, one of the most ambitious and extensive encyclopedic compilations in human history. While dated in many respects, it is still an invaluable catalogue of knowledge and data, and where it is dated, it provides insights into how views have changed. The whole encyclopedia has been in the public domain for some time, but was only available as image scan with poor OCR data. Here is a prototype version of a searchable database, with the pdfs also (roughly) linked. Any tables and figures are not captured in the existing OCR and are only visible in the pdfs.<br> View the project on <a href="https://github.com/fsncps/britannica" target="_blank">GitHub</a>.
    </p>
</section>


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
                    <th>PDF</th>
                    <th>TEXT</th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($results as $row): ?>
                    <tr>
                        <td><?= $row['id'] ?></td>
                        <td><?= htmlspecialchars($row['title']) ?></td>
      <td>
          <?php if ($row['volume']): ?>
              <?php
                  $offset = $page_offsets[$row['volume']] ?? 0;
                  $raw_page = $row['page'] ?: 1;
                  $pdf_page = $raw_page + $offset;
              ?>
              <a href="pdf/VOL<?= $row['volume'] ?>.pdf#page=<?= $pdf_page ?>" target="_blank">View PDF</a>
          <?php else: ?>
              —
          <?php endif; ?>
      </td>

                        <td>
                            <a href="article.php?id=<?= $row['id'] ?>" target="_blank">View Text</a>
                        </td>
                    </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
    <?php endif; ?>
</section>

<?php include 'includes/footer.php'; ?>
