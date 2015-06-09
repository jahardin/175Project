from sklearn.svm import libsvm
import math

# First, build sparse SVM to identify useful features
normalizeByDocumentLength = true;
normalizeByFeature = true;
stochastic = true;
doPlot = true;

# Load preprocessed bag of words representations
[YTr, XTr] = libsvmread('trainLabeledBow.feat');
XTr = sparse(XTr);

[YTe, XTe] = libsvmread('testLabeledBow.feat');
XTe = sparse(XTe);

#Dataset contains extra features in test set (?)
feaUse = [1:len(XTe, 2)];
XTrN = XTr(:, feaUse);
XTeN = XTe(:, feaUse);
    

#Load vocabulary
f = fopen('imdb.vocab', 'r');
vocab = textscan(f, '%s'); vocab = vocab{1};
fclose(f);

#FIRST: train classification model to reduce feature space

#Convert to classification problem
YTrC = double(YTr>5);
YTeC = double(YTe>5);

# L1 Regularization
weightsL1 = zeros(1, numel(feaUse));

model = train(YTrC, XTrN, '-s 5 -c 0.031623');
weightsL1 = model.w;

featsNonZero = find(weightsL1 ~= 0);
weightsNonZero = weightsL1(featsNonZero);
vocabNonZero = {vocab{featsNonZero}};
'''
% ============== NAIVE BAYES ===============

% reduce feature space
XTr = XTr(:, featsNonZero);
XTe = XTe(:, featsNonZero);

% binarize all features
XTr = double(XTr >= 1);
XTe = double(XTe >= 1);
YTr = (YTr >= 5);
YTe = (YTe >= 5);

% Estimate class-conditional probabilities:

% Phat(x_i = 1| Y = y) = #(x_i = 1 && Y = y) / #(Y = y)
PhatPos = sum(XTr(YTr, :), 1)./sum(YTr);
PhatNeg = sum(XTr(~YTr, :), 1)./sum(~YTr);

% Because training/test sets are balanced, no need to learn P(y)
% (unnormalized) log probability of class "true":
% \sum_i log( x_i * Phat(X_i = 1 | Y = true) + (1 - x_i) * Phat(X_i = 0 | Y = true) )


% Evaluate on training examples:
logProbPos = sum(log(bsxfun(@times, XTr, PhatPos) + bsxfun(@times, (1 - XTr), (1 - PhatPos))), 2);
logProbNeg = sum(log(bsxfun(@times, XTr, PhatNeg) + bsxfun(@times, (1 - XTr), (1 - PhatNeg))), 2);
YHatTr = logProbPos > logProbNeg;
accTr = mean(YHatTr==YTr);

logProbPos = sum(log(bsxfun(@times, XTe, PhatPos) + bsxfun(@times, (1 - XTe), (1 - PhatPos))), 2);
logProbNeg = sum(log(bsxfun(@times, XTe, PhatNeg) + bsxfun(@times, (1 - XTe), (1 - PhatNeg))), 2);
YHatTe = logProbPos > logProbNeg;
accTe = mean(YHatTe==YTe);


disp(['Training Accuracy (nBayes): ' num2str(accTr)]);
disp(['Test Accuracy (nBayes): ' num2str(accTe)]);
'''
