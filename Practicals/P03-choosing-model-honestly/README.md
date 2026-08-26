# Practical 03: Choosing a Model Honestly

**SCSE3040 Machine Learning Operations | Bennett University | Session 2026-27**

> Compare model capacity, observe overfitting, select configurations with cross-validation, and preserve the final test set for one independent evaluation.

| Item | Detail |
|---|---|
| Follows lectures | L04-L05 |
| Course Outcome | CO2 |
| Duration | 120 minutes |
| Approx. memory | 400 MB |
| GPU required | No |
| Extra software | Nothing beyond the course environment |
| Assessment | 10 marks |

## 1. Why this practical exists

P02 established the first boundary:

```text
training data != test data
```

P03 strengthens that idea.

A common workflow mistake is to train several models, inspect their test scores, change their settings, inspect the test scores again, and finally keep the configuration that performed best. The code may never fit on `y_test`, yet the **human development process has still learned from the test set**.

The stronger workflow is:

```text
ALL DATA
   |
   +--------------------------+
   |                          |
   v                          v
DEVELOPMENT DATA          FINAL TEST DATA
(X_train, y_train)        (X_test, y_test)
   |                          |
   | 5-fold CV                | untouched during
   | model/config selection   | model selection
   v                          |
SELECT CONFIGURATION          |
   |                          |
   v                          |
FIT ON ALL DEVELOPMENT DATA   |
   |                          |
   +------------->------------+
                  |
                  v
          ONE FINAL EVALUATION
```

That separation is the central engineering lesson of P03.

## 2. Learning outcomes

After P03, you should be able to:

- compare training and held-out errors;
- recognise overfitting as observed behaviour rather than a label attached to an algorithm;
- explain why a small train/test gap does not automatically mean a good model;
- identify underfitting;
- perform 5-fold cross-validation on development data;
- interpret mean validation MAE and its fold-to-fold spread;
- tune a hyperparameter without repeatedly consulting the final test set;
- build a reusable model-comparison function;
- select a model using predictive and operational evidence;
- evaluate the selected configuration once on the final held-out test set.

## 3. Starting point

P03 assumes P02 is complete.

The same dataset and prediction contract are used:

```python
FEATURES = [
    "distance_km",
    "prep_time_min",
    "traffic_level",
    "rain",
]
TARGET = "delivery_min"
```

The primary split remains:

```text
80% development/training data
20% final held-out test data
random_state = 42
```

## 4. Four models, four lessons

The walkthrough deliberately uses models with different capacities.

| Model | What it helps reveal |
|---|---|
| Linear Regression | a simple model can generalise well when its assumptions fit the data |
| Unrestricted Decision Tree | near-perfect training fit can coexist with worse unseen-data performance |
| Depth-4 Decision Tree | reducing capacity can reduce the gap but can also underfit |
| Random Forest | ensembling can improve generalisation, but does not abolish overfitting |

The point is not that one algorithm is universally best.

## 5. The train/test gap

For MAE:

```text
gap = test MAE - training MAE
```

A large positive gap is evidence consistent with overfitting.

But the gap is **not a standalone quality score**.

A model can have:

```text
train MAE = 10
test MAE  = 10.1
gap       = 0.1
```

and still be poor because both errors are high.

Likewise, a slightly negative gap is possible when the held-out sample happens to be a little easier than the training sample.

## 6. Why cross-validation belongs only to development data here

P03 deliberately keeps `X_test` and `y_test` untouched during model and hyperparameter selection.

Five-fold cross-validation is therefore performed on:

```python
X_train, y_train
```

not on the full `X, y`.

Each development observation is used for validation once and for fitting in the other four folds.

This distinction matters because the final test partition is intended to remain independent of the decisions made during development.

## 7. Understanding scikit-learn's negative MAE

scikit-learn's scoring interface follows a higher-is-better convention.

Therefore:

```python
scoring="neg_mean_absolute_error"
```

returns the negative of MAE.

Convert it back:

```python
mae_scores = -cross_val_score(...)
```

Then lower positive MAE is better.

## 8. Hyperparameter tuning

The notebook sweeps Decision Tree depth using only development-data cross-validation.

A typical validation-error pattern is:

```text
too shallow        useful capacity        too flexible
underfitting   ->      minimum       ->   overfitting risk
```

Do not assume every empirical curve will be perfectly smooth or exactly U-shaped. The measured optimum depends on the dataset, folds, model, and random state.

## 9. Tasks

### T1: Measure overfitting manually

Fit:

```python
DecisionTreeRegressor(
    max_depth=12,
    random_state=42,
)
```

and calculate:

```python
T1_train_mae
T1_test_mae
T1_gap
```

