function sig = sigmoid(X)
%sigmoid Computes logistic function (vectorized)
%   X is column vector of linear responses

    sig = 1./(1 + exp(-X));
    
end