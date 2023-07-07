from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Status(BaseModel):
    id: int
    status: str

def StatusListToJSONList(StatusList):
    res = []

    for Status in StatusList:
        res.append(jsonable_encoder(Status))
    
    return res


# Sample data for the API
status_data = [
    Status(id=1, status="Pending"),
    Status(id=2, status="Completed"),
    Status(id=3, status="Pending")
]

StatusListToJSONList(status_data)

# API endpoint for /api/status
@app.get('/api/status')
async def get_status():
    return JSONResponse(content = StatusListToJSONList(status_data), headers = {
        "Access-Control-Allow-Origin" : "*",
        "Access-Control-Expose-Headers" : "*",
        "Access-Control-Allow-Credentials" : "true"
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port = 8000)