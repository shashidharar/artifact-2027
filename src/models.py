
"""
============================================================
ARIA Research Prototype
Common Data Models
============================================================
"""

from enum import Enum


# ============================================================
# Fault Categories
# ============================================================

class FaultCategory(Enum):

    RESOURCE = "Resource"

    APPLICATION = "Application"

    NETWORK = "Network"

    SECURITY = "Security"

    SYSTEM = "System"


# ============================================================
# Fault Severity
# ============================================================

class FaultSeverity(Enum):

    LOW = 1

    MEDIUM = 2

    HIGH = 3

    CRITICAL = 4


# ============================================================
# Remediation Actions
# ============================================================

class RemediationAction(Enum):

    NONE = "none"

    CLEAR_CACHE = "clear_cache"

    RESTART_APPLICATION = "restart_application"

    RESTART_SERVICE = "restart_service"

    CLEANUP_STORAGE = "cleanup_storage"

    RESET_NETWORK = "reset_network"

    APPLY_PATCH = "apply_patch"

    CLOUD_ASSISTED = "cloud_assisted"

    HUMAN_APPROVAL = "human_approval"


# ============================================================
# Authorization Decision
# ============================================================

class AuthorizationDecision(Enum):

    ALLOW = "ALLOW"

    ESCALATE = "ESCALATE"

    HUMAN_APPROVAL = "HUMAN_APPROVAL"

    REJECT = "REJECT"



from dataclasses import dataclass
from typing import Optional


# ============================================================
# Device Runtime State
# ============================================================

@dataclass
class DeviceState:

    cpu_utilization: float

    memory_utilization: float

    storage_utilization: float

    network_latency: float

    battery_level: float

    application_running: bool

    security_alert: bool

    health_score: float


# ============================================================
# Fault Event
# ============================================================

@dataclass
class FaultEvent:

    category: FaultCategory

    fault_code: str

    severity: FaultSeverity

    description: str

    risk_score: float

    timestamp: float


# ============================================================
# Remediation Result
# ============================================================

@dataclass
class RemediationResult:

    diagnosis: FaultEvent

    action: RemediationAction

    decision: AuthorizationDecision

    previous_health: float

    current_health: float

    success: bool

    latency_ms: float



from dataclasses import dataclass
from typing import List


# ============================================================
# Agent-Bound Token (ABT)
# ============================================================

@dataclass
class AgentBoundToken:

    token_id: str

    agent_id: str

    role: str

    endpoint: str

    permissions: List[str]

    capabilities: List[str]

    issued_at: float

    expires_at: float

    attestation_hash: str

    issuer: str

    credential_status: str

    version: int

    revocation_id: str

    signature: str = ""


# ============================================================
# Authentication Request
# ============================================================

@dataclass
class AuthenticationRequest:

    abt: AgentBoundToken

    endpoint: str

    nonce: str

    zk_proof: str

    requested_action: str

    timestamp: float

    signature: str


# ============================================================
# Authentication Result
# ============================================================

@dataclass
class AuthenticationResult:

    authenticated: bool

    decision: AuthorizationDecision

    message: str

    agent_id: str

