import unittest
import sys
import os

# Add parent path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models import InboundInquiry, GateStatus
from app.orchestrator import SovereignOrchestrator

class TestSovereignOrchestrator(unittest.TestCase):

    def test_deterministic_workflow_lock(self):
        """Verify that an inbound inquiry is ALWAYS locked pending human approval."""
        orchestrator = SovereignOrchestrator()
        inquiry = InboundInquiry(
            inquiry_id="test-101",
            source="whatsapp",
            sender_name="Enterprise Procurement Lead",
            sender_contact="+971501234567",
            raw_message="We need a Quote & Lock contract for 10,000 MT Urea delivery."
        )
        
        execution = orchestrator.process_inbound(inquiry)
        
        # Assertions
        self.assertIsNotNone(execution.execution_id)
        self.assertEqual(execution.gate_status, GateStatus.PENDING_APPROVAL)
        self.assertFalse(execution.is_dispatched)
        self.assertEqual(len(execution.evaluations), 2)
        self.assertIsNotNone(execution.audit_hash)

    def test_human_approval_gate(self):
        """Verify that only explicit operator approval can dispatch the response."""
        orchestrator = SovereignOrchestrator()
        inquiry = InboundInquiry(
            inquiry_id="test-102",
            source="web",
            sender_name="Dubai Tech Partner",
            sender_contact="partner@dubai.ae",
            raw_message="Requesting Sovereign AI integration for local healthcare compliance."
        )
        
        execution = orchestrator.process_inbound(inquiry)
        self.assertFalse(execution.is_dispatched)
        
        # Simulate Operator Approval
        updated = orchestrator.submit_operator_decision(
            execution.execution_id, 
            approved=True, 
            reason="Verified corporate credentials"
        )
        
        self.assertEqual(updated.gate_status, GateStatus.APPROVED)
        self.assertTrue(updated.is_dispatched)
        self.assertIn("APPROVED", updated.operator_decision)

    def test_human_rejection_gate(self):
        """Verify that human rejection permanently halts external dispatch."""
        orchestrator = SovereignOrchestrator()
        inquiry = InboundInquiry(
            inquiry_id="test-103",
            source="email",
            sender_name="Unknown Caller",
            sender_contact="spam@unknown.com",
            raw_message="Unverified spam solicitations."
        )
        
        execution = orchestrator.process_inbound(inquiry)
        updated = orchestrator.submit_operator_decision(
            execution.execution_id, 
            approved=False, 
            reason="Unverified counterparty"
        )
        
        self.assertEqual(updated.gate_status, GateStatus.REJECTED)
        self.assertFalse(updated.is_dispatched)
        self.assertIn("REJECTED", updated.operator_decision)

if __name__ == "__main__":
    unittest.main()
