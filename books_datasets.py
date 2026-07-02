import kagglehub
import pandas as pd
import os

# Download latest version
path = kagglehub.dataset_download("lokeshparab/gutenberg-books-and-metadata-2025")

print("Path to dataset files:", path)

# Looking inside the dataset
metadata_path = os.path.join(path, "gutenberg_metadata.csv")
df = pd.read_csv(metadata_path, )

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())


def get_books(df):
    eng_books = df[
        (df['Language'] == 'en') &
        (df['Type'] == 'Text')
        ]

    books = filter_subjects(eng_books)


def filter_subjects(books):
    desired_subj = ["fiction", "romance", "horror", "fantasy"]
    desired_subj = [des_subj[0:4] for des_subj in desired_subj]
    desired_books = []

    for subject in books["Subjects"]:
        if isinstance(subject, float):
            continue

        valid = [subj for subj in subject.split()
                 if subj.lower()[:4] in desired_subj]
        if valid:
            desired_books.append(books)

    return desired_books


get_books(df)
