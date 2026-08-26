# Practical 01: Building a Reproducible MLOps Workbench

**SCSE3040 Machine Learning Operations | Bennett University | Session 2026-27**

> A reliable ML workflow starts before model training. This practical establishes the execution, dependency, randomness, data, and source-control habits that every later practical assumes.

| Item | Detail |
|---|---|
| Follows lectures | L01-L02 |
| Course Outcome | CO1 |
| Duration | 120 minutes |
| Approx. memory | 250 MB |
| GPU required | No |
| Extra software | Git and the course Python environment |
| Assessment | 10 marks |

## 1. Why this practical exists

A notebook that runs once on one laptop is not yet a reproducible ML workflow.

To reproduce an experiment later, we need evidence about the conditions that produced it. In this practical you will build five such controls:

1. **Execution identity**: which Python interpreter actually runs the notebook?
2. **Dependency identity**: which library versions are installed?
3. **Stochastic identity**: which random seed controls repeatable pseudo-random operations?
4. **Data identity**: can we prove that two generated files contain the same bytes?
5. **Source identity**: which Git revision contains the work?

These controls do not guarantee that every numerical result will be bit-for-bit identical across every operating system, processor, Python build, or library implementation. They do provide the minimum reproducibility evidence expected from a disciplined ML workflow.

## 2. Learning outcomes

After completing P01, you should be able to:

- verify the Python interpreter used by a notebook;
- inspect installed package versions from the running interpreter;
- create a pinned requirements file using exact package versions;
- explain what a pseudo-random seed controls;
- generate deterministic course data from a known seed;
- compute and compare SHA-256 fingerprints;
- record a small experiment manifest;
- inspect Git provenance without creating a nested repository;
- complete and interpret automated self-checks.

## 3. What you will produce

By the end of the practical, your working directory will contain files similar to:

```text
P01-reproducible-ml-workbench/
├── P01.ipynb
├── README.md
├── requirements.txt
├── .gitignore
└── work/
    ├── requirements.txt
    ├── my_requirements.txt
    ├── run_a.csv
    ├── run_b.csv
    └── run_info.json
```

The `work/` directory contains generated learning artifacts. It is intentionally ignored by Git in the public course repository so that repeated executions do not pollute source history.

## 4. Prerequisites

Before starting, verify that:

- Python 3.12 or newer is installed;
- the course virtual environment has been created;
- Jupyter is using the course kernel;
- Git is installed and available on `PATH`;
- the repository has been cloned locally.

For Windows PowerShell, from the repository root:

```powershell
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
git --version
```

The interpreter path should point into the repository's `.venv`.

### Why verify before debugging?

A missing import can be caused by the wrong Python rather than by a missing package. Always establish the execution context first.

## 5. Start the notebook

From the practical directory:

```powershell
python -m jupyter lab P01.ipynb
```

If your environment is not activated, use the project-local interpreter explicitly.

Example from a practical nested two levels below the repository root:

```powershell
..\..\.venv\Scripts\python -m jupyter lab P01.ipynb
```

Run cells **top to bottom** with `Shift + Enter`.

If notebook state becomes confusing, use:

**Kernel > Restart Kernel and Clear All Outputs**

and start again from the first cell.

---

# Walkthrough

## 6. Pre-flight check

### RUN

The first notebook cell reports the Python version, working folder, and whether core libraries can be imported.

### VERIFY

You should see the final line:

```text
All good. You can carry on to Step 1.
```

### STOP AND THINK

If NumPy is installed in `.venv` but Jupyter still reports `ModuleNotFoundError`, what is the first thing you should verify?

**Answer to reason toward:** the notebook kernel may be using a different Python interpreter.

---

## 7. Step 1: Identify the executing Python

### RUN

Inside the notebook:

```python
import sys
from pathlib import Path

print("Python version :", sys.version.split()[0])
print("Python program :", sys.executable)
print("Working folder :", Path.cwd())
```

### UNDERSTAND

`sys.executable` is stronger evidence than the notebook's visible kernel label. It reports the executable of the Python process actually evaluating the cell.

### VERIFY

The path should resolve into the course `.venv`.

### MLOPS CONNECTION

A reproducible run needs execution identity. "Python worked" is not enough when several Python installations may exist on the same machine.

---

## 8. Step 2: Inspect dependency versions

### RUN

```python
from importlib.metadata import version

LIBRARIES = [
    "numpy",
    "pandas",
    "scikit-learn",
    "matplotlib",
]

for name in LIBRARIES:
    print(f"{name:<15} {version(name)}")
```

### UNDERSTAND

The package name identifies *what* dependency is required. The version identifies *which release* supplied the behavior used by the experiment.

### STOP AND THINK

Compare:

```text
numpy
```

with:

```text
numpy==2.5.1
```

The first allows version resolution at installation time. The second requests one exact version.

---

## 9. Step 3: Capture a pinned dependency record

