# Encyclopedia Britannica 11th Edition (1911) Clone

A public-domain preservation and transformation project.

This project aims to make the *1911 Encyclopædia Britannica* (EB11) fully accessible in modern formats: searchable, cleanly structured, and analyzable. EB11 remains one of the most ambitious encyclopedic projects in history, but its text has never been systematically corrected or semantically indexed.

Alongside creating a modern reading experience, the project aims to **analyze epistemic and rhetorical shifts** by comparing EB11 articles to their modern Wikipedia counterparts using **semantic similarity**, tone, and linguistic framing.

---

## The Encyclopedia Britannica 11th Edition

The Encyclopædia Britannica was first published in Edinburgh between 1768 and 1771 and gradually evolved into one of the most authoritative reference works of the Western world. Over the centuries, it expanded through multiple editions, shifting from a concise digest to a sprawling scholarly enterprise by the early 20th century.

The 11th edition, published in 1910–1911, marked the peak of this effort. Spanning 29 volumes and roughly 30,000 printed pages, it contains around 40,000 articles written by over 1,500 contributors—many of them leading figures in their fields, including Bertrand Russell, T.H. Huxley, and Swinburne. It was the last edition compiled entirely in the United Kingdom before editorial control moved to the United States. The complete set was priced at $32 in 1911, equivalent to about $1,000 today, making it a major investment for middle-class households. In terms of scale, the full text comes to approximately 250–300 MB of raw OCR, or around 50 million words.

By contrast, Wikipedia’s English edition now exceeds 6 million articles and an estimated 4 billion words. However, fewer than 10% of its contributors have formal training in the subjects they edit. While Wikipedia’s scale is orders of magnitude larger—nearly 100 times in terms of total word count—the number of curated, high-quality "featured articles" is only around 6,000. Viewed this way, EB11's achievement remains impressive: it concentrated expert-authored, editorially curated content into a durable print form with a quality and consistency that a decentralized model still rarely matches.

This makes the 11th edition not just a historical curiosity but a valuable counterpoint to Wikipedia—useful for studying how language, authority, and framing have evolved over the past century.

---

## Extracted Text Database

### Current Pipeline

- Source: OCR text from archive.org scans of EB11 volumes
- Cleaning: Articles segmented and reconstructed using a custom parser
- Database: MySQL (schema included in `schema.sql`)
- Embeddings: Each article is vectorized using `sentence-transformers` for semantic similarity
- Web UI: Live at [https://eb.kallisti.ch](https://eb.kallisti.ch)

### Features

- Full-text search across articles
- Semantic similarity queries using vector embeddings
- Structured metadata and canonical titles

---

## Wikipedia Similarity Vectors (planned)

This part of the project compares the **rhetoric and epistemic framing** of 1911 EB articles with their modern-day Wikipedia equivalents.

### Semantic Drift

This project aims to trace how knowledge changes—not only in content, but in tone, framing, and rhetorical posture. The 1911 Encyclopædia Britannica offers a stable historical baseline for such comparison. While shaped by the norms of its time, its entries are rarely factually wrong; more often, they are incomplete or silent on developments that became central later. Even in controversial domains, the tone is often measured, occasionally imperial in framing but seldom polemical.

We hypothesize that changes in language reflect not just advances in knowledge but shifting institutional norms and rhetorical expectations. Over the past century, we expect topics such as race, gender, or empire to exhibit strong semantic drift, while fields like mathematics or classical physics may remain linguistically stable.

To measure this, we embed Britannica and Wikipedia articles into the same semantic space using pre-trained transformer models such as all-MiniLM-L6-v2 or BGE-small-en. These sentence embedding models compress each article into a vector—typically 384 or 768 dimensions—that captures patterns of semantic usage: not only what is said, but how it is said. By comparing the cosine distance between matched articles, we can estimate how much a topic’s framing has changed.

### Fnords

Furthermore, for a qualitative assessment of how rhetoric framing shifts, we aim to identify *Fnords*—low-entropy linguistic units that aim to trigger a subconcious response in the audience irrelevant of what is being said, consisting of familiar combinations of words that rarely surprise the reader, often operating through cliché, emphasis, or repetition. They are rarely domain-specific, but are highly genre-specific—especially common in institutional, conspiratorial, polemical, or promotional discourse. 

They are a unit of misinformation, also corresponding to what Harry Frankfurt identifies as Bullshit in the epistemic sense (On Bullshit, 1986). When clustered, fnords form what could be called a certain  jargon of bullshit: a patterned set of phrasings, tonal cues, and discursive habits that collectively define a rhetorical style concerned more with effect than accuracy.

To identify such fnordic dialects (e.g. "militaristic", "postmodern", "feminist", "colonialistic", "bueraucratic"), we want to create fine-tuned vector spaces using highly polarizing, polemic, idiosyncratic text samples representative of a school of thought, political ideology or similar, and identify the archetypal patterns.

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

