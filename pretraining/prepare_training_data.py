import json
import os
import random
import tiktoken

books_folder = "extracted_books"
train_count = 0
valid_count = 0
VALIDATION_SPLIT = 0.10

# Target model token limit (e.g., 2048 or 4096)
# Subtract a buffer for your "You are MorpheusAI..." system prompt
MAX_TOKENS = 1800
MIN_TOKENS = 1000  # Skip tiny trailing fragments

# Initialize tokenizer (cl100k_base is used by GPT-3.5/GPT-4)
tokenizer = tiktoken.get_encoding("cl100k_base")

print("Starting processing...")

train_file = open("../data/train.jsonl", "w", encoding="utf-8")
valid_file = open("valid.jsonl", "w", encoding="utf-8")

for filename in os.listdir(books_folder):
    try:
        book_path = os.path.join(books_folder, filename)
        with open(book_path, "r", encoding="utf-8") as book:
            text = book.read()

        # [Your existing Gutenberg header removal code goes here]
        if "Project Gutenberg" in text:
            start = text.find("CHAPTER")
            if start == -1:
                start = text.find("*** START OF THIS PROJECT GUTENBERG")
                if start != -1:
                    start = text.find("\n", start) + 1
            if start != -1:
                text = text[start:]

        # Tokenize the entire book text at once
        book_tokens = tokenizer.encode(text)

        # Chunk based on token length instead of character length
        for i in range(0, len(book_tokens), MAX_TOKENS):
            chunk_tokens = book_tokens[i:i + MAX_TOKENS]

            if len(chunk_tokens) < MIN_TOKENS:
                continue

            # Decode tokens back to a clean string
            chunk_text = tokenizer.decode(chunk_tokens).strip()

            entry = {
                "text": f"You are MorpheusAI, a masterful immersive storyteller.\n\n{chunk_text}"
            }
            json_line = json.dumps(entry, ensure_ascii=False) + "\n"

            if random.random() > VALIDATION_SPLIT:
                train_file.write(json_line)
                train_count += 1
            else:
                valid_file.write(json_line)
                valid_count += 1

    except Exception as e:
        print(f"Error processing {filename}: {e}")
        continue

train_file.close()
valid_file.close()

print(f"\nFinished! Train: {train_count}, Valid: {valid_count}")