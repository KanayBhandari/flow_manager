from fastapi import FastAPI
from app.api.flow_routes import router as flow_router
from app.api.flow_read_routes import router as flow_read_router

app = FastAPI()

app.include_router(flow_router)
app.include_router(flow_read_router)
