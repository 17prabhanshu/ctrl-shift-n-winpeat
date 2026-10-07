# NLP Benchmark Results

## Evaluation against 50 manually mapped skills

- **Level 1 (Exact Match):** Accuracy = 68.00%
- **Level 2 (TF-IDF Similarity):** Accuracy = 66.00%
- **Level 3 (N-gram Matching):** Accuracy = 48.00%

### Observations
- Exact matching works well for taxonomy keywords but fails for variations.
- TF-IDF depends on overlap; short phrases can be tricky.
- N-gram/substring matching captures variations like 'python programming' -> 'python' but can introduce false positives.
