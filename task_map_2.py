import sys


def window_task() -> None:
    input_data: list[str] = sys.stdin.read().split()
    N, K = int(input_data[0]), int(input_data[1])
    ids = input_data[2:]

    ids_counts = dict()
    result = []

    # Загрузка первого окна
    for j in range(K):
        if ids[j] in ids_counts:
            ids_counts[ids[j]] = ids_counts[ids[j]] + 1
        else:
            ids_counts[ids[j]] = 1

    # Итерация по следующим окнам
    for i in range(N - K + 1):
        result.append(str(len(ids_counts)))
        cur_count = ids_counts[ids[i]] - 1
        ids_counts[ids[i]] = cur_count
        if cur_count == 0:
            del ids_counts[ids[i]]

        if i != N - K:
            if ids[i + K] in ids_counts:
                ids_counts[ids[i + K]] = ids_counts[ids[i + K]] + 1
            else:
                ids_counts[ids[i + K]] = 1

    sys.stdout.write(" ".join(result) + "\n")

if __name__ == "__main__":
    window_task()
