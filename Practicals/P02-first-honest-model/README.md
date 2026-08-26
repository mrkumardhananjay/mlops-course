# Practical 02: Your First Honest Model

**SCSE3040 Machine Learning Operations | Bennett University | Session 2026-27**

> Split the data, establish a baseline, train a model, and produce evidence on observations the model did not learn from.

| Item | Detail |
|---|---|
| Follows lecture | L03 |
| Course Outcome | CO2 |
| Duration | 120 minutes |
| Approx. memory | 300 MB |
| GPU required | No |
| Extra software | Nothing beyond the course environment |
| Assessment | 10 marks |

## 1. Why this practical exists

P01 established reproducible execution. P02 establishes the first **evaluation boundary**.

Training a model is not yet evidence that it will work on new observations. A useful experiment must distinguish:

```text
data used to learn
        |
        v
   TRAINING SET
        |
        | model.fit(...)
        v
   FITTED MODEL
        |
        | model.predict(...)
        v
     TEST SET
  (held out during fitting)
```

The central question is not merely:

> Can we train a model?

It is:

> Can we train a model and produce defensible evidence that it performs better than a simple reference strategy on held-out data?

## 2. Learning outcomes

After P02, you should be able to:

- distinguish features from the prediction target;
- explain why training and testing on the same observations is not an honest estimate of generalisation;
- create a reproducible train/test split;
- construct a baseline using **training data only**;
- train a `LinearRegression` model;
- evaluate held-out predictions using MAE and RMSE;
- compare model performance with a baseline;
- interpret linear-regression coefficients cautiously;
- retrain after changing the data split;
- package one-row inference behind a small Python function.

## 3. Starting point

P02 assumes that P01 is complete. In particular, you should already understand:

- the course Python environment;
- random seeds;
- the shared delivery dataset;
- reproducible execution.

The shared dataset contains 600 rows and five columns:

| Column | Role | Meaning |
|---|---|---|
| `distance_km` | feature | delivery distance |
| `prep_time_min` | feature | restaurant preparation time |
| `traffic_level` | feature | coded traffic level, 1 to 3 |
| `rain` | feature | binary indicator, 0 or 1 |
| `delivery_min` | target | observed delivery duration |

## 4. The evaluation contract

Before running a model, establish the rules of the experiment:

```text
Dataset          600 rows
Features         4
Target           delivery_min
Primary split    80% train / 20% test
Split seed       42
Baseline         training-set mean
Primary metric   MAE
Secondary metric RMSE
Model            LinearRegression
```

Recording this context makes the final score interpretable.

---

# Walkthrough

## 5. Pre-flight verification

### RUN

The notebook first checks the Python environment and core imports.

### VERIFY

You should see:

```text
All good. Continue to Step 1.
```

If imports fail, verify `sys.executable` before installing anything.

## 6. Ensure the shared dataset exists

The notebook looks for the shared course CSV and rebuilds it deterministically if it is absent.

### VERIFY

The path should resolve to the course `data/delivery_times.csv`.

This rebuild mechanism is a convenience for the teaching repository. In a production ML system, silently regenerating missing production data would usually be inappropriate. Data acquisition and validation would be explicit pipeline stages.

## 7. Step 1: Load and inspect the data

### RUN

```python
orders = pd.read_csv(DATA)

print("rows, columns:", orders.shape)
print(orders.head())
print(orders.dtypes)
```

### VERIFY

Expected shape:

```text
(600, 5)
```

### STOP AND THINK

Before modelling, answer:

1. What does one row represent?
2. Which columns are available before a delivery is completed?
3. Which column is known only after the delivery completes?
4. Are the coded values for `traffic_level` and `rain` being treated as numbers by the model?

## 8. Step 2: Separate features and target

```python
FEATURES = [
    "distance_km",
    "prep_time_min",
    "traffic_level",
    "rain",
]
TARGET = "delivery_min"

X = orders[FEATURES]
y = orders[TARGET]
```

`X` contains information supplied to the model. `y` contains the outcome the model learns to predict.

### MLOPS CONNECTION

The ordered feature list is already part of an emerging **input contract**. Later, the same contract must be preserved when the model is packaged and served.

