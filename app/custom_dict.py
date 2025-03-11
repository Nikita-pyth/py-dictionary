from typing import Any, Hashable

from node import Node


class CustomDict:
    _no_value = object()
    _deleted_marker = object()

    def __init__(self) -> None:
        self.capacity: int = 8
        self.dictionary: list[Node | object | None] = [None] * self.capacity
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
        for i in range(self.capacity):
            index = (cell_to_occupy + i) % self.capacity
            if (
                self.dictionary[index] is None
                or self.dictionary[index] is self._deleted_marker
            ):
                self.dictionary[index] = new_node
                self._used_cells_counter += 1
                break
            elif self.dictionary[index].key == key:
                self.dictionary[index].value = value
                break

        if self._used_cells_counter >= self.threshold:
            self._resize()

    def __getitem__(self, key: Hashable) -> Any:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            index = (index + i) % self.capacity
            if self.dictionary[index] is None:
                break
            if (
                self.dictionary[index] is not self._deleted_marker
                and self.dictionary[index].key == key
            ):
                return self.dictionary[index].value
        raise KeyError(f"Key {key} is not found in the dictionary")

    def __delitem__(self, key: Hashable) -> None:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            index = (index + i) % self.capacity
            if self.dictionary[index] is None:
                break
            if (
                self.dictionary[index] is not self._deleted_marker
                and self.dictionary[index].key == key
            ):
                self.dictionary[index] = self._deleted_marker
                self._used_cells_counter -= 1
                return
        raise KeyError(f"Key {key} is not present in the dictionary."
                       f" Unable to delete.")

    def pop(self, key: Hashable, default: Any = _no_value) -> Any:
        index = hash(key) % self.capacity
        for i in range(self.capacity):
            index = (index + i) % self.capacity
            if self.dictionary[index] is None:
                break
            if (
                self.dictionary[index] is not self._deleted_marker
                and self.dictionary[index].key == key
            ):
                temp = self.dictionary[index].value
                self.dictionary[index] = self._deleted_marker
                self._used_cells_counter -= 1
                return temp
        if default is self._no_value:
            raise KeyError(f"Key {key} is not present in the dictionary."
                           f" Unable to pop.")

        return default

    def _resize(self) -> None:
        old_dict = self.dictionary
        self.capacity *= 2
        self.dictionary = [None] * self.capacity
        self._used_cells_counter = 0
        for node in old_dict:
            if isinstance(node, Node):
                self.__setitem__(node.key, node.value)
