# Practical 04: From Notebook to Package

**Turn scattered notebook cells into reusable Python modules and command-line programs.**

SCSE3040 Machine Learning Operations  
Bennett University | Session 2026-27

## Practical goal

In P01-P03, the machine-learning workflow still depended heavily on notebook state. In this practical, that workflow is refactored into an importable Python package.

By the end of P04, you will be able to:

- explain why hidden notebook state is dangerous for reproducibility;
- separate data, feature, and model responsibilities into Python modules;
- create and import a project-local package;
- persist a trained model with `joblib`;
- write a training entry-point script;
- execute the workflow from the command line;
- interpret process exit codes;
- extend the package through three assessed programming tasks.

## Prerequisites

Complete P01-P03 first. You should already understand:

- reproducible environments;
- the shared delivery-time dataset;
- train/test separation;
- MAE;
- Python functions and imports.

No GPU is required.

## Files in this public practical

```text
P04-from-notebook-to-package/
├── P04.ipynb
├── README.md
├── requirements.txt
└── .gitignore
```

The notebook creates the working package during execution. Completed `work/`
outputs and faculty solutions are intentionally not included in the public
problem package.

## What you will build

During the walkthrough, your notebook progressively creates:

```text
work/
├── delivery/
│   ├── __init__.py
│   ├── data.py
│   ├── features.py
│   ├── model.py
│   └── validate.py        # student task
├── train.py
├── predict.py             # student task
└── model.joblib
```

Each module has one primary responsibility.

## Recommended execution

From the course virtual environment:

```powershell
jupyter notebook P04.ipynb
```

Run the notebook from top to bottom.

If notebook state becomes confusing, restart the kernel, clear outputs, and run
again from the first cell.

## Student tasks

### T1: Extend the feature module

Add:

```python
average_speed_kmph(distance_km, delivery_min)
```

to `delivery/features.py`.

For 10 km completed in 30 minutes, the function should return `20.0`.

### T2: Add input validation

Create `delivery/validate.py` containing:

```python
is_valid_order(order)
```

An order is valid only when:

- `distance_km > 0`
- `prep_time_min >= 0`
- `traffic_level` is 1, 2, or 3
- `rain` is 0 or 1

### T3: Create a prediction command

Create `work/predict.py`.

It must load the persisted model and print one prediction for the order
specified in the notebook. Its output must begin with:

```text
PREDICTION:
```

## Self-check

The notebook contains an automated self-check with **9 conditions** covering
T1, T2, and T3.

A completed implementation should report:

```text
9 of 9 checks passed
```

Use the self-check as feedback, not as a substitute for understanding why each
module and command works.

## Submission

Submit:

1. the completed notebook with outputs visible;
2. the `work/delivery/` package you created, zipped;
3. the requested one-sentence responsibility description for each module.

Follow your instructor's naming convention for the notebook.

## Why P04 matters in MLOps

A notebook is excellent for exploration, but downstream systems need reusable,
importable, executable software. Tests, services, containers, scheduled jobs,
and CI/CD pipelines operate on modules and programs rather than interactive
notebook state.

P04 therefore forms the engineering bridge between experimental ML and the
software structure used in later practicals.

## Next practical

P05 will test the package created here. The quality of the module boundaries
introduced in P04 directly affects how easy the system is to test and automate.

## References

- Python documentation: Modules
- Python documentation: The module search path
- joblib documentation: Persistence
- scikit-learn documentation: Model persistence

The detailed step-by-step explanation is provided in the course Practical 04
manual. This repository package remains the executable student problem.
