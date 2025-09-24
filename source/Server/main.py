from typing import Union, Optional

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai.inference import Inference

app = FastAPI()
model = Inference(model_path="source/Server/ai/Models/spam-detector", device=1)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/inference/{msg}")
async def read_inference(msg: str) -> dict[str, Optional[Union[str, int]]]:
    try:
        result = model.predict(msg)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
