import pandas as pd
from sklearn import metrics

def LogisticDiagnostics(logr, X, y, threshold=0.5):
    y_pred = (pd.DataFrame(logr.predict_proba(X))
              .loc[:, 0]
              .apply(lambda x: 0 if x>threshold else 1)
              .values)
    print('Test Set Metrics\n' + '*' * 40)
    metric_vals = {'Accuracy': metrics.accuracy_score(y, y_pred),
                   'Precision': metrics.precision_score(y, y_pred),
                   'Recall': metrics.recall_score(y, y_pred),
                   'F1 Score': metrics.f1_score(y, y_pred)}
    strpat = '%-10s%11.2f%s'
    print('%-10s%12s' % ('Metric', 'Result'))
    print('-' * 9 + ' ' * 7 + '-' * 6)
    for metric, result in metric_vals.items():
        print(strpat % (metric, result, '%'))
    print('\nConfusion Matrix\n' + '*' * 40)
    index = pd.MultiIndex.from_product([['Actual'], [0, 1]])
    columns = pd.MultiIndex.from_product([['Predicted'], [0, 1]])
    print(pd.DataFrame(confusion_matrix(y, y_pred), index=index, columns=columns)
          .applymap('{:,}'.format)
          .to_string())
