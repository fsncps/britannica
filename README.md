# Encyclopedia Britannica 11th Edition (1911) Clone

A public-domain preservation and transformation project. The aim is to make the *1911 Encyclopædia Britannica 11th edition* (EB11) fully accessible in modern formats: searchable, cleanly structured and analyzable. EB11 remains one of the most ambitious encyclopedic projects in history, but its text has never been systematically digitized and formatted. So far, we have recorded the availbale OCR data in a searchable DB, however, the text is only about 75% complete, and the tables and figures are missing. OCR reprocessing will be necessary with care to detail and modern tools.

**[HERE](https://eb.kallisti.ch)** is the first version of extracted texts.


---

## The Encyclopedia Britannica 11th Edition

The Encyclopædia Britannica was first published in Edinburgh between 1768 and 1771 and gradually evolved into one of the most authoritative reference works of the Western world. Over the centuries, it expanded through multiple editions, shifting from a concise digest to a sprawling scholarly enterprise by the early 20th century.

The 11th edition, published in 1910–1911, marked the peak of this effort. Spanning 29 volumes and roughly 30,000 printed pages, it contains around 40,000 articles written by over 1,500 contributors—many of them leading figures in their fields, including Bertrand Russell, T.H. Huxley, and Swinburne. It was the last edition compiled entirely in the United Kingdom before editorial control moved to the United States. The complete set was priced at $32 in 1911, equivalent to about $1,000 today.

By contrast, Wikipedia’s English edition now exceeds 6 million articles and an estimated 4 billion words. However, fewer than 10% of its contributors have formal training in the subjects they edit. While Wikipedia’s scale is orders of magnitude larger—nearly 100 times in terms of total word count—the number of curated, high-quality "featured articles" is only around 6,000. Viewed this way, EB11's achievement remains impressive: it concentrated expert-authored, editorially curated content into a durable print form with a quality and consistency that a decentralized model still rarely matches.

This makes EB11 not just a historical curiosity but a valuable counterpoint to Wikipedia, not only because many of the information contained is still valid or valuable, but also because where content and language did change, it presents an interesting framework for studying how language, authority and medial framing have evolved over the past century.

---

## Extracted Text Database

Archive.org has [OCR scans of EB11](https://archive.org/details/encyclopedia-britannica-volume-14_202405/Encyclopedia%20Britannica%2C%20Volume%201/), which have been parsed into individual articles, and stored in a structured MySQL database (see schema.sql). Each article is embedded using a pre-trained sentence-transformers model, allowing semantic similarity comparisons within the corpus and against external texts.

Web UI: Prototype live at [https://eb.kallisti.ch](https://eb.kallisti.ch)

#### Features

- Full-text search across articles
- Semantic similarity queries using vector embeddings
- Structured metadata and canonical titles

#### TODO

- Rescan OCR: Due to the quality of the original OCR, the dataset includes formatting issues, occasional data loss, missing figures, tables, and footnotes, and makes contributor attribution difficult (See OCR section below)
- Wiki-style links: Create cross-references with links throughout the articles DB
- Reference authors and contributors per article
- Embed into vector space for similarity search

---

## OCR Reprocessing Plan

The currently available OCR output from EB11 volumes, while usable for basic extraction, suffers from serious structural flaws. The underlying scans are high-quality, but the automated text recognition—mostly performed years ago using generic settings—fails to capture much of the document’s original layout. The two-column format typical of EB11 is frequently misread as a continuous single column. Figures, tables and captions are often misplaced or omitted entirely. Headings, list formatting, footnotes and contributor attributions are inconsistently captured, and in some cases dropped altogether. This results in articles that are legible but structurally degraded, limiting both readability and recoverability.

To address this, we are developing an improved OCR and post-processing pipeline with the goal of reconstructing each article as a clean Markdown document that mirrors the original formatting as closely as possible.

The pipeline includes:

- Tesseract 5, with layout-aware page segmentation (--psm 1) and output in TSV or hOCR format
- OpenCV-based preprocessing, including deskewing, denoising, and contrast adjustment
- Markdown reconstruction, based on visual layout features such as block alignment, indentation, font size, and heading placement
- Table recognition and fallback, using spatial heuristics to extract simple tables or retain complex ones as embedded image snapshots
- Create heading anchors in pdfs for precise linking

The aim is not just to improve text quality, but to recover the visual and semantic structure of the original printed encyclopedia in a portable, structured form.

---

## Evolution of Language and Framing Trends (a possible extra)

While shaped by the norms of its time, the EB11 articles are rarely obsolete in the sense that they are refuted, but rather merely incomplete from a more modern perspective.[^1] Language use and represented views have certainly changed as well, but likewise, the changes are rather subtle.[^2] To examine how much framing and subtext changes, we want to compare the EB11 articles to their modern Wikipedia counterparts and see which kind of articles exhibit the greatest cosine deviations over a common vector space.

### Semantic Drift

What is considered adequate vocabulary or desirable rhetoric has obviously changed, and it has changed with varying degrees and trends for different genres and social groups. EB11 offers a stable historical baseline for such comparison. The intuitive expectation is that articles on sexuality or imperial politics will drift more and that articles on integral algebra or ducks will be rather static in terms rhetoric and subtext, but this is yet to be tested. It is possible that a shift in editorial expectations and epistemic standards have changed encyclopedic language just as much as political changes or shifts of dominant views.  

To measure this, the plan here is to embed Britannica and Wikipedia articles into the same semantic space using pre-trained transformer models such as all-MiniLM-L6-v2 or BGE-small-en. These sentence embedding models compress each article into a vector that captures patterns of semantic usage. By comparing the cosine distance between matched articles, we can estimate how much a topic’s framing has changed.

### Fnords

Next, this makes it possible to identify *Fnords*—low-entropy linguistic units that aim to trigger a subconscious response in the audience irrelevant of what is being said, consisting of familiar combinations of words that operate through cliché, reduction and repetition. They are rarely domain-specific, but highly genre-specific. They are especially common in institutional, conspiratorial, polemical discourse or advertisement -- but they do creep in on medial frames and academic writing.[^3] 

Clustering of certain types of these patterns could identify a sort of fnordic dialect (e.g. "militaristic", "postmodern", "bureaucratic"). To benchmark, a possible approach could be to create fine-tuned vector spaces using highly polarizing, polemic, idiosyncratic text samples representative of a school of thought, political ideology or similar, and identify the archetypal patterns. The fnordic embedding could then show on what axis a semantic drift has taken place.

### Data dumps

The Wikipedia data dumps are huge, so we can't have them in a repo. [Wikimedia](https://dumps.wikimedia.org/enwiki/latest/) is ultra slow in providing them, but the [Uni of Oslo has a great mirror server](https://ftp.acc.umu.se/mirror/) which has [2025 dumps](https://ftp.acc.umu.se/mirror/wikimedia.org/dumps/enwiki/), and an old one from 2010 can be found [on archive.org](https://archive.org/details/enwiki_20100408).

[^1]: See e.g. the article on the atom, which surprisingly contains almost no falsehoods and could still be considered a relevant read today, if not from the theoretical-physical but rather a historical and philosophical angle.
[^2]: E.g., articles about foreign geography or ethnology at times use language that would be considered inadequately colonial or Eurocentric today, but they very rarely advocate supremacist views or similar. Some topics considered politically delicate today are and a rather neutral tone considering the publication date.
[^3]: As a unit of disinformation, it also corresponds to what Harry Frankfurt has identified as Bullshit in the epistemic sense: it contrasts from a lie in that whereas the lie is concerned with concealing the truth and must therefore have some regard for truthiness, bullshit culture corrodes epistemic standards as a whole through its complete disregard of meaning in favour of showmanship. When clustered, fnords then form what could be called a jargon of bullshit: a patterned set of phrasings, tonal cues and discursive habits that collectively define a rhetorical style concerned more with effect than accuracy. (On Bullshit, 1986, [archived](https://archive.org/details/on-bullshit-by-harry-frankfurt).)

---


## Contributions welcome!

If you're interested in contributing anything, feel free to open an issue or pull request.

---

