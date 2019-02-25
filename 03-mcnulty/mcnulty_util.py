import pandas as pd
from sklearn import metrics

def ClassifierDiagnostics(clf, X, y, threshold=0.5):
    y_pred = (pd.DataFrame(clf.predict_proba(X))
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
    print(pd.DataFrame(metrics.confusion_matrix(y, y_pred), index=index,
                       columns=columns)
          .applymap('{:,}'.format)
          .to_string())

def status_filter(input_df):
    df = input_df.copy()
    statuses = ['Fully Paid', 'Charged Off', 'Default']
    return df.loc[df.loan_status.isin(statuses), ]

def remove_annual_inc_nas(input_df):
    df = input_df.copy()
    return df.loc[~df.annual_inc.isna(), ]

def emp_length_filter(input_df):
    df = input_df.copy()
    na_mask = df.emp_length.isna() | (df.emp_length == 'n/a')
    return df.loc[~na_mask, ]

def revol_util_filter(input_df):
    df = input_df.copy()
    na_mask = df.revol_util.isna()
    return df.loc[~na_mask, ]

def make_dummy(input_df, column):
    df = input_df.copy()
    dummies = (df.loc[:, [column]]
               .pipe(pd.get_dummies)
               .iloc[:, 1:])
    return df.join(dummies).drop(column, axis=1)
