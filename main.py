from fastapi import FastAPI
import pyarrow.parquet as pq

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}