with:

```text
T1_gap = T1_test_mae - T1_train_mae
```

This task intentionally asks you to write the scoring steps yourself.

### T2: Tune Random Forest depth without touching the final test set

Evaluate:

```text
max_depth = 2, 4, 6, None
```

for:

```python
RandomForestRegressor(
    n_estimators=50,
    random_state=42,
)
```

using 5-fold cross-validation on `X_train, y_train`.

Create:

```python
T2_scores
T2_best_depth
```

The final test set must not participate in this search.

### T3: Build a reusable comparison function

Implement:

```python
compare(models)
```

where `models` is a dictionary of `{name: estimator}`.

The function must use 5-fold cross-validation on the development data and return:

```python
{
    "model_name": {
        "cv_mae_mean": ...,
        "cv_mae_std": ...
    }
}
```

This structure is deliberately machine-readable. Later, MLflow will record the same kinds of model parameters and metrics as experiment runs.

## 10. Final evaluation

After model/configuration selection is complete:

1. instantiate the selected configuration;
2. fit it on all `X_train, y_train`;
3. evaluate it once on `X_test, y_test`;
4. record the final MAE.

This is the score intended to approximate performance on unseen data under the current experimental design.

It is still evidence, not a guarantee of production behaviour.

## 11. Reference observations

For the supplied synthetic dataset, the walkthrough should produce values close to:

```text
LinearRegression
  train MAE  2.04
  test MAE   1.92
  gap       -0.11

DecisionTree, unrestricted
  train MAE  0.00
  test MAE   3.43
  gap        3.43

DecisionTree, depth 4
  train MAE  3.66
  test MAE   4.23
  gap        0.57

RandomForest, 50 trees
  train MAE  1.00
  test MAE   2.39
  gap        1.40
```

For **development-only 5-fold CV**, values should be close to:

```text
LinearRegression           2.05 +/- 0.17
DecisionTree (depth 4)     4.44 +/- 0.33
RandomForest (50 trees)    2.75 +/- 0.25
```

The development-only Decision Tree depth sweep is approximately:

```text
depth 2      5.89
depth 3      4.81
depth 4      4.44
depth 6      3.64
depth 8      3.49
depth None   3.51
```

These are reference observations for this teaching dataset, not universal performance expectations.

## 12. Common mistakes

| Mistake | Why it is a problem |
|---|---|
| choosing the model with the lowest training MAE | measures fit to seen observations, not generalisation |
| treating a small gap as proof of a strong model | both train and validation errors can be high |
| tuning `max_depth` on `X_test, y_test` | leaks final-evaluation information into development |
| running CV on full `X, y` while claiming the test set is untouched | the nominal test observations enter the model-selection process |
| forgetting the minus sign for `neg_mean_absolute_error` | reports the scoring convention instead of positive MAE |
| changing several modelling choices simultaneously | makes causal attribution of the observed change difficult |
| printing from `compare()` but returning nothing | prevents downstream automation from consuming the result |

## 13. Submission

Submit:

1. `P03_<roll-number>.ipynb`, executed top to bottom with outputs visible;
2. a final three-sentence model-choice justification:
   - which model/configuration you would deploy;
   - why, using evaluation evidence plus at least one operational consideration;
   - what trade-off you accept compared with an alternative.

## 14. Marking

| Component | Marks |
|---|---:|
| Walkthrough completed with outputs visible | 3 |
| T1: overfitting measured as a gap | 2 |
| T2: forest depth selected by development-only CV | 3 |
| T3: reusable CV comparison function | 2 |
| **Total** | **10** |

## 15. MLOps connection

| P03 concept | Later MLOps manifestation |
|---|---|
| repeated model comparison | MLflow experiment runs |
| hyperparameter values | tracked parameters |
| MAE and fold statistics | tracked metrics |
| reusable comparison function | software modules and automated pipelines |
| self-checks | pytest and CI |
| model-selection evidence | governance and promotion decisions |
| untouched final evaluation | release gates and production validation |
| trade-off reasoning | deployment architecture decisions |

## 16. References

- scikit-learn cross-validation: <https://scikit-learn.org/stable/modules/cross_validation.html>
- scikit-learn Decision Trees: <https://scikit-learn.org/stable/modules/tree.html>
- scikit-learn ensemble methods: <https://scikit-learn.org/stable/modules/ensemble.html>
- scikit-learn underfitting and overfitting example: <https://scikit-learn.org/stable/auto_examples/model_selection/plot_underfitting_overfitting.html>

---

**Course design principle:** model selection is part of learning, so the evidence used to select a model must be separated from the evidence reserved for final evaluation.
