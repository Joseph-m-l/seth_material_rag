# Data Preparation Guide

Source texts are not hosted in this repository due to copyright restrictions.

## How to reproduce

Obtain legal copies of the Seth Material by Jane Roberts:
   - *Seth Speaks: The Eternal Validity of the Soul*
   - (Additional books as they are added to the pipeline)


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
Speaker values: Seth, Rob, Jane, etc
Type values: statement, note, delivery, chapter_start

### Step 3: Verification
Annotated XML is spot-checked for tag consistency using DeepSeek as a second pass.

Annotation prompt
The exact prompt used for Qwen2.5-Coder is available in annotations/qwen_2.5_coder_prompt_for_S_Sp.md

### Currently indexed in ChromaDB:

Book: Seth Speak

Chapter 1: I Do Not Have a Physical Body, Yet I Am Writing This Book 
Chapter 2: My Present Environment, Work, and Activities
Chapter 3: My Work and Those Dimensions of Reality Into Which It Takes Me 
Chapter 4: Reincarnational Dramas
Chapter 5: How Thoughts Form Matter — Coordination Points 
Chapter 6: The Soul and the Nature of Its Perception
Chapter 7: The Potentials of the Soul
Chapter 8: Sleep, Dreams, and Consciousness
Chapter 9: The “Death” Experience
Chapter 10: “Death” Conditions in Life
Chapter 11: After-Death Choices and the Mechanics of Transition 
Chapter 12: Reincarnational Relationships
Chapter 13: Reincarnation, Dreams, and the Hidden Male and Female Within the Self 
Chapter 14: Stories of the Beginning, and the Multidimensional God 
Chapter 15: Reincarnational Civilizations, Probabilities, and More on the Multidimensional God 
Chapter 16: Probable Systems, Men, and Gods
Chapter 17: Probabilities, the Nature of Good and Evil, and Religious Symbolism 
Chapter 18: Various Stages of Consciousness, Symbolism, and Multiple Focus 
Chapter 19: Alternate Presents and Multiple Focus
Chapter 20: Questions and Answers
Chapter 21: The Meaning of Religion
Chapter 22: A Goodbye and an Introduction: Aspects of Multidimensional Personality as Viewed Through My Own Experience

All annotations and chunking respect speaker boundaries: only SETH segments are indexed for retrieval.

## Pre-built index

A pre-built ChromaDB index for *"Seth Speaks"* is available in `/chroma_db_v2/`.
This index contains vector embeddings only — the original text cannot be reconstructed from it.



For questions about the data preparation process, open an issue in this repository.

