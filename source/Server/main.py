from typing import Union, Optional
import logging

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from ai.inference import Inference

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()
model = Inference(model_path="source/Server/ai/Models/spam-detector", device=1)


class InferenceRequest(BaseModel):
    message: str


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.post("/inference")
async def read_inference(
    request: InferenceRequest,
) -> dict[str, Optional[Union[str, int]]]:
    try:
        logger.info(f"Received message for inference: {request.message}")
        result = model.predict_with_confidence(request.message)
        logger.info(f"Inference result: {result}")
        return {"result": result["prediction"]}
    except Exception as e:
        logger.error(f"Error occurred during inference: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
