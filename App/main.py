from fastapi import FastAPI
from App.api.routes import router as api_router
import Sockets.stockClient
import Sockets.stockServer

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def root():
    print("derp")