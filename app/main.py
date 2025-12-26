from fastapi import FastAPI
from app.api.flow_routes import router as flow_router
from app.api.flow_read_routes import router as flow_read_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://d36wquhowtcyl5.cloudfront.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{path:path}")
async def options_handler(path: str):
    return {}

app.include_router(flow_router)
app.include_router(flow_read_router)
