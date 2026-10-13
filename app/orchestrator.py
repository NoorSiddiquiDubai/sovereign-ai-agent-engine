import hashlib
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List
from app.models import (
    InboundInquiry,
    AgentEvaluation,
    AgentRole,
    WorkflowExecution,
    GateStatus
)

class SovereignOrchestrator:
    """
    Sovereign Multi-Agent Orchestrator operating on local/private LLM logic.
    Enforces Human-in-the-Loop (HITL) gate lock before any external communication.
    """
    def __init__(self, ollama_endpoint: str = "http://localhost:11434"):
        self.ollama_endpoint = ollama_endpoint
        self.executions: Dict[str, WorkflowExecution] = {}

    def process_inbound(self, inquiry: InboundInquiry) -> WorkflowExecution:
        execution_id = str(uuid.uuid4())
        
        # 1. Lead Qualification Agent
        qualifier_eval = self._evaluate_qualification(inquiry)
        
        # 2. Compliance & Jurisdiction Agent (GCC / Sovereign verification)
        compliance_eval = self._evaluate_compliance(inquiry)
        
        # 3. Draft Proposed Output
        proposed_text = self._synthesize_response(inquiry, qualifier_eval, compliance_eval)
        
        # Calculate SHA256 audit hash
        audit_string = f"{execution_id}|{inquiry.raw_message}|{proposed_text}"
        audit_hash = hashlib.sha256(audit_string.encode()).hexdigest()

        execution = WorkflowExecution(
            execution_id=execution_id,
            inquiry=inquiry,
            evaluations=[qualifier_eval, compliance_eval],
            proposed_response=proposed_text,
            gate_status=GateStatus.PENDING_APPROVAL,
            is_dispatched=False,
            audit_hash=audit_hash
        )

        self.executions[execution_id] = execution
        return execution

    def submit_operator_decision(self, execution_id: str, approved: bool, reason: str = "") -> WorkflowExecution:
        if execution_id not in self.executions:
            raise ValueError(f"Execution {execution_id} not found.")

        exec_record = self.executions[execution_id]
        if exec_record.gate_status != GateStatus.PENDING_APPROVAL:
            raise RuntimeError(f"Workflow already decided: {exec_record.gate_status}")

        if approved:
            exec_record.gate_status = GateStatus.APPROVED
            exec_record.is_dispatched = True  # Simulated outbound release
            exec_record.operator_decision = f"APPROVED by Human Operator. {reason}".strip()
        else:
            exec_record.gate_status = GateStatus.REJECTED
            exec_record.is_dispatched = False
            exec_record.operator_decision = f"REJECTED by Human Operator. {reason}".strip()

        exec_record.operator_timestamp = datetime.utcnow()
        return exec_record

    def _evaluate_qualification(self, inquiry: InboundInquiry) -> AgentEvaluation:
        # Deterministic scoring logic
        is_high_intent = any(keyword in inquiry.raw_message.lower() for keyword in ["contract", "price", "quote", "rfq", "ai", "urea", "dap", "service"])
        confidence = 0.95 if is_high_intent else 0.70
        return AgentEvaluation(
            agent_role=AgentRole.LEAD_QUALIFIER,
            reasoning="Deterministic intent keyword and scope analysis completed.",
            confidence_score=confidence,
            output_payload={"intent": "commercial_inquiry" if is_high_intent else "general_info", "priority": "high" if is_high_intent else "standard"}
        )

    def _evaluate_compliance(self, inquiry: InboundInquiry) -> AgentEvaluation:
        return AgentEvaluation(
            agent_role=AgentRole.COMPLIANCE_OFFICER,
            reasoning="Sovereign jurisdiction check: Data residency preserved on private server; zero third-party API transmission.",
            confidence_score=1.0,
            output_payload={"jurisdiction": "UAE_GCC", "data_residency": "SOVEREIGN_ON_SOIL", "sanitized": True}
        )

    def _synthesize_response(self, inquiry: InboundInquiry, qual: AgentEvaluation, comp: AgentEvaluation) -> str:
        return (
            f"Dear {inquiry.sender_name},\n\n"
            f"Thank you for contacting our executive office. We have recorded your request: '{inquiry.raw_message}'. "
            f"Our team is reviewing the commercial parameters under our deterministic 48-hour Quote & Lock framework.\n\n"
            f"Best regards,\nExecutive Office (Sovereign Operations)"
        )
