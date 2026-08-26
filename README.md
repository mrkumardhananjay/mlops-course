# MLOps Course

A complete, self-contained undergraduate course in Machine Learning Operations.

One project runs through the semester: a delivery-time predictor that evolves from a reproducible local experiment into a versioned, tracked, tested, served, containerised, automated, and monitored ML system.

The emphasis is not only on training a model, but on understanding and engineering everything required to make that model reproducible, traceable, deployable, and maintainable.

Nothing here requires a GPU. The practicals are designed to run on an ordinary laptop with 8 GB of memory.

## What is here

| Folder | Contents |
|---|---|
| `Course/` | Course-level resources, including technical handbooks, course handouts, and supporting documentation |
| `Lectures/` | Lecture-wise teaching material with conceptual explanations, worked examples, exercises, self-checks, glossaries, and guided reading |
| `Practicals/` | Laboratory practicals and executable MLOps exercises, organized progressively so that each practical builds on the previous work |
| `Releases/` | Distribution-ready compiled resources, including released versions of the course manuals and handbooks |

## Course resource architecture

The course deliberately separates conceptual understanding from practical execution.

### MLOps with MLflow Living Manual

The conceptual companion to the course. It develops the internal mechanisms, mental models, reproducibility principles, evaluation discipline, and engineering reasoning behind MLOps.

Its primary question is:

> **Why does this work?**

### MLOps Laboratory Handbook

The execution companion to the course. It provides detailed practical procedures, commands, code, expected observations, interpretation checkpoints, troubleshooting guidance, and verification steps.

Its primary question is:

> **How do I execute it correctly?**

### Lecture Handouts

Lecture-specific resources connect classroom discussion with the broader conceptual manual and laboratory progression.

Distribution-ready versions of major course resources are maintained under `Releases/`.

## The arc

The semester follows one continuously evolving ML system:

**reproducible environment → versioned data → honest evaluation → tested package → tracked experiments → model lifecycle → served model → container → composed stack → automated pipeline → monitoring**

Nothing is thrown away simply because a practical has ended. Each stage builds on engineering decisions and artifacts created earlier.

This progression is deliberate: students experience MLOps as the lifecycle of a system rather than as a collection of unrelated tools.

## Who this is for

Students who can train a machine-learning model but cannot yet hand that model to someone else and confidently expect it to reproduce, run, and remain understandable.

It is also intended for instructors looking to teach the engineering around machine learning rather than treating MLOps as a sequence of software demonstrations.

## Approach

The course follows several principles:

- build the mental model before introducing the abstraction;
- verify execution context rather than assume it;
- make experiments reproducible before making them sophisticated;
- distinguish training performance from evidence of generalisation;
- treat data, code, environment, parameters, metrics, and artifacts as parts of the experimental record;
- introduce tools when an engineering problem creates the need for them;
- prefer primary sources when documenting technical claims; and
- use one evolving project to expose the relationships between different stages of the ML lifecycle.

Tooling is deliberately focused. Tools will change; the engineering discipline should transfer.

## Status

Under active development.

The conceptual manual, lecture material, and laboratory sequence evolve with the course. Stable distribution-ready versions are published under `Releases/`.

## License

To be added.
