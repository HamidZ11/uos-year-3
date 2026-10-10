import numpy as np

class Perceptron:
    def __init__(self, w, theta): # define constructor
        self.w = w
        self.theta = theta

    def apply(self, w, xi, theta): # method for computing output given an example

        a = np.dot(w,xi) # multiply input * weights
        if a >= theta: 
            return 1
        else: 
            return 0 

    def fit(self, x,t, alpha, acceptable_mse): #method for learning (FITS THE MODEL)

        mse = 20
        w_i = self.w # current values of w and theta 
        theta_i = self.theta
        list_mse = []

        while mse > acceptable_mse:
            mse = 0.0

            for i in range(len(x)):
                yi = self.apply(w_i, x[i], theta_i)
                diff = t[i] - yi
                delta = alpha * diff
                w_i = w_i + delta * x[i]
                theta_i = theta_i - delta

                mse = mse + diff*diff

            mse = mse / len(x) 
            list_mse.append(mse)

        self.w = w_i
        self.theta = theta_i

        return list_mse

# mse - mean squared error
# x - examples



# Example use

w = np.array([0, 0.4])
x = np.array([[0,0], [0,1], [1,0], [1,1]])
t = np.array([0,0,0,1])

theta = 0.3
alpha = 0.25
acceptable_mse = 0.01

p = Perceptron(w, theta)
results = p.fit(x,t, alpha, acceptable_mse)
print(results)
print("weights", p.w, p.theta)

