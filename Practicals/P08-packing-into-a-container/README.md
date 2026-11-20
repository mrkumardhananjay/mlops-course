# Practical 08 --- Packing the Service into a Container

*A Dockerfile, an image, and a service that runs the same everywhere*

SCSE3040 Machine Learning Operations · Bennett University · Session 2026-27

| | |
|---|---|
| Follows lectures | L17-L18 |
| Course Outcome | CO3 |
| Duration | 120 minutes |
| Peak memory | ~900 MB |
| Extra software | Docker Desktop |
| Marks | 10 |

## Aim

1. Explain what a container gives you that a virtual environment cannot.
2. Write a Dockerfile for the delivery-time service.
3. Build an image and run it, then call the service inside it.
4. Read a container's logs and shut it down cleanly.

## Before you start

- **Docker Desktop must be installed and running before this lab.** See `labs/SETUP.md`. Check it by opening a terminal and typing `docker version` --- you should see both a Client and a Server section.
- Practical P07 is finished. You have a working FastAPI service.
- Close other heavy programs. Docker Desktop wants about 2 GB on its own.

## Background


In P01 you pinned your library versions so a colleague could rebuild your
environment. That solves half the problem. It does not pin the Python version,
the operating system, the system libraries underneath, or the twenty small
things your laptop happens to have installed.

A **container** pins all of it. It is a sealed box holding your code, your
libraries, and a minimal operating system --- everything except the kernel
itself. The same box runs identically on your laptop, on your teacher's laptop
and on a server in Mumbai.

Three words you need.

An **image** is the box, built once and stored. A **container** is a running
copy of an image. One image, many containers --- exactly like one class and
many objects.

A **Dockerfile** is the recipe that builds the image. It is a plain text file of
instructions read from top to bottom: start from this base, copy these files,
run this command.

The one idea that separates people who find Docker fast from people who find it
slow is **layers**. Every instruction in a Dockerfile creates a layer, and
Docker caches them. If nothing above a layer changed, it is reused instantly.
This is why you copy `requirements.txt` and install libraries *before* you copy
your code: your code changes twenty times a day, your libraries change twice a
month. Get that order wrong and every rebuild reinstalls everything.

The Indian analogy your lectures used: a container is a packed tiffin. It does
not care whose kitchen it is opened in, because it brought everything with it.


## What you will do

1. **Check Docker is running before anything else**
2. **A helper for running Docker commands**
3. **Gather what goes in the box**
4. **Write the Dockerfile**
5. **Tell Docker what to ignore**
6. **Build the image**
7. **Look at what you built**
8. **Run it**
9. **Talk to the service inside the container**
10. **Read its logs, then stop it**

## Your turn

- **T1 --- Keep the rubbish out of your image.** Write a **new** file `work/.dockerignore.mine` that excludes all of the
- **T2 --- Fix a broken Dockerfile.** Below is a Dockerfile with **three** faults. Find them and write a
- **T3 --- Rebuild and serve a rainy order.** **This task needs Docker running.**

## What to submit

1. This notebook, with every cell run and its output visible.
2. Your `work/Dockerfile` and `work/.dockerignore`.
3. A screenshot of the output of `docker images delivery-api:1.0` showing the size.

## Marking

| What is marked | Marks |
|---|---|
| Walkthrough run end to end, image built and container answered | 3 |
| Task T1 --- a correct .dockerignore | 2 |
| Task T2 --- the broken Dockerfile diagnosed and fixed | 3 |
| Task T3 --- a rebuilt image serving a prediction | 2 |
| **Total** | **10** |

## Read more

- Docker --- Dockerfile reference --- <https://docs.docker.com/reference/dockerfile/>
- Docker --- Building best practices --- <https://docs.docker.com/build/building/best-practices/>
- Docker --- .dockerignore file --- <https://docs.docker.com/build/concepts/context/#dockerignore-files>
- Docker Hub --- the official python image --- <https://hub.docker.com/_/python>

---

*Open `P08.ipynb` in Jupyter and work through it top to bottom.
The notebook contains everything in this handout, plus the code.*