The notebook creates:

```text
work/requirements.txt
```

with one `name==version` entry per selected library.

### REBUILD PATTERN

From the directory containing the file:

```powershell
python -m pip install -r requirements.txt
```

Using `python -m pip` explicitly ties pip to the Python interpreter you selected.

### IMPORTANT LIMITATION

A Python requirements file records Python package requirements. It does **not** by itself capture every reproducibility condition such as:

- operating-system libraries;
- environment variables;
- Python build details;
- CPU/GPU architecture;
- external services;
- container/runtime configuration.

Later practicals will progressively capture more of this execution context.

---

## 10. Step 4: Observe uncontrolled randomness

### RUN TWICE

```python
import numpy as np

rng = np.random.default_rng()
print(np.round(rng.uniform(0, 10, 3), 2))
```

You should normally observe different values between executions because no explicit seed was supplied.

### STOP AND THINK

Different random values are not a bug. The question is whether the experiment requires variability or repeatability.

---

## 11. Step 5: Control pseudo-randomness with a seed

### RUN

```python
first = np.random.default_rng(42).uniform(0, 10, 3)
second = np.random.default_rng(42).uniform(0, 10, 3)

print(np.array_equal(first, second))
```

Expected result:

```text
True
```

### UNDERSTAND

A seed does not "turn randomness off." It selects a reproducible initial state for a pseudo-random generator.

For the same generator implementation and software context, the same seed allows the same pseudo-random sequence to be reproduced.

### MLOPS CONNECTION

Seeds matter in operations such as:

- train/test splitting;
- shuffling;
- bootstrapping;
- randomized models;
- sampling;
- some optimization procedures.

Each stochastic component must be controlled where repeatability is required.

---

## 12. Step 6: Generate the delivery dataset twice

The notebook generates two independent CSV files with the same generator and seed:

```text
work/run_a.csv
work/run_b.csv
```

Then it computes SHA-256 for both.

### VERIFY

You should see:

```text
identical files: True
```

### UNDERSTAND

The equality is stronger than saying the tables "look the same." Matching full SHA-256 digests provide extremely strong evidence that the files contain identical bytes.

A hash is an identifier derived from content. It is not a copy of the dataset and cannot reconstruct the dataset.

---

## 13. Step 7: Inspect the generated data

The shared course dataset contains 600 delivery records and five columns:

| Column | Meaning |
|---|---|
| `distance_km` | delivery distance in kilometres |
| `prep_time_min` | restaurant preparation time |
| `traffic_level` | coded traffic level, 1 to 3 |
| `rain` | binary indicator, 0 or 1 |
| `delivery_min` | observed delivery duration |

### VERIFY

```python
orders.shape
```

should report:

```text
(600, 5)
```

Before fitting a model, always know what one row means, what each field means, and which value will eventually become the prediction target.

---

## 14. Step 8: Record run provenance

The notebook writes:

```text
work/run_info.json
```

containing:

- Python version;
- operating platform;
- seed;
- row count;
- data SHA-256;
- package versions;
- Git commit, when available.

This small JSON file is an early form of an **experiment manifest**.

### MLOPS CONNECTION

Later MLflow runs will automate much of this recording. P01 deliberately makes the information visible first so that experiment tracking does not become a black box.

---

## 15. Step 9: Inspect Git provenance

The public repository edition does **not** initialize another `.git` directory inside `work/`.

Nested repositories are unnecessary here because the course itself is already a Git repository.

### RUN IN A TERMINAL

From anywhere inside the cloned course repository:

```powershell
git status
git rev-parse --show-toplevel
git log -1 --oneline
```

### COMPONENT-WISE MEANING

| Command | Purpose |
|---|---|
| `git status` | shows uncommitted working-tree changes |
| `git rev-parse --show-toplevel` | identifies the root of the current repository |
| `git log -1 --oneline` | shows the latest commit in compact form |

### COMMIT YOUR OWN WORK

When your instructor asks you to save your practical progress:

```powershell
git add Practicals/P01-reproducible-ml-workbench/P01.ipynb
git commit -m "P01: complete reproducibility workbench"
```

Adjust the path if your local repository uses a different folder hierarchy.

Do not commit generated caches, `.venv`, or notebook runtime clutter.

---

# Your turn

## 16. Task T1: Change the seed

The dataset uses seed `42`.

Use seed `7` to generate 600 values from a uniform distribution between `0.5` and `12.0`, round them to two decimal places, and store the first three values in:

```python
T1_first_three
```

### Progressive hint

1. Create a generator with `np.random.default_rng(7)`.
2. Call `.uniform(0.5, 12.0, 600)`.
3. Round with `np.round(..., 2)`.
4. Slice the first three values.
5. Convert them to a plain Python list.

---

## 17. Task T2: Build your own pinned requirements file

Create:

```text
work/my_requirements.txt
```

