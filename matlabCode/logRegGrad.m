function grad = logRegGrad(X, Y, w)
%logRegGradient Compute (stochastic) gradient for logistic regression
%   X is nxd matrix of training examples
%   Y is nx1 column of training labels
%   w is dx1 column of weights

    grad = -1*X'*((Y - logReg(X, w)).*sigmoid(X*w).*(1-sigmoid(X*w)));

end