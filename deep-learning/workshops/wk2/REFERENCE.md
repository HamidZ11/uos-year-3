# Week 2 · The perceptron

**Quick reference** · Learning a decision boundary

[All weeks](../README.md) · [Python code](perceptron_DL.py) · [Full experiment results](README.md) · [← Week 1](../wk1/REFERENCE.md) · [Week 3 →](../wk3/REFERENCE.md)

---

> **The idea:** a perceptron learns a straight decision boundary by correcting its mistakes. Its capacity limits what it can learn.

## 01 · Prediction and learning

| Symbol | Meaning |
|---|---|
| `x` | Input features, such as the two truth-table inputs. |
| `w` | One learned weight per input feature. |
| `theta` | Decision threshold; equivalent to an additive bias of `-theta`. |
| `alpha` | Learning rate: scales each correction. |
| `t`, `y` | Target label and predicted label, each either 0 or 1. |

```text
score      = dot(w, x)
prediction = 1 if score >= theta, otherwise 0
error      = target - prediction

w          = w + alpha * error * x
theta      = theta - alpha * error
```

A correct prediction gives zero error, so no update is needed. An **epoch** is one pass through all training examples.

## 02 · Why AND and OR work, but XOR does not

| Inputs | AND | OR | XOR |
|---|---|---|---|
| 0, 0 | 0 | 0 | 0 |
| 0, 1 | 0 | 1 | 1 |
| 1, 0 | 0 | 1 | 1 |
| 1, 1 | 1 | 1 | 0 |

**AND and OR are linearly separable:** one straight line separates the two labels. **XOR is not:** the positive examples occupy opposite corners. A different learning rate cannot overcome this limitation; a network with a nonlinear hidden layer can represent XOR.

## 03 · Error and stopping

**Mean squared error:** `MSE = mean((target - prediction) ** 2)`.

With hard binary predictions, each mistake contributes 1, so MSE also equals the fraction of incorrect predictions. Our code measures it **after each complete epoch**, using the same final weights for all examples.

```python
p = Perceptron([0, 0.4], theta=0.3)
history = p.fit(x, targets, alpha=0.25, acceptable_mse=0, max_epochs=100)
print(p.converged_, p.n_epochs_, history[-1])
```

`max_epochs` bounds the work. **Reaching the limit is not convergence**; check `converged_`. At rate 0.25, our AND and OR runs converged in 3 and 1 epochs respectively. XOR stopped after 100 epochs with MSE 0.50.

## 04 · What the learning-rate experiment showed

| Learning rate | AND epochs | OR epochs |
|---|---|---|
| 0.001 | 51 | 150 |
| 0.1 | 2 | 2 |
| 0.25 | 3 | 1 |

Smaller updates took longer from these starting parameters. Larger rates were **not always faster**: AND needed five epochs at 0.5. Keep initial weights and example order fixed when comparing rates.

---

**Run from the workshops folder:** `python wk2/perceptron_DL.py`

**Remember:** changing the training settings cannot fix a model that cannot represent the answer.
