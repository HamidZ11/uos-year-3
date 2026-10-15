# Week 1 · Python & NumPy

**Quick reference** · Lists, arrays and a first class

[All weeks](../README.md) · [Python exercises](wk1.py) · [Workshop sheet](DL%20Workshop%201.pdf) · [Next: perceptrons →](../wk2/REFERENCE.md)

---

> **The idea:** get comfortable representing data, finding values and grouping related data with behaviour.

## 01 · What was covered

| Concept | What to remember |
|---|---|
| Lists | Ordered values; positions start at **0**. `list.index(value)` finds only the first match. |
| `enumerate()` | Gives both the position and value while looping. Useful for finding **every** matching position. |
| Sets | Store distinct values. Remember previously seen values to detect a duplicate. |
| Dictionaries | Map a key to a value: `marks[student_id]` retrieves that student's mark. |
| NumPy arrays | Represent numerical data with a shape and a data type. |
| Classes | Keep related data and methods together. `__init__` initialises an instance; `self` refers to that instance. |

## 02 · Array patterns

```python
a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

a.shape          # (3, 3): three rows, three columns
a[:2]            # first two rows; the stop position is excluded
a[:, 1]          # second column: [2, 5, 8]
a[:2, :2]        # top-left 2 × 2 block
a.reshape(1, 9)  # one row, nine columns
a.reshape(-1)    # a one-dimensional array of nine values
```

| Create an array | Meaning |
|---|---|
| `np.empty((3, 2))` | Allocates space without initialising the values. |
| `np.ones((3, 2))` | Three rows and two columns, filled with ones. |
| `np.random.default_rng(42).random((2, 2))` | A repeatable 2 × 2 sample of values in `[0, 1)`. |

**Shape is a tuple of axis sizes.** `(9,)`, `(1, 9)` and `(3, 3)` all contain nine values but describe different arrangements.

## 03 · The `Module` class

```python
module = Module("Deep Learning", [101, 102], {101: 72, 102: 88})
module.find_mark(101)  # 72
module.average_mark() # 80.0
```

The instance holds the module name, enrolled student IDs and a dictionary of recorded marks. The average is `sum(marks) / number_of_recorded_marks`; an unmarked student is not automatically assigned zero.

## 04 · Watch for

- **`np.empty` does not mean zeros.** Its displayed values are arbitrary until assigned.
- **Reshaping preserves the number of values.** Nine values cannot become a 2 × 5 array.
- **Missing is different from zero.** A missing mark raises `KeyError`; averaging no marks raises `ValueError` in this implementation.
- **Print once.** `print(print(value))` prints the value followed by `None`.

---

**Run from the workshops folder:** `python wk1/wk1.py`
