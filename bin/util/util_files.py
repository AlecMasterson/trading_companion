import os
import pandas


def read_csv(file_path: str) -> pandas.DataFrame:
    full_path = f"data/{file_path}.csv"
    if not os.path.isfile(full_path):
        raise FileNotFoundError

    return pandas.read_csv(full_path)


def to_csv(path: str, name: str, data: pandas.DataFrame) -> None:
    full_path = f"data/{path}"
    os.makedirs(full_path, exist_ok=True)

    data.to_csv(f"{full_path}/{name}.csv", index=False)
