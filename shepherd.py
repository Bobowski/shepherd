from typing import List, Type, TypeVar, Callable
from fastapi import FastAPI
from pydantic import BaseModel, parse_obj_as
from pydantic.json import pydantic_encoder

import uvicorn
import types

import json
import requests


import inspect

# We can add this when we will have to support the http/rpc and others
# We can guess the values right now...

# class Service(BaseModel):
#     uid: str
#     name: str
#     requires: List['Service']
#     type: str


# app = FastAPI()


# def list_services() -> Service:
#     pass


T = TypeVar('T')


def fetcher(url: str, func: Callable):

    sig = inspect.signature(func)
    

    def fetch(self, *args, **kwargs):
        
        # TODO: can we have the same signature as the oriinal function?

        print(self, *args)
        print("asfsd")
        print("Signature", sig)
        ba = sig.bind(self, *args, **kwargs)
        ba.apply_defaults()
        data = ba.arguments
        data.pop("self")

        if len(data) == 1:
            _, data = data.popitem()

        print("Url:", url)
        
        data_pars = json.dumps(data, default=pydantic_encoder)
        print("Data:", data_pars)

        response = requests.post(f"{url}/{func.__name__}", data=data_pars)
        print("Response:", response.json())

        return parse_obj_as(sig.return_annotation, response.json())
    
    return fetch


# TODO: some Protocol here?
class Requester:

    def __init__(self, url: str) -> None:
        self.url = url


class Application:
    def __init__(self) -> None:
        pass

    def get(self, obj: Type[T]) -> T:

        if not inspect.isclass(obj):
            raise ValueError("cls should be a class, nothing else.")

        url = f"http://{obj.__name__}"
        req = Requester(url=url)

        for name, value in inspect.getmembers(obj, inspect.isfunction):
            if name == "__init__":
                continue
            print(name, value)

            setattr(req, name, types.MethodType(fetcher(url, value), req))
            # setattr(req, name, )
            # setattr(req, name, lambda self, *args, **kwargs: print(self, args, kwargs))
        return req


    # def register(self, obj):
    #     pass

from fastapi import APIRouter, FastAPI

def magical_function_server(cls: Type[T], get_self) -> T:

    router = APIRouter()

    for name, value in inspect.getmembers(cls, inspect.isfunction):
        if name == "__init__":
            continue

        print(name, value)

        router.add_api_route(f"/{name}", value, methods=["POST"])
    
    from cbv import _cbv

    clss = _cbv(router, cls, get_self)
    return router



def magical_run(obj: T):
    app = FastAPI()
    cls = obj.__class__
    be_server_router = magical_function_server(cls, get_self=lambda: obj)
    app.include_router(be_server_router)

    uvicorn.run(app, host="0.0.0.0", port=80)


# --------- CLI ---------

import typer
from pathlib import Path
import shutil

app = typer.Typer()

@app.command()
def run(service_files: List[str]):

    print(f"Hello, building for {service_files}")

    here = Path(".")

    files = [x for x in here.glob("*") if x.is_file()]
    if Path("docker-compose.yml") in files:
        files.remove(Path("docker-compose.yml"))

    print(files)

    for sf in service_files:
        dirname = sf.split(".")[0]
        (here / dirname).mkdir(exist_ok=True)
        for file in files:
            shutil.copy(file, dirname)

        shutil.move(here / dirname / sf, here / dirname / 'main.py')

if __name__ == "__main__":
    app()


# philosophy:
# Each service has to be in separate file (ideally in separate directories)

# What about streamlit 
# streamlit run app.py
# how to push backend class to it ?
# if __name__ == "__main__":
#     app = Application() # optional args in constructor - read from envvars otherwise ?
#     be = app.get(Backend) # return fetcher to that object
#     be.do_something()

#     # app.run("streamlit run app.py")


# if __name__ == "__main__":
#     app = Application() # optional args in constructor - read from envvars otherwise ?
#     # app.register() # Register myself
#     db = app.get(Database)
#     something = app.get(Something)

#     app.run(BE(db, something), _as="http_server")


# Decision: It's better atm to use class = service, than object = service. 
#   Because: we should ignore the load-balancing atm, so each service should be only once.

# facade = Facade(fe, fe, fe, fe)... # iframe embedded frame