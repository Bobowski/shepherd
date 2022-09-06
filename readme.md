# Rapid prototyping, quick iteration microservice framework ...

Keep in mind that this is still a very early iteration of the framework... ;D 


The idea is to allow users to focus on the core functionality of the microservice system rather
than dealing with network and communication between them

Why not just monolyth architecture?
Well, if you're doing anything that requires a dedicated machine for some computations
like ML magic, then you'll need to have a separate machine for that.
So this way we can just focus one the nice and easy stuff first. 


# Run

Example explanation:
We have a BE and FE service (`be.py` and `fe.py` files), but we do not really want to bother with network communication between them.
Backend (be.py) is modeled via class and then using `magical_run` we make it into an HTTP server.
Method aguments need to be pydantic models (derived vrom BaseModel) to make it work atm.

In Frontend we have 2 methods, list and create. That's just a simple behaviour to see if the connection is actually there. Nothing fancy. We will experiment with things like streamlit next (probably).
The magic happens here:
```
app = Application()
be = app.get(BE)
```
as what's actually hapening is the `BE` class get's translated into `Requester` that has the same methods as `BE` but actually does HTTP requests. So network + object parsing is hidden away - that's cool.


```
# checkout repository
git clone ...

# install requirements (you might want to create a separate venv first...)
pip install -r requirements.txt

# Run shepherd (creates dedicated directories per service)
python shepherd.py fe.py be.py

# build and run locally with docker-compose
docker-compose up --build

# to stop, simply CTRL+C:
```


## Notes

- We know that atm there are all files in the same dictionary, it's messy but it's what we ahve atm.
- Not whole process is streamlined yet, that is still tbd. Don't worry. We just create a dedicated directories for docker stuff atm.