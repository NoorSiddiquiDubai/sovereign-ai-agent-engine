from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AgentRole(str, Enum):
    LEAD_QUALIFIER = "lead_qualifier"
    COMPLIANCE_OFFICER = "compliance_officer"
    QUOTE_DRAFTER = "quote_drafter"

class GateStatus(str, Enum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"

class InboundInquiry(BaseModel):
    inquiry_id: str = Field(..., description="Unique inquiry tracking UUID")
    source: str = Field(default="whatsapp", description="Intake source (whatsapp/web/email)")
    sender_name: str
    sender_contact: str
    raw_message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentEvaluation(BaseModel):
    agent_role: AgentRole
    reasoning: str
    confidence_score: float
    output_payload: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class WorkflowExecution(BaseModel):
    execution_id: str
    inquiry: InboundInquiry
    evaluations: List[AgentEvaluation] = Field(default_factory=list)
    proposed_response: str
    gate_status: GateStatus = GateStatus.PENDING_APPROVAL
    operator_decision: Optional[str] = None
    operator_timestamp: Optional[datetime] = None
    is_dispatched: bool = False
    audit_hash: Optional[str] = None
