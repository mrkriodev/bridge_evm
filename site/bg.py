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
    ID: int
    Status: str
    Address: str
    From: str
    To: str
    Signs: int
    Amount: int
    InternalStatus: int
    Direction: int

def StatusListToJSONList(StatusList):
    res = []

    for Status in StatusList:
        res.append(jsonable_encoder(Status))
    
    return res


# Sample data for the API
status_data = [
    Status(ID = 1, Status = "Pending", Address = "0xeD37bF8F4fe63AFEC337054B1df6bf28F6826661", From = "0x7dac71dbe9cd15fd71f791e3849a641ac6472fb5a54a4272a7b8bca227b55b1b", To = "0x7dac71dbe9cd15fd71f791e3849a641ac6472fb5a54a4272a7b8bca227b55b1b", Signs = 2, Amount = 1, InternalStatus = 200, Direction = 1),
    Status(ID = 2, Status = "Success", Address = "0xeD37bF8F4fe63AFEC337054B1df6bf28F6826661", From = "0x7dac71dbe9cd15fd71f791e3849a641ac6472fb5a54a4272a7b8bca227b55b1b", To = "0x7dac71dbe9cd15fd71f791e3849a641ac6472fb5a54a4272a7b8bca227b55b1b", Signs = 1, Amount = 2, InternalStatus = 200, Direction = 0),
    Status(ID = 3, Status = "Pending", Address = "0xeD37bF8F4fe63AFEC337054B1df6bf28F6826661", From = "0x7dac71dbe9cd15fd71f791e3849a641ac6472fb5a54a4272a7b8bca227b55b1b", To = "0x7dac71dbe9cd15fd71f791e3849a641ac6472fb5a54a4272a7b8bca227b55b1b", Signs = 3, Amount = 3, InternalStatus = 200, Direction = 1)
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

# API endpoint for /api/numSigns/{id}
@app.get('/api/status/{id}')
async def get_status_id(id: int):

    if id < 0 or id >= len(status_data):
        return JSONResponse(content = jsonable_encoder(Status(ID = 0, Status = "", Address = "", From = "", To = "", Signs = 0, Amount = 0, InternalStatus = 404)), headers = {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Expose-Headers" : "*",
            "Access-Control-Allow-Credentials" : "true"
        })

    return JSONResponse(content = jsonable_encoder(status_data[id]), headers = {
        "Access-Control-Allow-Origin" : "*",
        "Access-Control-Expose-Headers" : "*",
        "Access-Control-Allow-Credentials" : "true"
    })

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port = 8000)