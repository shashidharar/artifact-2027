"""
============================================================
ARIA Research Prototype
cloud.py
Implements Algorithm 3
============================================================
"""

from dataclasses import dataclass
from typing import List

from models import FaultCategory
from models import RemediationAction


# ============================================================
# Knowledge Record
# ============================================================

@dataclass
class KnowledgeRecord:

    category: FaultCategory

    fault_code: str

    recommendation: RemediationAction

    confidence: float

    explanation: str


# ============================================================
# Cloud Response
# ============================================================

@dataclass
class CloudResponse:

    recommendation: RemediationAction

    confidence: float

    explanation: str

    retrieved_records: int


# ============================================================
# Cloud Knowledge Base
# ============================================================

class CloudKnowledgeBase:

    def __init__(self):

        self.records = [

            KnowledgeRecord(
                FaultCategory.RESOURCE,
                "MEMORY_HIGH",
                RemediationAction.CLEAR_CACHE,
                0.98,
                "High memory utilization resolved by clearing cache."
            ),

            KnowledgeRecord(
                FaultCategory.RESOURCE,
                "STORAGE_HIGH",
                RemediationAction.CLEANUP_STORAGE,
                0.97,
                "Storage cleanup restores available space."
            ),

            KnowledgeRecord(
                FaultCategory.APPLICATION,
                "APPLICATION_CRASH",
                RemediationAction.RESTART_APPLICATION,
                0.99,
                "Restarting the application resolves transient failures."
            ),

            KnowledgeRecord(
                FaultCategory.NETWORK,
                "NETWORK_LATENCY",
                RemediationAction.RESET_NETWORK,
                0.94,
                "Resetting network interfaces reduces latency."
            ),

            KnowledgeRecord(
                FaultCategory.SECURITY,
                "SECURITY_ALERT",
                RemediationAction.CLOUD_ASSISTED,
                1.00,
                "Security incidents require cloud-assisted remediation."
            )

        ]

    def search(self, fault_code: str):

        return [

            r

            for r in self.records

            if r.fault_code == fault_code

        ]


# ============================================================
# Retrieval Engine
# ============================================================

class RetrievalEngine:

    def __init__(self, kb):

        self.kb = kb

    def retrieve(self, diagnosis):

        return self.kb.search(

            diagnosis.fault_code

        )


# ============================================================
# Recommendation Engine
# ============================================================

class RecommendationEngine:

    @staticmethod
    def recommend(records):

        if len(records) == 0:

            return CloudResponse(

                recommendation=RemediationAction.NONE,

                confidence=0.0,

                explanation="No recommendation available.",

                retrieved_records=0

            )

        best = max(

            records,

            key=lambda r: r.confidence

        )

        return CloudResponse(

            recommendation=best.recommendation,

            confidence=best.confidence,

            explanation=best.explanation,

            retrieved_records=len(records)

        )


# ============================================================
# Cloud Orchestrator
# ============================================================

class CloudOrchestrator:
    """
    Algorithm 3

    1. Receive authenticated diagnosis
    2. Retrieve historical knowledge
    3. Rank candidate remediations
    4. Return best recommendation
    """

    def __init__(self):

        self.kb = CloudKnowledgeBase()

        self.retrieval = RetrievalEngine(

            self.kb

        )

    def process(

        self,

        authentication_result,

        diagnosis

    ):

        ########################################################
        # Authentication failed
        ########################################################

        if not authentication_result.authenticated:

            print("Authentication rejected by Cloud.")

            return CloudResponse(

                recommendation=RemediationAction.NONE,

                confidence=0.0,

                explanation="Authentication failed.",

                retrieved_records=0

            )

        ########################################################
        # Retrieve similar knowledge
        ########################################################

        records = self.retrieval.retrieve(

            diagnosis

        )

        ########################################################
        # Recommend best remediation
        ########################################################

        return RecommendationEngine.recommend(

            records

        )