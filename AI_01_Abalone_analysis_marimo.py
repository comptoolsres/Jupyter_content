import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Abalone data analysis

    This notebook was created in class as we walked through the analysis done by [Amo Moloko in their Kaggle notebook](https://www.kaggle.com/code/princeashburton/abalone-analysis-supervised-learning/notebook).
    """)
    return


@app.cell
def _():
    #Standard libs
    import numpy as np 
    import pandas as pd 

    #Data Visualisation libs
    import matplotlib.pyplot as plt
    import seaborn as sns
    import scipy.stats as st

    #Feature engineering, metrics and modeling libs
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.metrics import mean_absolute_error
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import cross_val_score
    from sklearn.ensemble import RandomForestRegressor
    #from sklearn.preprocessing import Imputer
    from xgboost import XGBRegressor
    from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
    #from sklearn.ensemble.partial_dependence import partial_dependence, plot_partial_dependence
    from sklearn.pipeline import make_pipeline
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import accuracy_score
    from sklearn import metrics

    #Detect Missing values
    #import missingno as msno


    import os

    return (
        DecisionTreeRegressor,
        XGBRegressor,
        cross_val_score,
        make_pipeline,
        mean_absolute_error,
        np,
        pd,
        plt,
        sns,
        st,
        train_test_split,
    )


@app.cell
def _(pd):
    abalone = pd.read_csv('../../share/abalone.csv')
    return (abalone,)


@app.cell
def _(abalone):
    abalone.head()
    return


@app.cell
def _(abalone):
    abalone.info()
    return


@app.cell
def _(abalone):
    abalone.describe()
    return


@app.cell
def _(abalone):
    abalone.shape
    return


@app.cell
def _(abalone, plt, sns, st):
    rings = abalone['Rings']
    plt.figure(1);plt.title('Normal')
    sns.distplot(rings,kde=False,fit=st.norm)
    plt.figure(2);plt.title('Johnson SU')
    sns.distplot(rings,kde=False,fit=st.johnsonsu)
    plt.figure(3);plt.title('Log Normal')
    sns.distplot(rings,kde=False,fit=st.lognorm)
    return


@app.cell
def _(abalone, np):
    numeric_features = abalone.select_dtypes(include=[np.number])
    correlation = numeric_features.corr()
    print(correlation['Rings'].sort_values(ascending=False))
    return


@app.cell
def _(abalone, plt, sns):
    cols = ['Rings','Shell weight','Diameter','Height','Length']
    sns.pairplot(abalone[cols],size=2,kind='scatter')
    plt.show()
    return


@app.cell
def _(abalone, sns):
    f = (abalone.loc[abalone['Sex'].isin(['M','F'])]
          .loc[:,['Shell weight','Rings','Sex']])

    f = f[f["Rings"] >= 8]
    f = f[f["Rings"] < 23]
    sns.boxplot(x="Rings",y="Shell weight", hue='Sex',data=f)
    return


@app.cell
def _(abalone, np):
    from scipy import stats
    z= np.abs(stats.zscore(abalone.select_dtypes(include=[np.number])))
    print(z)
    return (z,)


@app.cell
def _(abalone, z):
    abalone_o = abalone[(z < 3).all(axis=1)]
    return (abalone_o,)


@app.cell
def _(abalone, abalone_o):
    print("Shape of Abalones with outliers: "+ str(abalone.shape) , 
          "Shape of Abalones without outliers: " + str(abalone_o.shape))
    return


@app.cell
def _(abalone_o):
    low_cardinality_cols = [cname for cname in abalone_o.columns if
                            abalone_o[cname].nunique() < 10 and 
                           abalone_o[cname].dtype == "object"]
    numeric_cols = [cname for cname in abalone_o.columns if
                                     abalone_o[cname].dtype in ['int64','float64']]

    my_cols = low_cardinality_cols + numeric_cols
    abalone_predictors = abalone_o[my_cols]
    return (abalone_predictors,)


@app.cell
def _(abalone_predictors):
    abalone_predictors.head()
    return


@app.cell
def _(abalone_predictors):
    abalone_predictors.dtypes.sample(7)
    return


@app.cell
def _(abalone_predictors, pd):
    abalone_encoded_predictors = pd.get_dummies(abalone_predictors)
    return (abalone_encoded_predictors,)


@app.cell
def _(abalone_encoded_predictors):
    abalone_encoded_predictors.head()
    return


@app.cell
def _(abalone_encoded_predictors):
    abalone_encoded_predictors.shape
    return


@app.cell
def _(
    DecisionTreeRegressor,
    abalone_encoded_predictors,
    cross_val_score,
    make_pipeline,
):
    cross_cols = ['Length','Diameter','Height','Whole weight','Shucked weight','Viscera weight','Shell weight','Sex_F','Sex_I','Sex_M']
    X = abalone_encoded_predictors[cross_cols]
    y = abalone_encoded_predictors.Rings

    decision_pipeline = make_pipeline(DecisionTreeRegressor())
    decision_scores = cross_val_score(decision_pipeline, X,y,scoring='neg_mean_absolute_error')

    print('MAE %2f' %(-1 * decision_scores.mean()))
    return X, y


@app.cell
def _(
    DecisionTreeRegressor,
    X,
    make_pipeline,
    mean_absolute_error,
    train_test_split,
    y,
):
    dt_train_X,dt_test_X,dt_train_y,dt_test_y = train_test_split(X,y)
    decision_split_pipeline = make_pipeline(DecisionTreeRegressor(max_leaf_nodes=5))
    decision_split_pipeline.fit(dt_train_X,dt_train_y)
    decision_tree_prediction = decision_split_pipeline.predict(dt_test_X)
    print("MAE: " + str(mean_absolute_error(decision_tree_prediction,dt_test_y)))
    return decision_split_pipeline, dt_test_X, dt_test_y


@app.cell
def _(decision_split_pipeline, dt_test_X, dt_test_y):
    acc_decision = decision_split_pipeline.score(dt_test_X,dt_test_y)
    print("Acc:", acc_decision )
    return


@app.cell
def _(X, train_test_split, y):
    train_X,test_X,train_y,test_y = train_test_split(X.values,y.values,test_size=0.25)
    return test_X, test_y, train_X, train_y


@app.cell
def _(XGBRegressor, mean_absolute_error, test_X, test_y, train_X, train_y):
    xgb_model = XGBRegressor()
    xgb_model.fit(train_X,train_y,verbose=False)
    xgb_preds = xgb_model.predict(test_X)
    print("MAE: " + str(mean_absolute_error(xgb_preds,test_y)))
    print("Accuracy:",xgb_model.score(test_X,test_y))
    return


@app.cell
def _(XGBRegressor, mean_absolute_error, test_X, test_y, train_X, train_y):
    xgb_model_II = XGBRegressor(n_estimators=1000, learning_rat=0.05)
    xgb_model_II.fit(train_X, train_y, early_stopping_rounds=5, eval_set=[(test_X, test_y)], verbose=False)
    xgb_preds_1 = xgb_model_II.predict(test_X)
    print('MAE: ' + str(mean_absolute_error(xgb_preds_1, test_y)))
    print('Accuracy:', xgb_model_II.score(test_X, test_y))
    return (xgb_preds_1,)


@app.cell
def _(plt, test_y, xgb_preds_1):
    plt.scatter(test_y, xgb_preds_1, color='blue')
    plt.xlabel('Actuals')
    plt.ylabel('Predictions')
    plt.title('Actuals vs Predictions')
    plt.show()
    return


if __name__ == "__main__":
    app.run()
