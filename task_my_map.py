import sys


class MyMap:

    __TOMBSTONE: object = object()
    __INIT_CAPACITY: int = 16
    __LOAD_FACTOR: float = 0.7
    __RESIZE_FACTOR: int = 2

    def __init__(self):
        self.pairs: list[tuple[str, int] | None | object] = (
                [None] * MyMap.__INIT_CAPACITY)
        self.capacity: int = MyMap.__INIT_CAPACITY
        self.size: int = 0
        self.tomb_count: int = 0

    def put(self, key: str, value: int) -> None:
        idx: int = self.__calc_key_hash(key) % self.capacity
        first_tomb_idx: int | None = None

        # Вставка новой пары
        if self.pairs[idx] is None:
            self.pairs[idx] = (key, value)
            self.size += 1

        # Обновление значения по ключу
        elif self.pairs[idx] is not MyMap.__TOMBSTONE and self.pairs[idx][0] == key:
            self.pairs[idx] = (key, value)

        # Коллизия индексов
        else:
            # Сохраняем место первого попавшегося Томба
            if first_tomb_idx is None and self.pairs[idx] is MyMap.__TOMBSTONE:
                first_tomb_idx = idx

            # Открытая адресация по следующим ячейкам
            for i in range(1, self.capacity):
                idx = (idx + 1) % self.capacity

                # Сохраняем место первого попавшегося Томба
                if first_tomb_idx is None and self.pairs[idx] is MyMap.__TOMBSTONE:
                    first_tomb_idx = idx

                # Нашли пустую ячейку
                if self.pairs[idx] is None:
                    # Если до этого не видели Томбов, то тупо вставляем
                    if first_tomb_idx is None:
                        self.pairs[idx] = (key, value)
                    # Ну а если встречали уже Томб, то заменяем на нашу пару самый первый Камень
                    else:
                        self.pairs[first_tomb_idx] = (key, value)
                        self.tomb_count -= 1
                    self.size += 1
                    break

                # Обновление значения по ключу
                elif self.pairs[idx] is not MyMap.__TOMBSTONE and self.pairs[idx][0] == key:
                    self.pairs[idx] = (key, value)
                    break

                # Наткнулись на Томб - идём дальше
                else:
                    continue

            # Если все ячейки в Томбах и нет свободного места, то вставляем по первому Томбу
            else:
                self.pairs[first_tomb_idx] = (key, value)
                self.tomb_count -= 1
                self.size += 1

        # В любом случае под конец проверяем заполненность
        if self.size + self.tomb_count >= self.capacity * MyMap.__LOAD_FACTOR:
            self.__resize()

    def get(self, key: str) -> int | None:
        idx: int = self.__calc_key_hash(key) % self.capacity - 1
        for i in range(self.capacity):
            idx = (idx + 1) % self.capacity
            # По индексу ничего не лежит - такого ключа нет в мапе
            if self.pairs[idx] is None:
                return None

            # По индексу лежит пара по данному ключу - нашли
            elif self.pairs[idx] is not MyMap.__TOMBSTONE and self.pairs[idx][0] == key:
                return self.pairs[idx][1]

            # По индексу лежит Томб или пара с другим ключом - двигаемся по ячейкам
            else:
                continue

        # Если все ячейки в Томбах или в парах с другими ключами, то такого искомого нет в мапе
        return None


    def delete(self, key: str) -> int | None:
        idx: int = self.__calc_key_hash(key) % self.capacity - 1
        for i in range(self.capacity):
            idx = (idx + 1) % self.capacity
            # По индексу ничего не лежит - такого ключа нет в мапе
            if self.pairs[idx] is None:
                return None

            # По индексу лежит пара по данному ключу - удаляем (заменяем на Томб)
            elif self.pairs[idx] is not MyMap.__TOMBSTONE and self.pairs[idx][0] == key:
                deleted_pair: tuple[str, int] = self.pairs[idx]
                self.pairs[idx] = MyMap.__TOMBSTONE
                self.size -= 1
                self.tomb_count += 1
                return deleted_pair[1]

            # По индексу лежит Томб или пара с другим ключом - двигаемся по ячейкам
            else:
                continue

        # Если все ячейки в Томбах или в парах с другими ключами, то такого искомого нет в мапе
        return None

    def __len__(self) -> int:
        return self.size

    def __resize(self):
        old_pairs: list[tuple[str, int] | None | object] = self.pairs
        if self.size >= self.capacity * MyMap.__LOAD_FACTOR / 2:
            self.capacity *= MyMap.__RESIZE_FACTOR
        self.size = 0
        self.tomb_count = 0
        self.pairs = [None] * self.capacity

        for pair in old_pairs:
            if pair is not None and pair is not MyMap.__TOMBSTONE:
                self.put(pair[0], pair[1])

    @staticmethod
    def __calc_key_hash(key: str) -> int:
        calculated_hash: int = 5381
        for char in key:
            calculated_hash = ((calculated_hash << 5) + calculated_hash) + ord(char)

            calculated_hash &= 0xFFFFFFFF
        return calculated_hash

def map_task() -> None:
    input_data: list[str] = sys.stdin.read().split("\n")
    Q: int = int(input_data[0])
    my_map: MyMap = MyMap()
    result: list[str] = []

    for i in range(1, Q + 1):
        command: str = input_data[i]
        split_command: list[str] = command.split()

        if command[0] == "p":
            my_map.put(split_command[1], int(split_command[2]))
        elif command[0] == "g":
            r = my_map.get(split_command[1])
            if r is None:
                result.append("Error")
            else:
                result.append(str(r))
        elif command[0] == "d":
            r = my_map.delete(split_command[1])
            if r is None:
                result.append("Error")
            else:
                result.append(str(r))
        elif command[0] == "s":
            result.append(str(len(my_map)))

    sys.stdout.write("\n".join(result) + "\n")

if __name__ == "__main__":
    map_task()