## 9. Step 3: Create the evaluation boundary

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)
```

### COMPONENT-WISE

| Component | Meaning |
|---|---|
| `X, y` | aligned feature rows and targets |
| `test_size=0.2` | reserve 20% for held-out evaluation |
| `random_state=42` | make this partition reproducible |
| `X_train, y_train` | observations allowed during fitting |
| `X_test, y_test` | observations withheld from fitting |

### VERIFY

```text
training on: 480 orders
testing on : 120 orders
```

### IMPORTANT

The test set is not "secret forever." It is deliberately withheld during model fitting so it can provide evidence on unseen observations.

Repeatedly using the same test set to choose models or hyperparameters can also leak information into the development process. P03 will address that stronger model-selection problem.

## 10. Step 4: Establish the baseline

Before fitting the regression model, define a simple reference strategy:

> Ignore every feature and always predict the **mean target value from the training set**.

```python
average_time = y_train.mean()
baseline_predictions = np.full(len(y_test), average_time)
baseline_mae = mean_absolute_error(y_test, baseline_predictions)
```

### WHY THE TRAINING MEAN?

Using `y_test.mean()` would allow information from the held-out targets to influence the predictor. The baseline must obey the same evaluation boundary as the model.

### STOP AND THINK

A score such as `MAE = 2.0 minutes` is incomplete without knowing:

- the dataset;
- the evaluation split;
- the metric;
- the baseline or other reference;
- the model/configuration.

## 11. Step 5: Fit Linear Regression

```python
model = LinearRegression()
model.fit(X_train, y_train)
```

`LinearRegression()` creates an unfitted estimator.

`.fit(X_train, y_train)` estimates its parameters using only the training observations.

### VERIFY

After fitting, scikit-learn exposes learned attributes such as:

```python
model.coef_
model.intercept_
```

## 12. Step 6: Evaluate on held-out observations

```python
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
```

### MAE

For \(n\) test observations,

```text
MAE = (1/n) * sum |actual - predicted|
```

MAE is expressed in the target's unit: **minutes**.

### RMSE

```text
RMSE = sqrt((1/n) * sum (actual - predicted)^2)
```

Squaring gives larger residuals more influence before the square root returns the metric to minutes.

Do not infer from `RMSE > MAE` alone that a few catastrophic errors definitely exist. For non-identical absolute residuals, RMSE is generally at least MAE. The size and distribution of residuals must be inspected before making stronger claims about outliers.

### COMPARE WITH THE BASELINE

```python
improvement_pct = 100 * (baseline_mae - mae) / baseline_mae
```

This expresses relative MAE reduction against the chosen baseline.

## 13. Step 7: Inspect what the model learned

Linear regression estimates one coefficient per feature.

```python
learned = pd.DataFrame({
    "feature": FEATURES,
    "coefficient": model.coef_,
})
```

For this synthetic course dataset, the learned values should be close to the coefficients used by the data generator.

### IMPORTANT INTERPRETATION LIMIT

A coefficient is a **model parameter**, not automatically a causal effect.

Within this fitted linear model, a coefficient describes the predicted change associated with one unit of a feature while the other included features are held fixed. Observational modelling alone does not prove causation.

## 14. Step 8: Predict one new order

Use a one-row DataFrame with the same named features:

```python
new_order = pd.DataFrame([{
    "distance_km": 5.0,
    "prep_time_min": 20,
    "traffic_level": 2,
    "rain": 0,
}])

