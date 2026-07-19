## Expected format

### Step 1: Raw TXT
Obtain a clean UTF-8 plain-text file (`.txt`) for each book. Remove OCR artifacts, fix obvious typos, and normalize punctuation. No markup is required at this stage — just clean, readable English text.

### Step 2: XML Annotation via Qwen2.5-Coder-14B-Instruct
The cleaned `.txt` is passed to `Qwen2.5-Coder-14B-Instruct` with a structured prompt that instructs the model to wrap the text in the following XML schema:

(Used Prompt: annotations/qwen_2.5_14b_coder_prompt_for_S_Sp.md)

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
</session>
```
Speaker values: Seth, Rob, Jane
Type values: statement, note, delivery, chapter_start

### Step 3: Verification
Annotated XML is spot-checked for tag consistency using DeepSeek as a second pass.

