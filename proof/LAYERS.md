# Layers (written in build order)

1. Done picture — RESULT.md exists and proves the goal was reverse-built.
2. Terminal test — file exists AND size > 80 bytes AND required headings present
3. Last act — write RESULT.md from gathered facts plus layer record
4. Preconditions
   - goal text is nonempty
   - layers object is complete
   - output directory exists and is writable
5. Gather
   - read --goal argument
   - confirm ROOT.mkdir succeeded
   - stamp UTC time
6. Intake — raw line -> one-sentence goal; if empty use 'prove backward construction'
