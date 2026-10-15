# Week 3 · Feed-forward neural networks

**Quick reference** · MNIST, Fashion-MNIST and controlled experiments

[All weeks](../README.md) · [MNIST notebook](MINST%20Feedforward.ipynb) · [Fashion-MNIST notebook](Fashion_MNIST.ipynb) · [← Week 2](../wk2/REFERENCE.md) · [Week 4 →](../wk4/REFERENCE.md)

---

> **The idea:** turn images into numerical inputs, learn useful features with dense layers, and measure how well those features generalise.

## 01 · From image to prediction

Both datasets have **60,000 training images**, **10,000 test images**, **28 × 28 grayscale pixels** and **10 classes**. MNIST contains digits; Fashion-MNIST contains clothing categories.

```text
28 × 28 image → 784 scaled values → Dense(512, ReLU) → Dense(10, softmax)
```

| Step | Purpose |
|---|---|
| Flatten | Reshape each image into 784 features for the dense network. |
| Scale | Convert to `float32` and divide by 255: pixels become values in `[0, 1]`. |
| One-hot encode labels | Represent the correct class with one 1 and nine 0s. |
| ReLU hidden layer | Applies `max(0, value)`, adding nonlinearity to the network. |
| Softmax output | Produces ten class probabilities that sum to one. |
| Categorical cross-entropy | Matches the one-hot targets and ten-class output. |

Keep the raw data separate so preprocessing can be rerun without scaling or encoding twice.

## 02 · The model pattern

```python
model = keras.Sequential([
    keras.layers.Input(shape=(784,)),
    keras.layers.Dense(512, activation="relu"),
    keras.layers.Dense(10, activation="softmax"),
])
model.compile(
    optimizer=keras.optimizers.RMSprop(learning_rate=0.001),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)
```

**Dense-layer parameters:** `inputs * units + units` — the final term counts biases. The baseline has `(784 * 512 + 512) + (512 * 10 + 10) = 407,050` parameters. Use `model.summary()` to inspect shapes and counts.

## 03 · Settings you changed

| Setting | Meaning |
|---|---|
| Width / depth | Units in each hidden layer / number of hidden layers. More capacity also adds parameters. |
| Activation | ReLU versus tanh changes the nonlinear transformation in the hidden layers. |
| Epochs | Complete passes through the training subset; more can lead to overfitting. |
| Batch size | Examples per weight update; these experiments use **128**. |
| Learning rate | Scales the optimiser's updates; these runs compare **0.0001, 0.001 and 0.005**. |

Fashion-MNIST changes one factor at a time, using the same split and a fresh model with seed 42 for each run.

## 04 · Read the results correctly

**Training** updates weights. **Validation** chooses settings and an epoch budget. **Testing** measures the selected model after those choices.

Fashion-MNIST uses 50,000 training examples and 10,000 validation examples for comparison. The 15-epoch run reached its lowest validation loss at **epoch 8**; that setting was retrained on all 60,000 training examples for eight epochs.

| Saved final result | Test accuracy |
|---|---|
| MNIST: 512-unit ReLU layer, 5 epochs | **97.60%** |
| Fashion-MNIST: 512-unit ReLU layer, 8 epochs | **87.44%** |

MNIST uses a 48,000/12,000 training/validation split. The scores describe the saved runs; these are different datasets, not a controlled comparison of one setting.

## 05 · Watch for

- **A better training fit can generalise worse.** Falling training loss with rising validation loss indicates overfitting.
- **Accuracy and loss measure different things.** Confident wrong predictions can raise loss without greatly changing accuracy.
- **One seed is limited evidence.** Small differences do not establish a reliable winner or a fixed performance ceiling.
- **Keep the test set for the final evaluation.** Compare settings using validation scores.
