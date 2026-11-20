# Practical 07 --- Putting the Model Behind an Address

*A prediction service with FastAPI, input validation, and automatic docs*

SCSE3040 Machine Learning Operations · Bennett University · Session 2026-27

| | |
|---|---|
| Follows lectures | L13-L14 |
| Course Outcome | CO4 |
| Duration | 120 minutes |
| Peak memory | ~450 MB |
| Extra software | nothing beyond the course venv |
| Marks | 10 |

## Aim

1. Explain why a trained model is useless until something can call it.
2. Build a small web service with a /health and a /predict endpoint.
3. Let the framework reject bad input for you, before your code runs.
4. Test the whole service from Python, without starting a server.

## Before you start

- Practical P04 is finished. You can write a module and save a model.
- You know what a dictionary is. You do not need any web experience.

## Background


Your model currently lives inside a notebook on your laptop. A food delivery
app cannot open your notebook. It needs to *ask* for a prediction and get an
answer back, from anywhere, at any time.

The way software asks other software for things is an **API** (Application
Programming Interface). For services on a network, the usual style is **REST**,
and the pieces are simple:

- an **endpoint** is an address, such as `/predict`
- a **method** says what you want: `GET` to fetch something, `POST` to send
  something and get a result
- the body of the message is usually **JSON** (JavaScript Object Notation), a
  plain-text format of keys and values that looks like a Python dictionary
- the reply carries a **status code**: `200` means fine, `422` means your input
  was unacceptable, `500` means the service itself broke

**FastAPI** is the Python framework we use. Three things make it right for
machine learning. It is fast. It checks incoming data for you and rejects bad
requests before your code ever sees them. And it writes its own documentation
page, which you get for free.

That middle point matters more than it sounds. A model given `traffic_level=9`
when it was trained on 1 to 3 will not crash --- it will return a confident,
wrong number. Rejecting impossible input at the door is the cheapest safety you
will ever add.

Today you also learn to test a service **without running a server**. FastAPI
gives you a `TestClient` that calls your app directly, in the same process. No
ports, no browser, nothing to leave running by mistake --- and it works
identically inside an automated pipeline, which is where P11 will use it.


## What you will do

1. **Train a model and save it**
2. **Describe what a valid order looks like**
3. **Write the service**
4. **Load the service without starting a server**
5. **Ask it whether it is alive**
6. **Ask it for a prediction**
7. **Watch it refuse bad input**
8. **The documentation you did not write**
9. **Run it for real, in a terminal**

## Your turn

- **T1 --- Add an endpoint that describes the model.** Add a new endpoint `GET /model-info` to `work/app.py`. It must return a
- **T2 --- Compare two orders through the service.** Using `client.post`, ask the service for two predictions:
- **T3 --- Refuse an order nobody could deliver.** The service currently accepts a distance of 50 km. Our riders never go

## What to submit

1. This notebook, with every cell run and its output visible.
2. Your `work/app.py`.
3. A screenshot of `http://127.0.0.1:8000/docs` showing a successful prediction in the Response body panel.

## Marking

| What is marked | Marks |
|---|---|
| Walkthrough run end to end, service answers requests | 3 |
| Task T1 --- a new endpoint added | 2 |
| Task T2 --- predictions requested and compared | 2 |
| Task T3 --- validation tightened and proven | 3 |
| **Total** | **10** |

## Read more

- FastAPI --- First steps --- <https://fastapi.tiangolo.com/tutorial/first-steps/>
- FastAPI --- Request body and pydantic models --- <https://fastapi.tiangolo.com/tutorial/body/>
- FastAPI --- Testing with TestClient --- <https://fastapi.tiangolo.com/tutorial/testing/>
- Pydantic --- Field constraints --- <https://docs.pydantic.dev/latest/concepts/fields/>
- MDN --- HTTP response status codes --- <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status>

---

*Open `P07.ipynb` in Jupyter and work through it top to bottom.
The notebook contains everything in this handout, plus the code.*
