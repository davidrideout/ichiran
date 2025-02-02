from datetime import datetime
import json
from fastapi import FastAPI, HTTPException
from utils import run_cmd

CONTAINER_NAME = "ichiran-main-1"

app = FastAPI()


@app.get("/ping")
def ping():
    return {"time": datetime.now()}


@app.get("/lookup")
def lookup(query: str):
    success, output = run_cmd(["docker", "exec", "-it", "ichiran-cli", "-f", query])

    if not success:
        raise HTTPException(status_code=400, detail="Error during lookup")

    return json.loads(output)
