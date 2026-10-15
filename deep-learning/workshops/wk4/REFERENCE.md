# Week 4 · Sentiment analysis

**Quick reference** · IMDB reviews, validation and overfitting

[All weeks](../README.md) · [IMDB notebook](IMDB.ipynb) · [Workshop sheet](DL%20Workshop%204_imdb.pdf) · [← Week 3](../wk3/REFERENCE.md)

---

> **The idea:** represent a review numerically, predict positive or negative sentiment, and use validation to decide when training should stop.

## 01 · Representing text

The dataset contains **25,000 training reviews** and **25,000 test reviews**. Targets are **0 = negative** and **1 = positive**. Keras loads reviews as variable-length sequences of word IDs, restricted here to a 10,000-ID vocabulary.

| Representation | What it means |
|---|---|
| Word IDs | Integer tokens rather than raw text; decoding uses an offset of three for reserved IDs. |
| Multi-hot inputs | A 10,000-value vector: 1 if an ID appears, otherwise 0. Many positions can be 1. |
| Binary target | One sentiment label per review. It is not a ten-class one-hot target like week 3. |

**What is lost:** multi-hot vectors discard word order and word counts. Repeating a word still sets only one position to 1.

```python
vectorize([[1, 3, 3], [2]], dimension=5)
# [[0., 1., 0., 1., 0.],
#  [0., 0., 1., 0., 0.]]
```

Use `float32`: one 25,000 × 10,000 feature matrix needs about **1 GB**, compared with 2 GB for `float64`.

## 02 · The binary classifier

```text
10,000 features → Dense(16, ReLU) → Dense(16, ReLU) → Dense(1, sigmoid)
```

| Choice | Why it fits this task |
|---|---|
| Two ReLU hidden layers | Learn nonlinear combinations of word-presence features. |
| One sigmoid output | Returns a positive-sentiment score between 0 and 1. |
| Threshold 0.5 | Scores at or above 0.5 predict positive; lower scores predict negative. |
| Binary cross-entropy | Matches the single binary target and sigmoid output. |
| RMSprop | Updates the weights; learning rate **0.001**, batch size **512**. |

The baseline has **160,305 trainable parameters**. A sigmoid score is not guaranteed to be a calibrated probability.

## 03 · Validation before testing

| Data | Examples | Role |
|---|---|---|
| Training subset | 15,000 | Updates weights during the experiments. |
| Validation subset | 10,000 | Compares networks and selects the epoch budget. |
| Test set | 25,000 | Evaluates the selected model after retraining. |

```python
model = build_network(hidden_layers=(16, 16))
history = model.fit(
    partial_x_train, partial_y_train,
    validation_data=(x_val, y_val), epochs=10, batch_size=512,
)
best_epoch = int(np.argmin(history.history["val_loss"])) + 1
```

Training accuracy describes reviews already used to learn the weights. **It does not establish performance on unseen reviews.**

## 04 · Experiments and the result

| Factor | Values compared |
|---|---|
| Epoch count | 4, 10 and 20 |
| Hidden-layer width | Two layers with 8, 16 or 32 units each |
| Hidden-layer depth | One, two or three layers, each with 16 units |

Each run starts with fresh weights and the same seed and split. The selected configuration was **two 16-unit layers, trained for four epochs**, chosen by the lowest validation loss. Retraining on all 25,000 training reviews gave **88.36% test accuracy**, with **0.2899 test loss**.

## 05 · Recognise overfitting

In the 20-epoch experiment, the lowest validation loss occurred at **epoch 4**. By epoch 20, training accuracy reached **99.71%**, while validation accuracy was **86.99%**.

**Read the curves:** training loss falls, validation loss rises → the network fits the training reviews more closely while generalisation worsens. More training, units or layers are not automatic improvements. Use the validation result to make the choice, then keep the test score as the final check.

---

**Week 3 → week 4:** ten-class softmax + categorical cross-entropy becomes one sigmoid output + binary cross-entropy.
