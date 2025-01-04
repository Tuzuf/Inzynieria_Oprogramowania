import pandas as pd

def read_data(file_path): # type: ignore
    data = pd.read_excel(file_path)
    return data