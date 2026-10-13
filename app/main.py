from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.models import InboundInquiry, WorkflowExecution
from app.orchestrator import SovereignOrchestrator

app = FastAPI(
    title="Sovereign AI Agent Engine",
    description="Enterprise Multi-Agent Workflow Engine with Human-in-the-Loop Release Gates",
    version="1.0.0"
)

orchestrator = SovereignOrchestrator()

class DecisionRequest(BaseModel):
    approved: bool
    reason: str = ""

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "doctrine": "No evidence, no done",
        "sovereign_mode": "ACTIVE",
        "data_residency": "ON_SOIL"
    }

@app.post("/inbound/process", response_model=WorkflowExecution)
def process_inquiry(inquiry: InboundInquiry):
    return orchestrator.process_inbound(inquiry)

@app.get("/workflows/{execution_id}", response_model=WorkflowExecution)
def get_workflow(execution_id: str):
    if execution_id not in orchestrator.executions:
        raise HTTPException(status_code=404, detail="Execution not found")
    return orchestrator.executions[execution_id]

@app.post("/workflows/{execution_id}/decision", response_model=WorkflowExecution)
def submit_decision(execution_id: str, decision: DecisionRequest):
    try:
        return orchestrator.submit_operator_decision(execution_id, decision.approved, decision.reason)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
