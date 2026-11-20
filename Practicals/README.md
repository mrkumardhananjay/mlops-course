# SCSE3040 Lab Practicals

**Machine Learning Operations | B.Tech CSE Semester V | Bennett University | Odd Semester 2026-27**

Thirteen practicals, all building one running project: a food delivery time predictor. Each picks up where the last one stopped, so the arc across the semester is

> notebook, package, tracked experiments, API, container, cluster, logs, automated pipeline, monitoring

## The practicals

| # | Practical | Follows lectures | BTLAP lab | CO | Time | Extra software |
|---|---|---|---|---|---|---|
| P01 | [Your MLOps Workbench](P01-reproducible-ml-workbench/) | L01-L02 | Lab 1 | CO1 | 120 min | Git |
| P02 | [Your First Honest Model](P02-first-honest-model/) | L03 | Lab 4 | CO2 | 120 min | none |
| P03 | [Choosing a Model Honestly](P03-choosing-model-honestly/) | L04 | Lab 4 | CO2 | 120 min | none |
| P04 | [From Notebook to Package](P04-from-notebook-to-package/) | L09 | Lab 5 | CO3 | 120 min | none |
| P05 | [Settings in a File, Bugs Caught by a Robot](P05-settings-and-tests/) | L10 | Lab 5 | CO3 | 120 min | none |
| P06 | [Remembering Every Experiment](P06-remembering-every-experiment/) | L11-L12 | Lab 6, Lab 7 | CO5 | 120 min | none |
| P07 | [Putting the Model Behind an Address](P07-model-behind-an-address/) | L13-L14 | Lab 8 | CO4 | 120 min | none |
| P08 | [Packing the Service into a Container](P08-packing-into-a-container/) | L17-L18 | Lab 9 | CO3 | 120 min | **Docker Desktop** |
| P09 | [Describing the Service to a Cluster](P09-describing-to-a-cluster/) | L22 | Lab 10 | CO4 | 120 min | none |
| P10 | [Logs You Can Actually Search](P10-logs-you-can-search/) | L21 | Lab 10 | CO5 | 120 min | none |
| P11 | [A Robot That Checks Your Work](P11-a-robot-that-checks/) | L24-L25 | Lab 11 | CO4 | 120 min | none |
| P12 | [A Pipeline You Can Re-run](P12-a-pipeline-you-can-rerun/) | L26 | Lab 12 | CO4 | 120 min | none |
| P13 | [Watching a Model Get Worse](P13-watching-a-model-get-worse/) | L27-L28 | Lab 13 | CO5 | 120 min | none |

Only **P08** needs anything beyond the course Python environment. **P09** runs real `kubectl` commands if a cluster happens to be available, and every graded task in it works without one.

### A note on the two numbering schemes

The approved plan (BTLAP) numbers these Lab 1 to Lab 13, with Lab 14 and Lab 15 reserved as buffer labs. The folders here use P01 to P13, which is the numbering the lab materials themselves use. The two sequences are not identical, so the **BTLAP lab** column above is the mapping. Where one practical satisfies two plan labs, both are listed.

Two plan labs have no practical of their own in this set: **Lab 2, collaborative Git**, and **Lab 3, data versioning with DVC**. Those topics are taught in L05 and L06 and are exercised inside P01 rather than as separate practicals.

## How a practical works

Every notebook has the same three parts, in this order.

1. **Walkthrough.** Numbered steps you read and run. It works as shipped, so it can be projected and demonstrated. Nothing here can be got wrong.
2. **Your turn.** Three tasks, each with a `# TODO` stub and a hint. Do them in order; they get harder.
3. **Self-check.** One cell that marks your work and prints a PASS or FAIL table. Run it as often as you like. It never breaks your notebook, and a task you have not started simply shows FAIL.

## Running one

```bash
cd Practicals/P01-reproducible-ml-workbench
jupyter lab P01.ipynb
```

Open the notebook from inside its own folder. Every notebook locates the shared dataset by walking upward until it finds `data/delivery_times.csv`, so it also works if you launch Jupyter from `Practicals/` or from the repository root.

## The shared dataset

`data/delivery_times.csv`, 600 delivery orders, five columns:

| Column | Meaning |
|---|---|
| `distance_km` | Distance from restaurant to customer |
| `prep_time_min` | Minutes the kitchen took |
| `traffic_level` | 1 light, 2 moderate, 3 heavy |
| `rain` | 0 dry, 1 wet |
| `delivery_min` | The true delivery time, the target |

Every practical uses this one file. Do not edit it. Anything a practical generates belongs in that practical's `work/` folder, which `.gitignore` already keeps out of the repository.

## What is deliberately not committed

`mlruns/`, `mlflow.db`, `__pycache__/`, `.ipynb_checkpoints/`, `*.joblib` and `*.skops`. These are produced when you run a practical. If you find them in a clone, something has gone wrong.
