import store


def write(path, rows):
    path.write_text("Date,Category,Amount,Description\n" + "".join(r + "\n" for r in rows), encoding="utf-8")


def test_reset_empties_an_existing_file(tmp_path):
    # Before the fix "Delete All Expenses" left an existing file untouched.
    f = tmp_path / "expenses.csv"
    write(f, ["2024-08-25,Transport,£2.00,Taxi", "2024-08-25,Food,£10.00,Takeaway"])
    store.reset(f)
    assert store.load(f).empty
    assert list(store.load(f).columns) == store.COLUMNS


def test_drop_row_removes_only_the_selected_duplicate(tmp_path):
    # Before the fix both identical rows were deleted.
    f = tmp_path / "expenses.csv"
    write(f, ["2024-08-25,Transport,£2.00,Taxi", "2024-08-25,Transport,£2.00,Taxi", "2024-08-26,Food,£5.00,100"])
    df = store.drop_row(f, 0)
    assert len(df) == 2
    assert df.iloc[0]["Description"] == "Taxi"
    assert df.iloc[1]["Description"] == "100"  # a numeric description stays text


def test_ensure_creates_missing_file_and_repairs_bad_columns(tmp_path):
    f = tmp_path / "new.csv"
    store.ensure(f)
    assert list(store.load(f).columns) == store.COLUMNS
    f.write_text("a,b\n1,2\n", encoding="utf-8")
    store.ensure(f)
    assert store.load(f).empty
