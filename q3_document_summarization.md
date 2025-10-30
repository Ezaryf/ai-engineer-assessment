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


## 2) Multilingual & Code-Switching Handling

**Options:**

1. **Multilingual Model Approach (Preferred)**
 - Single multilingual seq2seq model: mT5, mBART-50, instruction-tuned multilingual LLM.
 - Tag input with language hints (`#lang:ms`, `#lang:en`, `#lang:mix`).

2. **Translate-then-Summarize**
 - Translate Malay → English (or vice versa), summarize, optionally translate back.
 - Adds fidelity risk and latency.

3. **Language-Aware Pipeline**
 - Route chunks to language-specific summarizers, then merge outputs.

**Handling Code-Switching**
- Keep mixed chunks intact using multilingual model trained on code-switched data.
- Alternatively: split by language, summarize each, then merge.


## 3) Summarization Approach: Extractive vs Abstractive & Model Choice

**Tradeoffs**

| Approach | Pros| Cons|
|-----------|-----------------------------|-------------------------------|
| Extractive | Faithful, less hallucination, faster | Disjointed, less compression |
| Abstractive | Fluent, can synthesize & compress | Risk of hallucination |

**Practical Hybrid Pipeline**
1. **Extractive Pruning:** Select relevant chunks (TF-IDF).
2. **Chunk Summarization (Abstractive):** Run abstractive summarizer per chunk.
3. **Hierarchical Summarization:** Merge chunk summaries into coherent document-level summary.
4. **Factuality Check:** Run factuality check and fallback to extractive if flagged.

**Model Choices**

- **Open-source seq2seq:** mT5, mBART-50, BART.
- **Instruction-tuned LLMs:** GPT-family, Claude, Llama.
- **Small & Fast:** DistilBART or distilled seq2seq for on-device low-latency needs.


## 4) Ensuring Fidelity, Accuracy & Evaluation

**Factuality & Hallucination Checks**
Use automated verification based on:
1. Extractive QA
2. NLI/entailment models
3. **Entity consistency:**
   - Names
   - Dates
   - Numbers
   - Product codes

**Quality Metrics**
1. **Automatic:**
   - ROUGE-L (overlap with reference)
   - BERTScore (semantic similarity)
   - QAGS/FEQA (factual consistency)

2. **Human evaluation:**
   - Fluency (English + Malay)
   - Coverage (does it include main points?)
   - Conciseness
   - Factuality
   - Readability

**Production Monitoring**
- User feedback: “Helpful?” / “Report inaccurate summary.”
- Drift detection (changes in language distribution or content).
- Human spot checks on random samples.
- Logging summaries + source chunks for auditing.