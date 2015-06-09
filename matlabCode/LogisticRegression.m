addpath(genpath('liblinear-1.96'));

normalizeByDocumentLength = true;
normalizeByFeature = true;
stochastic = true;
doPlot = true;

% Load preprocessed bag of words representations
[YTr, XTr] = libsvmread('aclImdb\train\labeledBow.feat');
XTr = sparse(XTr);

[YTe, XTe] = libsvmread('aclImdb\test\labeledBow.feat');
XTe = sparse(XTe);

% Dataset contains extra features in test set (?)
feaUse = [1:size(XTe, 2)];
XTrN = XTr(:, feaUse);
XTeN = XTe(:, feaUse);
    

% Load vocabulary
f = fopen('aclImdb\imdb.vocab', 'r');
vocab = textscan(f, '%s'); vocab = vocab{1};
fclose(f);

% FIRST: train classification model to reduce feature space

% Convert to classification problem
YTrC = double(YTr>5);
YTeC = double(YTe>5);

% L1 Regularization
weightsL1 = zeros(1, numel(feaUse));

model = train(YTrC, XTrN, '-s 5 -c 0.031623');
weightsL1 = model.w;

featsNonZero = find(weightsL1 ~= 0);
weightsNonZero = weightsL1(featsNonZero);
vocabNonZero = {vocab{featsNonZero}};

% Logistic Regression

% reduce feature space
XTrR = XTr(:, featsNonZero);
XTeR = XTe(:, featsNonZero);

if (normalizeByDocumentLength)
    XTrR = spdiags(1./sum(XTrR,2),0,size(XTrR, 1), size(XTrR, 1))*XTrR;
    XTeR = spdiags(1./sum(XTeR,2),0,size(XTeR, 1), size(XTeR, 1))*XTeR;
end

XTrR = [ones(size(XTr, 1), 1) XTrR];
XTeR = [ones(size(XTe, 1), 1) XTeR];

if (normalizeByFeature)
    sc = 1./sum(XTrR, 1);
    XTrR = bsxfun(@times, XTrR, sc);
    XTeR = bsxfun(@times, XTeR, sc);
end


% randomly initialize weights
wL = randn(size(XTrR, 2), 1)*1.0;
wL(1) = randn*1.0+5;

mseTr = zeros(1, 1000);
mseTe = zeros(1, 1000);



% Full gradient descent

if ~stochastic
    eta = 100;
    niter = 100;
    for i = 1:niter 
        wL = wL - eta*logRegGrad(XTrR, YTr, wL);

        mseTr(i) = mean((YTr-logReg(XTrR, wL)).^2);
        mseTe(i) = mean((YTe-logReg(XTeR, wL)).^2);
        if doPlot
            if (mod(i, 10)==0)
                figure(1);
                semilogx(1:i, mseTr(1:i), 'r-'); hold on;
                semilogx(1:i, mseTe(1:i), 'g-'); hold off;
                xlim([0, niter]);
                title('Gradient Descent');
                xlabel('Number of iterations');
                ylabel('MSE');
                legend({'Training MSE', 'Testing MSE'});
                drawnow;
            end
        end
    end
end

% Stochastic gradient descent

if stochastic
    wL = randn(size(XTrR, 2), 1)*.05;
    wL(1) = randn*.05 +5;
    
    batchSize = 1000;
    eta = 1000;
    niter = 100;
    
    for i = 1:niter
        
        ssz = eta/sqrt(i);
        
        order = randperm(size(XTrR, 1));
        
        XTrS = XTrR(order, :);
        YTrS = YTr(order);
        
        for j = 1:numel(order)/batchSize
            
        
            wL = wL - ssz*logRegGrad(XTrS((j-1)*batchSize+1:j*batchSize, :), ... 
                                     YTrS((j-1)*batchSize+1:j*batchSize), ...
                                     wL);
        
        end
            
        mseTr(i) = mean((YTr-logReg(XTrR, wL)).^2);
        mseTe(i) = mean((YTe-logReg(XTeR, wL)).^2);
    
        if doPlot
            if (mod(i, 10)==0)
                figure(1);
                semilogx(1:i, mseTr(1:i), 'r-'); hold on;
                semilogx(1:i, mseTe(1:i), 'g-'); hold off;
                xlim([0, niter]);
                title('Stochastic Gradient Descent');
                xlabel('Number of iterations');
                ylabel('MSE');
                legend({'Training MSE', 'Testing MSE'});
                drawnow;
            end
        end
    end
end

disp(['Training MSE: ' num2str(mseTr(end))]);
disp(['Test MSE: ' num2str(mseTe(end))]);
disp(['Number of features: ' num2str(numel(vocabNonZero))]);
disp(['Highest polarity words:']);

[sorted, idx] = sort(wL(2:end));
for i = 1:5
    disp(['   ' vocabNonZero{idx(i)} ': ' num2str(wL(idx(i)+1))]);
end

for i = numel(featsNonZero):-1:numel(featsNonZero)-5
    disp(['   ' vocabNonZero{idx(i)} ': ' num2str(wL(idx(i)+1))]);
end
