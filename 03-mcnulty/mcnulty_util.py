import itertools
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn import metrics
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

"""
Preprocessing
"""


def features_from_excel():
    lc_dd = pd.read_excel(r'data/LCDataDictionary.xlsx')
    qstr = 'Include == 1'
    cols = [x.strip() for x in lc_dd.query(qstr).LoanStatNew.values.tolist()]
    cols.remove('id')
    return cols

def loan_status_filter(input_df):
    df = input_df.copy()
    loan_status_lst = ['Fully Paid', 'Charged Off', 'Late (31-120 days)', 'Default']
    mask = df.loan_status.isin(loan_status_lst)
    return df.loc[mask, :]

def make_dummy(input_df, column):
    df = input_df.copy()
    dummies = (df.loc[:, [column]]
               .pipe(pd.get_dummies))
    return df.join(dummies).drop(column, axis=1)

def mcnulty_preprocessing():
    print('Initiating MAXIMUM data munging power')
    df = (pd.read_csv(r'Data/loan.csv', low_memory=False)
          .set_index('id')
          .pipe(loan_status_filter)
          .query('application_type == "INDIVIDUAL"')
          .query('home_ownership != "ANY"')
          .loc[:, features_from_excel()]
          .assign(issue_d=lambda x: x.issue_d.astype('datetime64'),
                  default=lambda x: np.where(x.loan_status=='Fully Paid', 0, 1),
                  term=lambda x: x.term.str.strip(),
                  emp_length=lambda x: x.emp_length.fillna('Not provided')))
    print('Luther Preprocessing Successful Woo Woo!\n')
    return df

def unpack_list(lst_2d):
    return list(itertools.chain.from_iterable(lst_2d))

"""
Logging models
"""

def results_to_df(results):
    col_ord = ['model_type', 'features', 'degree', 
               'train_accuracy', 'test_accuracy', 'precision', 'recall', 'f1_score', 
               'true_negatives', 'false_positives', 'false_negatives', 'true_positives'] 
    return (pd.DataFrame(results)
            .reindex(columns=col_ord)
            .sort_values('test_accuracy', ascending=False))

def scores_formatted(input_df):
    df = input_df.copy()
    scores = ['train_accuracy', 'test_accuracy', 'precision', 'recall', 'f1_score']
    for s in scores:
        df[s] = df[s].map('{:0.2%}'.format)
    gross_scores = ['true_negatives', 'false_positives', 'false_negatives', 'true_positives']
    for gs in gross_scores:
        df[gs] = df[gs].map('{:,.0f}'.format)
    return df
    
def log_clf_model(results, model, model_type, X, y, features, degree=1):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=11,
                                                        stratify=y)
    model.fit(X_train, y_train)
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    y_hat = model.predict(X_test)
    precision = metrics.precision_score(y_test, y_hat)
    recall = metrics.recall_score(y_test, y_hat)
    f1 = metrics.f1_score(y_test, y_hat)
    tn, fp, fn, tp = metrics.confusion_matrix(y_test, y_hat).ravel()
    record = {'model_type': model_type,
              'features': features,
              'degree': degree,
              'train_accuracy': train_accuracy,
              'test_accuracy': test_accuracy,
              'precision': precision,
              'recall': recall,
              'f1_score': f1,
              'true_negatives': tn,
              'false_positives': fp,
              'false_negatives': fn,
              'true_positives': tp}
    results.append(record)


"""
Sklearn Extensions
"""

independents = {'dti': 'numeric',
                'int_rate': 'numeric',
                'annual_inc': 'numeric',
                'loan_amnt': 'numeric',
                'revol_bal': 'numeric',
                'installment': 'numeric',
                'delinq_2yrs': 'numeric',
                'term': 'dummy',
                'home_ownership': 'dummy',
                'grade': 'dummy',
                'purpose': 'dummy',
                'emp_length': 'dummy',
                'addr_state': 'dummy'}

class ItemSelector(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None):
        return self

    def transform(self, data_dict):
        return data_dict.loc[:, self.key]
    
def poly_pipeline(features, degree):
    poly_steps = [('selector', ItemSelector(key=features)),
                  ('poly', PolynomialFeatures(degree=degree, include_bias=False))]
    pipeline = Pipeline(poly_steps)
    return pipeline

def dummy_pipeline(feature_name):
    feature = [feature_name]
    steps = [('selector', ItemSelector(key=feature)),
             ('enc', OneHotEncoder())]
    pipeline = Pipeline(steps)
    return pipeline

def feature_transformer_list(features, degree):
    transformer_list = list()
    numerics = [x for x in features if independents[x] == 'numeric']
    if numerics:
        numeric_trans = ('numeric', poly_pipeline(numerics, degree))
        transformer_list.append(numeric_trans)
    dummy_vars = [x for x in features if independents[x] == 'dummy']
    if dummy_vars:
        dummy_steps = list()
        for dummy in dummy_vars:
            step = ('{}_enc'.format(dummy), dummy_pipeline(dummy))
            dummy_steps.append(step)
        transformer_list += dummy_steps
    return transformer_list

def clf_pipeline(clf, features, degree):
    transformer_list = feature_transformer_list(features, degree)
    return Pipeline([('union', FeatureUnion(transformer_list=transformer_list)),
                     ('clf', clf)])

"""
Data Viz
"""

def millions(x, pos):
    'The two args are the value and tick position'
    return '%1.0fM' % (x*1e-6)
mil_fmt = FuncFormatter(millions)

def thousands(x, pos):
    'The two args are the value and tick position'
    return '%1.0fK' % (x*1e-3)
k_fmt = FuncFormatter(thousands)

def percent(x, pos):
    return '{:,.2%}'.format(x)
percent_formatter = FuncFormatter(percent)

def plot_estimator(estimator, X, y):
    x_min, x_max = X.iloc[:,0].min() - 0.1, X.iloc[:,0].max() + 0.1
    y_min, y_max = X.iloc[:,1].min() - 0.1, X.iloc[:,1].max() + 0.1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100),
                         np.linspace(y_min, y_max, 100))
    df_linspace = pd.DataFrame(np.c_[xx.ravel(), yy.ravel()], columns=X.columns.tolist())
    Z = estimator.predict(df_linspace)
                        
    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    fig, ax = plt.subplots(figsize=(12,12))
    ax.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.3)
    # Lets plot our sample points
    default_mask = y == 1
    ax.scatter(X.iloc[:, 0][~default_mask], X.iloc[:, 1][~default_mask], c='blue', label='Fully Paid',
              alpha=0.9, edgecolors='black')
    ax.scatter(X.iloc[:, 0][default_mask], X.iloc[:, 1][default_mask], c='red', label='Default',
              alpha=0.5, edgecolors='black')
    ax.set(xlabel=X.columns.tolist()[0], ylabel=X.columns.tolist()[1])
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    plt.legend()
    return ax