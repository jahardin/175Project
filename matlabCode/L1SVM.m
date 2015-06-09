addpath(genpath('liblinear-1.96'));

normalizeByDocumentLength = false;
normalizeByFeature = false;
doPlot = true;

% Choose range to search over for hyperparameter C
C = 10.^[-5:.25:0];

% Load preprocessed bag of words representations
[YTr, XTr] = libsvmread('aclImdb\train\labeledBow.feat');
XTr = sparse(XTr);

[YTe, XTe] = libsvmread('aclImdb\test\labeledBow.feat');
XTe = sparse(XTe);

% Dataset contains extra features in test set (?)
feaUse = [1:size(XTe, 2)];
XTrN = XTr(:, feaUse);
XTeN = XTe(:, feaUse);

if (normalizeByDocumentLength)
    XTrN = spdiags(1./sum(XTrN,2),0,size(XTrN, 1), size(XTrN, 1))*XTrN;
    XTeN = spdiags(1./sum(XTeN,2),0,size(XTeN, 1), size(XTeN, 1))*XTeN;
end

if (normalizeByFeature)    
    % Only rescale most common features (bsxfun hangs during computation)
    sc = 1./sum(XTrN(:, 1:2000), 1);
    XTrN(:, 1:2000) = bsxfun(@times, XTrN(:, 1:2000), sc);
    XTeN(:, 1:2000) = bsxfun(@times, XTeN(:, 1:2000), sc);

    % Zero-mean each feature: this leads to poor performance
    
    % [XTrN(:, 1:2000), mu, sc] = rescale(XTrN(:, 1:2000));
    % [XTeN(:, 1:2000), ~, ~] = rescale(XTeN(:, 1:2000), mu, sc);

    % Plot feature sums for verification
    % figure(); clf;
    % plot(sum(XTrN, 1))
    % drawnow;
end
    

% Load vocabulary
f = fopen('aclImdb\imdb.vocab', 'r');
vocab = textscan(f, '%s'); vocab = vocab{1};
fclose(f);

% Convert to classification problem
YTrC = double(YTr>5);
YTeC = double(YTe>5);

% L1 Regularization
weightsL1 = zeros(numel(C), numel(feaUse));
eRate = zeros(numel(C), 1);
eRateTr = zeros(numel(C), 1);
wordsUsed = zeros(numel(C), 1);

% Train models with sparse features
for i = 1:numel(C)
    model = train(YTrC, XTrN, sprintf('-s 5 -c %f', C(i)));
    weightsL1(i, :) = model.w;
    YTeHat = predict(YTeC, XTeN, model);
    YTrHat = predict(YTrC, XTrN, model);
    eRate(i) = mean(YTeHat~=YTeC);
    eRateTr(i) = mean(YTrHat~=YTrC);
    wordsUsed(i) = sum(model.w~=0);
end

best = find(eRate==min(eRate));
feats = find(weightsL1(best, :)~=0);

if doPlot
    figure(1); clf;
    plotyy(C, eRate, C, wordsUsed, @semilogx); hold on;
    semilogx(C, eRateTr, 'r'); 
    title('Error Rate vs. Complexity');
    legend({'Test Error', 'Training Error'});
    xlabel('Complexity C');
    ylabel('Error');
end
    
featsNonZero = find(weightsL1(best, :) ~= 0);
weightsNonZero = weightsL1(1:best, featsNonZero);
vocabNonZero = {vocab{featsNonZero}};

% Plot weights for increasing C
wplot = weightsNonZero;

if doPlot
    figure(2); clf;
    semilogx(C(1:best), wplot'); hold on;
    for i = 1:size(wplot, 2)
        text(C(best), wplot(end, i), vocabNonZero{i});
    end
    xlabel('Regularization penalty weight C');
    ylabel('Learned coefficient w');
    title('L1-Regularized SVM');
    xlim([C(1), C(best)]);
end

disp(['Best performance at C = ' num2str(C(best))]);
disp(['Training Error %: ' num2str(eRateTr(best))]);
disp(['Test Error %: ' num2str(eRate(best))]);
disp(['Number of features: ' num2str(numel(vocabNonZero))]);
disp(['Highest polarity words:']);

[sorted, idx] = sort(weightsNonZero(end, :));
for i = 1:5
    disp(['   ' vocabNonZero{idx(i)} ': ' num2str(weightsNonZero(end, idx(i)))]);
end

for i = numel(featsNonZero):-1:numel(featsNonZero)-5
    disp(['   ' vocabNonZero{idx(i)} ': ' num2str(weightsNonZero(end, idx(i)))]);
end



