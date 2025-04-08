from fastapi import FastAPI
from App.api.routes import router as api_router
inport Sockets.stockClient
import Sockets.stockServer

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def root():
    blahblahablah