import numpy as np

list1 = [13, 45, 33, 67, 18, 56,18,67,67]
print(list1.index(67)) # this returns 3


# Q1
def findarg(nums, num):
    results = []

    for index, n in enumerate(nums):
        if n == num:
            results.append(index)

    return results

# Q2
def has_duplicates(nums):
    listset = set()

    for n in nums: 
        if n in listset:
            return True
        else:
            listset.add(n)

    return False

# Q3
a1 = np.empty((3,2), float)
a2 = np.array([[1,2,3],[4,5,6], [7,8,9]])
a3 = np.ones((3,2))
a4 = np.random.random((2,2))

print(a1)
print(a2)
print(a3)
print(a4)

# Q4
print(a2.shape) # shape


print(print(a2[0:2]))  # slicing


print(a2.reshape(1, 9)) # Reshaping

# Q5
class Module:
    def __init__(self, mod_name, student_ids, marks):
        self.mod_name = mod_name
        self.student_ids = student_ids
        self.marks = marks

    def find_mark(self, student_id):
        return self.marks[student_id]

    def average_mark(self):
        total = sum(self.marks.values())
        length = len(self.marks.values())
        return total / length

        