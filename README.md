# Encyclopedia Britannica 11th Edition (1911) Clone

A public-domain preservation and transformation project. The aim is to make the *1911 Encyclopædia Britannica 11th edition* (EB11) fully accessible in modern formats: searchable, cleanly structured and analyzable. EB11 remains one of the most ambitious encyclopedic projects in history, but its text has never been systematically digitized and formatted. Alongside creating a modern reading experience, the project aims to analyze epistemic and rhetorical shifts by comparing EB11 articles to their modern Wikipedia counterparts.

**[HERE](https://eb.kallisti.ch)** is the first version of extracted texts.


---

## The Encyclopedia Britannica 11th Edition

The Encyclopædia Britannica was first published in Edinburgh between 1768 and 1771 and gradually evolved into one of the most authoritative reference works of the Western world. Over the centuries, it expanded through multiple editions, shifting from a concise digest to a sprawling scholarly enterprise by the early 20th century.

The 11th edition, published in 1910–1911, marked the peak of this effort. Spanning 29 volumes and roughly 30,000 printed pages, it contains around 40,000 articles written by over 1,500 contributors—many of them leading figures in their fields, including Bertrand Russell, T.H. Huxley, and Swinburne. It was the last edition compiled entirely in the United Kingdom before editorial control moved to the United States. The complete set was priced at $32 in 1911, equivalent to about $1,000 today.

By contrast, Wikipedia’s English edition now exceeds 6 million articles and an estimated 4 billion words. However, fewer than 10% of its contributors have formal training in the subjects they edit. While Wikipedia’s scale is orders of magnitude larger—nearly 100 times in terms of total word count—the number of curated, high-quality "featured articles" is only around 6,000. Viewed this way, EB11's achievement remains impressive: it concentrated expert-authored, editorially curated content into a durable print form with a quality and consistency that a decentralized model still rarely matches.

This makes EB11 not just a historical curiosity but a valuable counterpoint to Wikipedia, not only because many of the information contained is still valid or valuable, but also because where content and language did change, it presents an interesting framework for studying how language, authority, and framing have evolved over the past century.

---

## Extracted Text Database

Archive.org has [OCR scans of EB11](https://archive.org/details/encyclopedia-britannica-volume-14_202405/Encyclopedia%20Britannica%2C%20Volume%201/), which have been parsed into individual articles, and stored in a structured MySQL database (see schema.sql). Each article is embedded using a pre-trained sentence-transformers model, allowing semantic similarity comparisons within the corpus and against external texts.

Web UI: Live at [https://eb.kallisti.ch](https://eb.kallisti.ch)

#### Features

- Full-text search across articles
- Semantic similarity queries using vector embeddings
- Structured metadata and canonical titles

Due to the quality of the original OCR, the dataset includes formatting issues, occasional data loss, missing figures, tables, and footnotes, and makes contributor attribution difficult. These limitations are addressed further in the OCR section below.

---

## Evolution of Language and Framing Trends

We want to trace how knowledge changes—not only in content, but in tone, framing, and rhetorical posture. While shaped by the norms of its time, the EB11 articles are rarely obsolete in the sense that they are refuted, but rather merely incomplete from a more modern perspective.[^1] Language use and represented views have certainly changed as well, but likewise, the changes are rather subtle. To examine how much framing and subtext changes, we want to compare the EB11 articles to their modern Wikipedia counterparts and see which kind of articles exhibit the greatest cosine deviations over a common vector space.

### Semantic Drift

What is considered adequate vocabulary or desirable rhetoric has obviously changed, and it has changed with varying degrees and trends for different genres and social groups. EB11 offers a stable historical baseline for such comparison. The intuitive expectation is that articles on sexuality or imperial politics will drift more and that articles on integral algebra or ducks will be rather static in terms rhetoric and subtext, but this is yet to be tested. It is possible that a shift in editorial expectations and epistemic standards have changed encyclopedic language just as much as political changes or shifts of dominant views.  

To measure this, we embed Britannica and Wikipedia articles into the same semantic space using pre-trained transformer models such as all-MiniLM-L6-v2 or BGE-small-en. These sentence embedding models compress each article into a vector—typically 384 or 768 dimensions—that captures patterns of semantic usage: not only what is said, but how it is said. By comparing the cosine distance between matched articles, we can estimate how much a topic’s framing has changed.

### Fnords

Furthermore, for a qualitative assessment of how rhetoric framing shifts, we aim to identify *Fnords*—low-entropy linguistic units that aim to trigger a subconscious response in the audience irrelevant of what is being said, consisting of familiar combinations of words that operate through cliché, reduction and repetition. They are rarely domain-specific, but highly genre-specific. They are especially common in institutional, conspiratorial, polemical discourse or advertisement -- but they do creep in on medial frames and academic writing. 

As a unit of disinformation, it also corresponds to what Harry Frankfurt has identified as Bullshit in the epistemic sense:[^3] it contrasts from a lie in that whereas the lie is concerned with concealing the truth and must therefore have some regard for truthiness, bullshit culture corrodes epistemic standards as a whole through its complete disregard of meaning in favour of showmanship. When clustered, fnords then form what could be called a jargon of bullshit: a patterned set of phrasings, tonal cues and discursive habits that collectively define a rhetorical style concerned more with effect than accuracy.

To identify such fnordic dialects (e.g. "militaristic", "feminist", "bureaucratic"), we want to create fine-tuned vector spaces using highly polarizing, polemic, idiosyncratic text samples representative of a school of thought, political ideology or similar, and identify the archetypal patterns.

Using such embeddings, we can see on what axis a semantic drift has taken place.

### Data dumps

The Wikipedia data dumps are huge, so we can't have them in a repo. [Wikimedia](https://dumps.wikimedia.org/enwiki/latest/) is ultra slow in providing them, but the [Uni of Oslo has a great mirror server](https://ftp.acc.umu.se/mirror/) which has [2025 dumps](https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/), and an old one from 2010 can be found [on archive.org](https://archive.org/details/enwiki_20100408).

[^1]: See e.g. the article on the atom, which surprisingly contains almost no falsehoods and could still be considered a relevant read today, if not from the theoretical-physical but rather a historical and philosophical angle.
[^2]: E.g., articles about foreign geography or ethnology at times use language that would be considered inadequately colonial or Eurocentric today, but they very rarely advocate supremacist views or similar. Topics that are politically delicate today are approached with surprising finesse and a rather neutral tone considering the publication date, sometimes surprisingly modern in factual content and source selection. For example, note the beginning of the entry on *"WOMEN, The very word " woman " (O. Eng. wifmann), etymologically meaning a wife (or the wife division of the human race, the female of the species Homo), sums up a long history of dependence and subordination, from which the women of to-day have only gradually emancipated themselves in such parts of the world as come under "Western civilization."*
[^3]: On Bullshit, 1986, [archived](https://archive.org/details/on-bullshit-by-harry-frankfurt).

---

## OCR Reprocessing Plan

The available OCR text of EB11, although usable, suffers from significant layout misinterpretations. Major issues include:

- Two-column layouts being misread as single-column text
- Text below figures or tables being discarded
- Headings, lists, and formatting being inconsistently captured
- Tables and diagrams lost entirely or inserted incorrectly into text flow

To address this, we are developing an improved OCR pipeline using:

- Tesseract 5 with layout-aware configuration (`--psm 1`, TSV and hOCR output)
- Preprocessing steps using OpenCV: deskewing, denoising, contrast enhancement
- Markdown reconstruction based on block position, indentation, font size, and alignment
- Table detection using spatial heuristics and image snapshots (PNG) for fallback

The goal is to produce semantically faithful Markdown documents for each article, preserving the layout and formatting as close as possible to the original.

---

If you're interested in helping with:

- Re-OCR tuning and table extraction
- Wikipedia mapping and alignment
- Epistemic comparison methods
- Markdown generation from OCR data

…feel free to open an issue or pull request.

---

