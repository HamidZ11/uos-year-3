# Deep Learning workshops

University of Salford, final year. Completed solutions for the supplied workshop
sheets for weeks 1-4, with explanations and measured experiment outputs.
Week 5 is reserved for working through together when its material is added.

| Week | Work | Where to start |
|---|---|---|
| 1 | Lists, duplicate detection, NumPy arrays, shapes, slicing, reshaping and the `Module` class | [Quick reference](wk1/REFERENCE.md) · [Python exercises](wk1/wk1.py) |
| 2 | AND/OR/XOR, bounded perceptron training and eight learning rates | [Quick reference](wk2/REFERENCE.md) · [Experiment results](wk2/README.md) · [Code](wk2/perceptron_DL.py) |
| 3 | MNIST example; Fashion-MNIST depth, activation, epoch and learning-rate comparisons | [Quick reference](wk3/REFERENCE.md) · [MNIST](wk3/MINST%20Feedforward.ipynb) · [Fashion-MNIST](wk3/Fashion_MNIST.ipynb) |
| 4 | IMDB sentiment analysis, validation, epoch/width/depth experiments and final test evaluation | [Quick reference](wk4/REFERENCE.md) · [IMDB notebook](wk4/IMDB.ipynb) |

Each week's `REFERENCE.md` is a compact recap: key concepts, a useful code pattern,
the important results and mistakes to avoid. Use the notebooks and experiment
notes for the full walkthrough.

The original workshop PDFs are retained in each week's folder. The MNIST
notebook's existing `MINST` filename is retained so existing references still work.

## Recorded results

All three notebooks were executed from fresh kernels on the full datasets.
These are the saved run's test scores, not guaranteed results for every run.

| Dataset | Final model | Epochs | Test loss | Test accuracy |
|---|---|---|---|---|
| MNIST | One 512-unit ReLU hidden layer | 5 | 0.0768 | 97.60% |
| Fashion-MNIST | One 512-unit ReLU hidden layer | 8, selected on validation loss | 0.3697 | 87.44% |
| IMDB | Two 16-unit ReLU hidden layers | 4, selected on validation loss | 0.2899 | 88.36% |

MNIST uses a 48,000/12,000 training/validation split. Fashion-MNIST compares on
a 50,000/10,000 split and IMDB on a 15,000/10,000 split; those two selected models
are then retrained on all original training examples before their final test.

## Run the work

The existing Python environment is in `wk3/.venv`:

```sh
source wk3/.venv/bin/activate
python wk1/wk1.py
python wk2/perceptron_DL.py
python -m unittest discover -s tests -v
```

Open the notebooks in VS Code and select that same environment as the notebook
kernel. Use **Restart Kernel**, then **Run All**, to reproduce a complete run.
Each notebook is independent; run its cells in order.

To create a fresh environment, use Python 3.13 and the pinned versions tested here:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Select `.venv` instead when using that environment. Keras downloads each dataset
the first time it is used and caches it locally. Package installation is kept out
of notebook cells so rerunning the coursework does not change the environment.

## How to interpret the results

- **Training data** updates the weights. Training accuracy alone does not measure
  performance on unseen examples.
- **Validation data** compares settings and chooses an epoch budget. Fashion-MNIST
  and IMDB use a fixed validation split shared by all their experiments.
- **Test data** gives the model's final score. Fashion-MNIST and IMDB are tested
  after selection and a fresh fit on all of their original training data.
- **Accuracy** measures correct classifications. **Cross-entropy loss** also
  reflects confidence, so the two metrics can move in different directions.
- Falling training loss alongside rising validation loss is evidence of
  **overfitting**. More layers, units or epochs do not automatically improve
  validation performance.

Random seeds help make comparisons repeatable. They do not guarantee identical
results across hardware/library versions or establish how much scores vary
between seeds. The experiment reflections distinguish measured results from
broader claims.

The IMDB notebook uses `float32` multi-hot vectors. Its full training and test
feature matrices together occupy about 2 GB, plus TensorFlow's working memory.
The test matrix is allocated after model selection.

The regression tests cover the hand-written list/class behaviour, learning AND
and OR, rejecting invalid training data, and stopping safely on XOR. The notebook
training runs verify the neural-network workflows on the full datasets.
