from typing import List

from fastapi import FastAPI
import uvicorn


# This is just to have as an import

from be import BE, Item

from shepherd import Application

app = Application()
be = app.get(BE)  # this one is imported


app = FastAPI()

@app.get("/")
def read_all() -> List[Item]:
    return be.list_all()


i = 0

@app.get("/create")
def create() -> Item:
    global i
    item = Item(item_id=i, name=f"my_item_{i}", price=i)
    i += 1
    new_item = be.create_item(item=item)
    return new_item


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)