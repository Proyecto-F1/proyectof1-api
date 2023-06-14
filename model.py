import os
from utils import data_path
from typing import Optional
from pydantic import BaseModel, validator

class F1DataArgs(BaseModel):
    data_type: str
    max_rows: Optional[int]

    @validator('data_type')
    def data_type_must_be_valid(cls, v):
        data_values = []
        for file in os.listdir(data_path):
            if file.endswith(".csv"):
                data_values.append(file.split(".")[0])

        if v not in data_values:
            raise ValueError(f"Data type must be one of {data_values}")

        return v

    @validator('max_rows')
    def max_rows_must_be_positive(cls, v):
        if v < 1:
            raise ValueError("Max rows must be positive")

        return v
