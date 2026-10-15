"""Workshop 1: Python lists, NumPy arrays and a simple class."""

import numpy as np


# Q1: unlike list.index(), return every matching position.
def findarg(nums, num):
    results = []
    for index, value in enumerate(nums):
        if value == num:
            results.append(index)
    return results


# Q2: remember values already encountered, stopping at the first duplicate.
def has_duplicates(nums):
    seen = set()
    for value in nums:
        if value in seen:
            return True
        seen.add(value)
    return False


# Q5: average only the students who have a recorded mark.
class Module:
    def __init__(self, mod_name, student_ids, marks):
        self.mod_name = mod_name
        self.student_ids = list(student_ids)
        self.marks = dict(marks)
        if not set(self.marks).issubset(self.student_ids):
            raise ValueError("Marks must belong to students enrolled on the module.")

    def find_mark(self, student_id):
        # A missing mark raises KeyError: it must not silently become a zero.
        return self.marks[student_id]

    def average_mark(self):
        if not self.marks:
            raise ValueError("Cannot calculate an average without any marks.")
        return sum(self.marks.values()) / len(self.marks)


def main():
    list1 = [13, 45, 33, 67, 18, 56, 18, 67, 67]
    print("Q1: first occurrence:", list1.index(67))
    print("Q1: all occurrences:", findarg(list1, 67))
    print("Q1: missing value:", findarg(list1, 100))
    print("Q2: duplicates:", has_duplicates(list1))
    print("Q2: unique values:", has_duplicates([1, 2, 3]))
    print("Q2: empty list:", has_duplicates([]))

    # Q3: empty() allocates memory without initialising its contents.
    # Its displayed numbers are arbitrary, not guaranteed zeros.
    a1 = np.empty((3, 2), dtype=float)
    a2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    a3 = np.ones((3, 2))
    a4 = np.random.default_rng(42).random((2, 2))
    for name, array in [("a1 (uninitialised)", a1), ("a2", a2),
                        ("a3", a3), ("a4", a4)]:
        print(f"Q3: {name}:\n{array}")

    # Q4: shape gives the size along each axis; reshape preserves element count.
    print("Q4: vector shape:", np.array([1, 2, 3]).shape)
    print("Q4: matrix shape:", a2.shape)
    print("Q4: 3D array shape:", np.ones((2, 3, 4)).shape)
    print("Q4: first two rows:\n", a2[:2])
    print("Q4: second column:", a2[:, 1])
    print("Q4: top-left 2 by 2 block:\n", a2[:2, :2])
    print("Q4: one row of nine values:\n", a2.reshape(1, 9))
    print("Q4: one-dimensional vector:", a2.reshape(-1))

    module = Module("Deep Learning", [101, 102, 103], {101: 72, 102: 65, 103: 88})
    print("Q5: module:", module.mod_name)
    print("Q5: student 102's mark:", module.find_mark(102))
    print(f"Q5: average mark: {module.average_mark():.2f}")


if __name__ == "__main__":
    main()
