"""Reading and changing the expenses CSV, kept apart from the GUI so it can be tested."""

import os

import pandas as pd

type StrPath = str | os.PathLike[str]

COLUMNS = ["Date", "Category", "Amount", "Description"]


def reset(path: StrPath) -> None:
    """Replace the file with an empty one that has only the header row."""
    pd.DataFrame(columns=COLUMNS).to_csv(path, index=False)


def ensure(path: StrPath) -> None:
    """Create the file if it is missing, or reset it if its columns are wrong."""
    if not os.path.exists(path):
        reset(path)
        return
    if not set(COLUMNS).issubset(pd.read_csv(path).columns):
        reset(path)


def load(path: StrPath) -> pd.DataFrame:
    """All expenses, read as text so a description like "100" stays a string."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def drop_row(path: StrPath, row: int) -> pd.DataFrame:
    """Delete exactly one expense, by its row number in the file.

    Matching on the row's values instead would delete every identical row
    (two "£2.00 Taxi" entries on the same day would both go).
    """
    df = load(path)
    df = df.drop(index=row).reset_index(drop=True)
    df.to_csv(path, index=False)
    return df
