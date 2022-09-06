from typing import List, Optional

from pydantic import BaseModel


class Item(BaseModel):
    item_id: int
    name: str
    price: int


class BE:
    def __init__(self) -> None:
        print("Initialized Back-End!")
        self.db = {}

    def list_all(self) -> List[Item]:
        print("List all:", list(self.db.values()))
        return list(self.db.values())

    def get_item(self, item_id: int) -> Optional[Item]:
        print("Get Item:", self.db.get(item_id))
        return self.db.get(item_id)

    def create_item(self, item: Item) -> Item:
        self.db[item.item_id] = item
        print("List all after create:", list(self.db.values()))
        return item


if __name__ == "__main__":
    from shepherd import magical_run

    be = BE()
    be.create_item(item=Item(item_id=42, name="Math", price=4242))

    magical_run(be)
