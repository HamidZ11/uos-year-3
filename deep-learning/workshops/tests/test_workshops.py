"""Small regression checks for the hand-written workshop code."""

import unittest

import numpy as np

from wk1.wk1 import Module, findarg, has_duplicates
from wk2.perceptron_DL import Perceptron


class PythonExercisesTests(unittest.TestCase):
    def test_find_all_occurrences_and_missing_value(self):
        self.assertEqual(findarg([13, 45, 33, 67, 18, 56, 18, 67, 67], 67), [3, 7, 8])
        self.assertEqual(findarg([1, 2], 3), [])
        self.assertEqual(findarg([], 1), [])

    def test_duplicates(self):
        self.assertTrue(has_duplicates([1, 2, 1]))
        self.assertFalse(has_duplicates([1, 2, 3]))
        self.assertFalse(has_duplicates([]))

    def test_marks_and_average_exclude_unmarked_students(self):
        module = Module("DL", [1, 2, 3], {1: 60, 2: 80})
        self.assertEqual(module.find_mark(1), 60)
        self.assertEqual(module.average_mark(), 70)
        with self.assertRaises(KeyError):
            module.find_mark(3)

    def test_empty_marks_and_unenrolled_students(self):
        with self.assertRaises(ValueError):
            Module("DL", [], {}).average_mark()
        with self.assertRaises(ValueError):
            Module("DL", [1], {2: 75})


class PerceptronTests(unittest.TestCase):
    def setUp(self):
        self.x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

    def test_learns_linearly_separable_truth_tables(self):
        for targets in [[0, 0, 0, 1], [0, 1, 1, 1]]:
            with self.subTest(targets=targets):
                model = Perceptron([0, 0.4], 0.3)
                history = model.fit(self.x, targets, 0.25, 0)
                self.assertTrue(model.converged_)
                self.assertEqual(history[-1], 0)
                self.assertEqual([model.apply(model.w, row, model.theta)
                                  for row in self.x], targets)

    def test_xor_stops_at_epoch_limit_without_claiming_convergence(self):
        model = Perceptron([0, 0.4], 0.3)
        history = model.fit(self.x, [0, 1, 1, 0], 0.25, 0, max_epochs=30)
        self.assertFalse(model.converged_)
        self.assertEqual(len(history), 30)
        self.assertGreater(history[-1], 0)

    def test_invalid_training_inputs(self):
        model = Perceptron([0, 0.4], 0.3)
        targets = [0, 0, 0, 1]
        for alpha in [0, -1, float("nan")]:
            with self.subTest(alpha=alpha), self.assertRaises(ValueError):
                model.fit(self.x, targets, alpha, 0)
        with self.assertRaises(ValueError):
            model.fit([], [], 0.25, 0)
        with self.assertRaises(ValueError):
            model.fit(self.x, [0, 1], 0.25, 0)
        with self.assertRaises(ValueError):
            model.fit(self.x, [0, 0, 0, 2], 0.25, 0)
        with self.assertRaises(ValueError):
            model.fit(self.x, targets, 0.25, 0, max_epochs=0)


if __name__ == "__main__":
    unittest.main()
