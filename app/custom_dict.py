from typing import Hashable, Any, Iterator

from app.node import Node


class CustomDict:
    def __init__(self) -> None:
        self.capacity: int = 8
        self.dictionary: list[Node | None] = [None] * self.capacity
        self.load_factor: float = 2 / 3
        self._used_cells_counter: int = 0

    @property
    def threshold(self) -> int:
        return int(self.capacity * self.load_factor)

    def __len__(self) -> int:
        return self._used_cells_counter

    def __setitem__(self, key: Hashable, value: Any) -> None:
        new_node = Node(key, value)
        cell_to_occupy = hash(key) % self.capacity
        if not self.dictionary[cell_to_occupy]:
            self.dictionary[cell_to_occupy] = new_node
            self._used_cells_counter += 1
            return
        elif self.dictionary[cell_to_occupy].key == key:
            self.dictionary[cell_to_occupy].value = value
        else:
            for i in range(self.capacity):
                index = (cell_to_occupy + i) % self.capacity
                if self.dictionary[index] is None:
                    self.dictionary[index] = new_node
                    self._used_cells_counter += 1
                    break

        if self._used_cells_counter >= self.threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            index = (index + i) % self.capacity
            if self.dictionary[index] and self.dictionary[index].key == key:
                return self.dictionary[index].value
        raise KeyError(f"Key {key} is not found in the dictionary")

    def clear(self) -> None:
        self.__init__()

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            index = (index + i) % self.capacity
            if self.dictionary[index] and self.dictionary[index].key == key:
                self.dictionary[index] = None
                self._used_cells_counter -= 1
                return
        raise KeyError(f"Key {key} not in the dictionary"
                       f"unable to delete from the hash table.")

    def get(self, key: Hashable, default: Any = None) -> Any:
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key: Hashable, default: Any = None) -> Any:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            index = (index + i) % self.capacity
            if self.dictionary[index] and self.dictionary[index].key == key:
                temp = self.dictionary[index].value
                self.dictionary[index] = None
                self._used_cells_counter -= 1
                return temp
        if default is None:
            raise KeyError(f"Key {key} not in the dictionary"
                           f"unable to pop from the hash table.")

        return default

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            self.__setitem__(key, value)

    def _resize(self) -> None:
        old_dict = self.dictionary
        self.capacity *= 2
        self.dictionary = [None] * self.capacity
        self._used_cells_counter = 0

        for node in old_dict:
            if node is not None:
                self[node.key] = node.value

    def __iter__(self) -> Iterator:
        for node in self.dictionary:
            if node is not None:
                yield node.key
