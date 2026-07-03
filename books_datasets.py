from fileinput import close

import kagglehub
import pandas as pd
import os
import shutil

# Download latest version
path = kagglehub.dataset_download("lokeshparab/gutenberg-books-and-metadata-2025")

print("Path to dataset files:", path)

# Looking inside the dataset
metadata_path = os.path.join(path, "gutenberg_metadata.csv")
df = pd.read_csv(metadata_path, )

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())


def extract_desired_books(df, book_dir_path):
    desired_books = []

    new_dir = "extracted_books"
    curr_dir = "/Users/kelanwestwood/Desktop/Education/University/MorpheusAI"

    book_dir = os.listdir(book_dir_path)

    eng_books = df[
        (df['Language'] == 'en') &
        (df['Type'] == 'Text')
        ]
    book_ids = filter_subjects(eng_books)

    for book_id in book_dir:
        if int(book_id) in book_ids:
            book_path = f"{book_dir_path}/{book_id}"
            os.makedirs(f"{curr_dir}/{new_dir}", exist_ok=True)

            shutil.copyfile(
                src=book_path,
                dst=f"{curr_dir}/{new_dir}/{book_id}"
            )


def filter_subjects(books):
    desired_subj = ["fiction", "romance", "horror", "fantasy"]
    desired_subj = [des_subj[0:4] for des_subj in desired_subj]
    desired_books = []

    for text_id, subject in enumerate(books["Subjects"]):
        if isinstance(subject, float):
            continue

        valid = [subj for subj in subject.split()
                 if subj.lower()[:4] in desired_subj]
        if valid:
            desired_books.append(text_id)

    return desired_books


book_dir = f"{path}/books"

extract_desired_books(df, book_dir)