minutes = model.predict(new_order)[0]
```

### WHY A DATAFRAME?

Named columns preserve the feature interface more clearly than an unlabeled list.

This pattern will later become the core of a prediction service.

---

# Your turn

## 15. Task T1: Compare mean and median baselines

Step 4 used the training-set mean.

Build a second baseline that predicts:

```python
y_train.median()
```

for every held-out observation.

Store its MAE in:

```python
T1_median_mae
```

Then store the lower-MAE baseline name in:

```python
T1_which_is_better
```

using exactly `"mean"` or `"median"`.

### STOP AND THINK

If the two scores differ by only a tiny amount, do not exaggerate the practical significance of the difference.

## 16. Task T2: Test sensitivity to another split

Repeat the complete learning experiment with:

```text
test_size = 0.30
random_state = 7
```

Create:

```python
X_tr2, X_te2, y_tr2, y_te2
model2
T2_mae
```

### CRITICAL RULE

A new split requires a **new fitting step**.

Do not evaluate the old `model` as though it had been trained on the new training set.

This second split is a useful sensitivity check, but two hand-selected splits are not a complete model-selection methodology. P03 introduces cross-validation.

## 17. Task T3: Create a single-order prediction interface

Implement:

```python
predict_minutes(
    distance_km,
    prep_time_min,
    traffic_level,
    rain,
)
```

The function must:

1. construct a one-row DataFrame with the correct feature names;
2. call the original fitted `model`;
3. return one plain Python number rounded to one decimal place.

Then evaluate:

```text
distance_km   = 3
prep_time_min = 15
traffic_level = 1
rain          = 1
```

and store the result in:

```python
T3_rainy_order
```

### MLOPS CONNECTION

This function introduces an important separation:

```text
caller inputs
    ↓
feature representation
    ↓
model.predict(...)
    ↓
returned prediction
```

P07 will place essentially this inference boundary behind an HTTP API.

---

# Verification

## 18. Automated self-check

The final notebook cell evaluates nine conditions.

A complete solution reports:

```text
9 of 9 checks passed
```

The self-check validates:

- the median-baseline calculation;
- the baseline comparison;
- the new 70/30 split;
- retraining of `model2`;
- the second split's MAE;
- the prediction function's return type;
- agreement with the trained model;
- the effect of rain for the same synthetic order;
- the requested rainy-order prediction.

## 19. Expected reference observations

With the supplied dataset and reference environment, you should obtain values close to:

```text
Training rows       480
Test rows           120
Baseline MAE        10.32 min
Model MAE            1.92 min
Model RMSE           2.48 min
Relative reduction     81%
```

Small floating-point or dependency-version differences should not be interpreted as conceptual failures.

## 20. Common execution problems

| Symptom | First thing to verify |
|---|---|
| `ModuleNotFoundError` | notebook `sys.executable` |
| `KeyError: 'distance_km'` | dataset path, columns, and Step 1 |
| unexpected split sizes | `test_size` |
| reference metrics differ substantially | dataset identity and `random_state` |
| T2 appears unchanged | confirm a new model was fitted on `X_tr2, y_tr2` |
| feature-name warning | use a DataFrame with the expected columns |
| `NameError` | run prerequisite cells top to bottom |

## 21. Practical completion checklist

- [ ] Environment check passes.
- [ ] Dataset shape is `(600, 5)`.
- [ ] `X` contains four features and `y` contains the target.
- [ ] Primary split contains 480 training and 120 test rows.
- [ ] Baseline uses only the training target distribution.
- [ ] Linear Regression is fitted only on training data.
- [ ] MAE and RMSE are computed on held-out predictions.
- [ ] Model performance is compared with the baseline.
- [ ] Coefficients are interpreted as model parameters, not causal proof.
- [ ] T1 is complete.
- [ ] T2 uses a fresh split and a newly fitted model.
- [ ] T3 returns a plain rounded prediction.
- [ ] Self-check reports `9 of 9 checks passed`.

## 22. Submission

Follow the LMS instructions specified by your instructor.

A typical submission contains:

1. `P02_<roll-number>.ipynb`, executed top to bottom with outputs visible;
2. a final markdown statement reporting whether the model beat the baseline and by how much.

## 23. Marking

| Component | Marks |
|---|---:|
| Walkthrough completed with outputs visible | 3 |
| T1: baseline comparison | 2 |
| T2: retrained alternative split | 2 |
| T3: single-order predictor | 3 |
| **Total** | **10** |

## 24. Connection to P03

P02 establishes:

```text
training data != test data
```

and shows why model performance needs a baseline.

P03 asks a harder question:

> If several models and configurations are available, how can we choose among them without repeatedly using the final test set to make development decisions?

That leads to **overfitting, cross-validation, hyperparameter selection, and defensible model choice**.

## 25. References

Primary references:

- scikit-learn `train_test_split`: <https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html>
- scikit-learn `LinearRegression`: <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html>
- scikit-learn regression metrics: <https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics>

---

**Course design principle:** define the evaluation boundary before interpreting the model score.
