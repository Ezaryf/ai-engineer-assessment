# High-Level Design: Long Document Summarization (English & Malay)

**Goal:**
Produce faithful, fluent summaries in English and Malay, handling code-switching and domain-specific content.

We cover:

1. Preprocessing
2. Multilingual & code-switching handling
3. Summarization approach
4. Evaluation of summary quality

## 1) Preprocessing Steps

**Ingest & Canonicalize**
- Extract text, OCR if needed.

**Language Detection**
- Per-document and per-chunk.
- Tools: `langdetect` or lightweight transformer-based detectors.

**Normalize Text**
- Fix encoding, unify quotes, normalize whitespace.
- Handle abbreviations.
- Remove navigation, headers or footers, boilerplate.

**Sentence Segmentation & Tokenization**
- Use tokenizer supporting Malay.
- Subword tokenizers recommended for multilingual robustness.

**Chunking or Hierarchical Segmentation**
- Chunks: 500–1,500 tokens with overlap.
- Metadata: language, section headers, page numbers.

**Handling Tables & Figures**
- Extract tables to structured format or convert to text-friendly representation.
- Summarize separately if needed.

**Detect & Tag Code-Switching**
- Chunk-level detection of mixed language spans (e.g., `[EN]`, `[MS]`).

**Pre-summarization Cleaning**
- Remove repeated disclaimers, legalese, or long lists that can be compressed.