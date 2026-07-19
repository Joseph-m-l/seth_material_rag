# Data Preparation Guide

Source texts are not hosted in this repository due to copyright restrictions.

## How to reproduce

1. Obtain legal copies of the Seth Material by Jane Roberts:
   - *Seth Speaks: The Eternal Validity of the Soul*
   - *The Nature of Personal Reality*
   - (Additional books as they are added to the pipeline)

2. Place cleaned plain-text (`.txt`) files in this directory using the naming convention below.

3. Run the preprocessing and indexing scripts from `/retrieval` (when available):

python retrieval/build_index.py --input corpus/ --output chroma_db/


## Expected format

### Step 1: Raw TXT
Obtain a clean UTF-8 plain-text file (`.txt`) for each book. Remove OCR artifacts, fix obvious typos, and normalize punctuation. No markup is required at this stage — just clean, readable English text.

### Step 2: XML Annotation via Qwen2.5-Coder-14B-Instruct
The cleaned `.txt` is passed to `Qwen2.5-Coder-14B-Instruct` with a structured prompt that instructs the model to wrap the text in the following XML schema:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<session book="Seth Speaks" session_number="SESSION 511" date="JANUARY 21, 1970">
<meta>
 <session_number>SESSION 511</session_number>
 <date>JANUARY 21, 1970</date>
</meta>
<dialogue>
 <utterance speaker="Seth" type="statement">
   <text>Now: I bid you, Joseph, a good evening.</text>
 </utterance>
 <utterance speaker="Rob" type="note">
   <text>(9:10 P.M. WEDNESDAY)</text>
 </utterance>
 <utterance speaker="Seth" type="delivery">
   <text>(Smile.)</text>
 </utterance>
 <utterance speaker="Seth" type="chapter_start" chapter="1">
   <text>Chapter One</text>
 </utterance>
</dialogue>
</session>
```
Speaker values: Seth, Rob, Jane
Type values: statement, note, delivery, chapter_start

Step 3: Verification
Annotated XML is spot-checked for tag consistency using DeepSeek as a second pass.

Annotation prompt
The exact prompt used for Qwen2.5-Coder is available in annotations/prompt.md.

Currently indexed in ChromaDB
Seth Speaks, Part One — Chapters 1–9 (Sessions 511–537, personal sessions excluded):

Chapter 1: I Do Not Have a Physical Body, Yet I Am Writing This Book

Chapter 2: My Present Environment, Work, and Activities

Chapter 3: My Work and Those Dimensions of Reality Into Which It Takes Me

Chapter 4: Reincarnational Dramas

Chapter 5: How Thoughts Form Matter — Coordination Points

Chapter 6: The Soul and the Nature of Its Perception

Chapter 7: The Potentials of the Soul

Chapter 8: Sleep, Dreams, and Consciousness

Chapter 9: The "Death" Experience

More chapters will be added as processing continues.

Notes
Personal sessions (non-Seth, private material) are excluded from the indexed corpus.

All annotations and chunking respect speaker boundaries: only SETH segments are indexed for retrieval.

For questions about the data preparation process, open an issue in this repository.

