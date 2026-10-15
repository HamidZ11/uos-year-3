"""Workshop 2: AND, OR, XOR and the effect of the learning rate."""

from pathlib import Path

import numpy as np


class Perceptron:
    def __init__(self, w, theta):
        self.w = np.asarray(w, dtype=float).copy()
        if self.w.ndim != 1 or not self.w.size or not np.isfinite(self.w).all():
            raise ValueError("Weights must be a non-empty, finite vector.")
        if not np.isfinite(theta):
            raise ValueError("The threshold must be finite.")
        self.theta = float(theta)
        self.converged_ = False
        self.n_epochs_ = 0

    def apply(self, w, xi, theta):
        # theta is a threshold; the equivalent additive bias is -theta.
        return int(np.dot(w, xi) >= theta)

    def fit(self, x, t, alpha, acceptable_mse, max_epochs=1000):
        """Learn with online updates; return the MSE after each complete epoch.

        max_epochs makes non-separable data such as XOR safe to investigate.
        converged_ records whether the requested error was actually reached.
        """
        x = np.asarray(x, dtype=float)
        t = np.asarray(t, dtype=float)
        if x.ndim != 2 or not len(x) or x.shape[1] != len(self.w):
            raise ValueError("x must contain examples with one column per weight.")
        if t.shape != (len(x),) or not np.isin(t, [0, 1]).all():
            raise ValueError("Provide one binary target (0 or 1) per example.")
        if not np.isfinite(x).all():
            raise ValueError("Inputs must be finite.")
        if not np.isfinite(alpha) or alpha <= 0:
            raise ValueError("The learning rate must be positive and finite.")
        if not np.isfinite(acceptable_mse) or not 0 <= acceptable_mse < 1:
            raise ValueError("acceptable_mse must be between 0 (inclusive) and 1.")
        if not isinstance(max_epochs, (int, np.integer)) or max_epochs <= 0:
            raise ValueError("max_epochs must be a positive integer.")

        self.converged_ = False
        history = []
        for _ in range(max_epochs):
            for xi, target in zip(x, t):
                prediction = self.apply(self.w, xi, self.theta)
                delta = alpha * (target - prediction)
                self.w = self.w + delta * xi
                self.theta = self.theta - delta

            # Evaluate the final weights together, rather than mixing errors
            # measured before different updates within the same epoch.
            predictions = (x @ self.w >= self.theta).astype(int)
            mse = float(np.mean((t - predictions) ** 2))
            history.append(mse)
            if mse <= acceptable_mse:
                self.converged_ = True
                break

        self.n_epochs_ = len(history)
        return history


def main():
    import matplotlib.pyplot as plt

    x = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    targets = {"AND": [0, 0, 0, 1], "OR": [0, 1, 1, 1], "XOR": [0, 1, 1, 0]}
    figure, axes = plt.subplots(1, 2, figsize=(11, 4))

    print("Gate experiments (learning rate 0.25)")
    for name, t in targets.items():
        p = Perceptron([0, 0.4], theta=0.3)
        history = p.fit(x, t, alpha=0.25, acceptable_mse=0, max_epochs=100)
        predictions = [p.apply(p.w, xi, p.theta) for xi in x]
        print(f"{name}: predictions={predictions}, epochs={p.n_epochs_}, "
              f"MSE={history[-1]:.2f}, converged={p.converged_}")
        axes[0].plot(range(1, len(history) + 1), history,
                     marker="o" if name != "XOR" else None, label=name)

    rates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.25, 0.5, 1.0]
    print("\nLearning-rate comparison (same starting weights and example order)")
    print("gate | learning rate | epochs | final MSE | converged")
    for name in ["AND", "OR"]:
        epochs = []
        for alpha in rates:
            p = Perceptron([0, 0.4], theta=0.3)
            history = p.fit(x, targets[name], alpha, 0, max_epochs=5000)
            epochs.append(p.n_epochs_)
            print(f"{name} | {alpha:g} | {p.n_epochs_} | {history[-1]:.2f} | {p.converged_}")
        axes[1].plot(rates, epochs, marker="o", label=name)

    axes[0].set(xlabel="Epoch (log scale)", ylabel="MSE after epoch", title="Learning truth tables")
    axes[0].set_xscale("log")
    axes[1].set(xlabel="Learning rate (log scale)", ylabel="Epochs to convergence",
                title="Effect of learning rate")
    axes[1].set_xscale("log")
    for axis in axes:
        axis.legend()
        axis.grid(alpha=0.3)
    figure.tight_layout()
    output = Path(__file__).with_name("perceptron_experiments.png")
    figure.savefig(output, dpi=150)
    print(f"\nSaved plot: {output.name}")
    if plt.get_backend().lower() == "agg":
        plt.close(figure)
    else:
        plt.show()


if __name__ == "__main__":
    main()
