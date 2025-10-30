# High-Level Design: Searchable Knowledge-Base Chatbot (Customer Support)

**Goal:**
You need to build a searchable knowledge base chatbot for customer support using an LLM.

We will cover:

1. Document ingestion pipeline
2. Storage and retrieval
3. Ensuring accuracy & latency


## 1) Ingest Documents

**Input types:**
PDFs, DOCX, HTML pages, Markdown, email archives, databases, FAQs.

### Steps

#### Fetch & Canonicalize
- Connectors for sources: S3, SharePoint, Confluence, Git repos.
- Normalize to plain text + metadata (title, author, date, source, URL).
- OCR (for scanned docs):
  - Use Tesseract or commercial OCR if quality matters.
  - Keep original image and text confidence.

#### Clean & Preprocess
- Remove boilerplate (headers or footers), deduplicate, normalize whitespace, fix encoding.
- Remove or mark PII.

#### Segment
- Chunk into semantic windows (500–1,500 tokens) with overlaps (50–200 tokens) to retain context.
- Keep chunk-level metadata linking back to original document and location.

#### Language Detection
- Detect language per document and per chunk (useful for multilingual corporate).

#### Embeddings
- Compute vector embeddings for each chunk using semantic embedding models.
- Store embedding length, token count, model version in metadata.

#### Indexing
- Insert vectors + metadata into vector DB (Pinecone).

#### Quality & Deduplication
- Semantic deduplication to remove redundant chunks.


## 2) Store and Retrieve Efficiently

### Data Stores
- **Vector DB:** embeddings and similarity search.
- **Metadata store:** RDBMS or document DB for canonical docs, audit trail, and filters.
- **Cache:** Redis for hot queries & answer caching.

### Vector DB Considerations
- Scale & feature requirements: on-prem vs managed (FAISS, Pinecone).
- Support approximate nearest neighbor (ANN), persistence, replication, and metadata filtering.
- Version embeddings to handle model updates.

### Retrieval Approach
- Hybrid scoring: semantic similarity + lexical matching (BM25) for factual accuracy.
- Metadata filters: date range, product ID, language, doc type.
- **Reranker:** After top N ANN retrieval (e.g., 50), use cross-encoder reranker to select top K.
- **Chunk aggregation:** Merge retrieved chunks from same document region for coherent context.

### Performance
- ANN + small top_k + cross-encoder reranker balances speed and quality.
- Cache results for frequent queries; precompute popular query embeddings.
- Batch embedding computations.


## 3) Ensure Fast and Accurate Answers

### Answering Strategy (RAG Pattern)
1. Retrieve top K chunks with metadata (vector DB + optional BM25).
2. Rerank candidates with cross-encoder.
3. Assemble context: concatenate best chunks up to token budget; include citations (doc title + link + location).
4. Generate answer: feed context + user query into LLM with prompt template:
   - "Answer **only** from context"
   - Cite sources
   - Say “I don’t know” when answer is absent

### Post-Processing
- Extract & format citations.
- Apply safety or policy filters.
- Optionally perform factual consistency checks.

### Mitigate Hallucinations
- Constrain generator prompt: “Only use the documents provided in CONTEXT. If answer is not in context, respond: ‘I don’t know’.”
- Verifiability checks: secondary QA with extractive QA model.
- Confidence score: derived from retrieval + model certainty.

### UX: Citations & Traceability
- Return short answer + cited documents/chunk locations with links & confidence.
- “Show source” or “show full context” options.