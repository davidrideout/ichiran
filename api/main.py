import json
from datetime import datetime

import orjson
from fastapi import FastAPI, HTTPException
from utils import run_cmd

app = FastAPI()


@app.get("/ping")
def ping():
    return {"time": datetime.now()}


@app.get("/lookup")
def lookup(query: str):
    success, output = run_cmd(["ichiran-cli", "-f", query])
    output = output.decode("utf-8")
    output = "\n".join(line for line in output.splitlines() if not line.startswith("WARNING"))

    if not success:
        raise HTTPException(status_code=400, detail="Error during lookup")

    return orjson.loads(output)
