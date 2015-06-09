function yhat = logReg(X, w)
%logReg Apply logistic prediction function for logistic regression
%   X is nxd matrix of test examples
%   w is dx1 column of weights

    yhat = 1 + 9*sigmoid(X*w);
    
end