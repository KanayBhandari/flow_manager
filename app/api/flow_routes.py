from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.flow_schema import FlowRequest
from app.db.repositories import create_or_update_flow_definition
from app.flows.engine import run_flow

router = APIRouter(prefix="/flow")


@router.post("/run")
def run_flow_endpoint(req: FlowRequest, db: Session = Depends(get_db)):
    """
    1. Save (or update) flow definition in DB
    2. Trigger sequential flow execution
    """
    flow_data = req.flow

    # Save or update in DB via repository
    flow_def_model = create_or_update_flow_definition(
        db=db,
        flow_id=flow_data.id,
        name=flow_data.name,
        definition=req.flow.model_dump()
    )

    # Run the flow sequentially
    result = run_flow(flow_def_model, db)

    return result
