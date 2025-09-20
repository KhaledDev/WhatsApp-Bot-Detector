from typing import Union, Optional

from fastapi import FastAPI
import uvicorn
from ai import inference

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/inference/{msg}")
def read_inference(
    msg: Optional[Union[str, None]] = None,
) -> dict[str, Optional[Union[str, None]]]:
    # TODO: Add inference code here
    return {"message": msg}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
