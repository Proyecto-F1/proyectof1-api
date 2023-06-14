import os
import uvicorn
import numpy as np
import pandas as pd
from model import F1DataArgs
from utils import data_path, port
from fastapi import FastAPI, APIRouter

app = FastAPI()

@app.get("/f1-data")
async def get_data(args: F1DataArgs):
    csv_path = os.path.join(data_path, f"{args.data_type}.csv")

    if not os.path.exists(csv_path):
        return {"error": "Data type not found"}
    
    df_data = pd.read_csv(csv_path)
    df_data = df_data.replace([np.inf, -np.inf], np.nan).dropna(axis=1)
    df_data = df_data.drop(columns=["Unnamed: 0"])
    df_data = df_data.reset_index(drop=True)

    df_dict = df_data.to_dict(orient="records")

    if args.max_rows:
        df_dict = df_dict[:args.max_rows]
    
    return df_dict

if __name__ == "__main__":
    uvicorn.run(app, port=port)