containing exactly these three packages:

```text
numpy
pandas
scikit-learn
```

Each line must use the exact version installed in the current interpreter:

```text
name==version
```

Do not type version numbers manually.

### VERIFY

Your file should contain exactly three non-empty lines, and each recorded version should equal `importlib.metadata.version(name)`.

---

## 18. Task T3: Fingerprint a run

Implement:

```python
fingerprint(path)
```

so that it returns exactly:

```python
{
    "rows": ...,
    "sha256": ...,
    "seed": ...
}
```

Requirements:

- `rows` counts data rows, not the CSV header;
- `sha256` is the complete 64-character SHA-256 digest;
- `seed` uses the practical's `SEED` value.

Store the result for the shared course data in:

```python
T3_fp
```

---

## 19. Automated self-check

Run the final notebook self-check.

A complete solution should report:

```text
7 of 7 checks passed
```

The checks validate behavior, not just whether variables happen to exist.

If a check fails:

1. read the exact failed condition;
2. fix only the corresponding task;
3. re-run the task cell;
4. re-run the self-check.

---

# Troubleshooting

## 20. Common failures

| Symptom | Likely cause | What to verify |
|---|---|---|
| `Inside .venv: False` | wrong notebook kernel | `sys.executable` |
| `ModuleNotFoundError` | notebook and terminal use different Python environments | compare notebook `sys.executable` with terminal Python |
| `NameError: WORK is not defined` | earlier cells were skipped | restart and run top to bottom |
| generated hashes differ | seed or generation logic changed | confirm both calls use the same generator logic and seed |
| T2 fails although file exists | versions or formatting do not match installed packages | inspect all three lines |
| Git command fails | Git is not installed or current directory is outside a repository | `git --version`, `git rev-parse --show-toplevel` |
| notebook output seems stale | cell was edited after being executed | re-run the edited cell and dependent cells |

## 21. Diagnostic order

When something goes wrong, investigate in this order:

```text
working directory
    ↓
Python interpreter / Jupyter kernel
    ↓
installed dependencies
    ↓
dataset and generated files
    ↓
task code
```

Do not start rewriting ML code before the execution context has been verified.

---

# Repository hygiene

## 22. What belongs in Git

Commit source and teaching artifacts such as:

```text
README.md
P01.ipynb
requirements.txt
.gitignore
```

Depending on instructor policy, a student may also commit a completed notebook in their own fork/branch.

## 23. What should not be committed

The provided `.gitignore` excludes common runtime/generated material, including:

```text
.venv/
__pycache__/
.pytest_cache/
.ipynb_checkpoints/
work/
*.pyc
```

Generated files can be reproduced from the notebook and do not need to be stored in the public course source.

---

# Completion

## 24. Practical completion checklist

Before considering P01 complete:

- [ ] `sys.executable` points to the intended course environment.
- [ ] package versions are visible.
- [ ] `work/requirements.txt` contains pinned versions.
- [ ] the unseeded demonstration changes between runs.
- [ ] the seeded demonstration repeats.
- [ ] `run_a.csv` and `run_b.csv` have matching SHA-256 fingerprints.
- [ ] the shared dataset has shape `(600, 5)`.
- [ ] `run_info.json` has been created.
- [ ] Git repository identity can be inspected.
- [ ] T1 is complete.
- [ ] T2 is complete.
- [ ] T3 is complete.
- [ ] the self-check reports `7 of 7 checks passed`.

## 25. What to submit

Follow your instructor's LMS submission policy. A typical submission includes:

1. `P01_<roll-number>.ipynb`, executed top to bottom with outputs visible;
2. `work/my_requirements.txt`;
3. any evidence specifically requested by the instructor.

Do not upload `.venv`, caches, or nested `.git` directories.

## 26. Marking

| Component | Marks |
|---|---:|
| Walkthrough completed with outputs visible | 3 |
| T1: controlled randomness | 2 |
| T2: pinned requirements | 2 |
| T3: run fingerprint | 3 |
| **Total** | **10** |

## 27. Connection to P02

P01 establishes the evidence needed to trust the environment in which an experiment runs.

P02 will add the next boundary:

> **Can we train a model and evaluate it honestly on observations it did not learn from?**

That moves the project from **reproducible execution** to **reproducible evaluation**.

## 28. References

Primary references:

- Python documentation, virtual environments and packages: <https://docs.python.org/3/tutorial/venv.html>
- pip documentation, requirements file format: <https://pip.pypa.io/en/stable/reference/requirements-file-format/>
- NumPy documentation, random generator: <https://numpy.org/doc/stable/reference/random/generator.html>
- Python documentation, `hashlib`: <https://docs.python.org/3/library/hashlib.html>
- Pro Git: <https://git-scm.com/book/en/v2>

---

**Course design principle:** understand the mechanism, execute the step, verify the state, then connect it to the MLOps lifecycle.
