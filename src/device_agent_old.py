
"""
============================================================
ARIA Research Prototype
Device Agent
============================================================
"""

from models import *



from utils import TimeUtils


# ============================================================
# Diagnostic Engine
# ============================================================

class DiagnosticEngine:
    """
    Identifies the dominant fault affecting the device based
    on runtime telemetry.
    """

    @staticmethod
    def diagnose(state):

        # ----------------------------------------------------
        # Resource Faults
        # ----------------------------------------------------

        if state.memory_utilization >= 85:

            return FaultEvent(

                category=FaultCategory.RESOURCE,

                severity=FaultSeverity.HIGH,

                description="High memory utilization",

                risk_score=0.85,

                timestamp=TimeUtils.now()

            )

        if state.storage_utilization >= 90:

            return FaultEvent(

                category=FaultCategory.RESOURCE,

                severity=FaultSeverity.HIGH,

                description="Storage almost full",

                risk_score=0.90,

                timestamp=TimeUtils.now()

            )

        # ----------------------------------------------------
        # Application Faults
        # ----------------------------------------------------

        if not state.application_running:

            return FaultEvent(

                category=FaultCategory.APPLICATION,

                severity=FaultSeverity.HIGH,

                description="Application crash detected",

                risk_score=0.88,

                timestamp=TimeUtils.now()

            )

        # ----------------------------------------------------
        # Network Faults
        # ----------------------------------------------------

        if state.network_latency >= 250:

            return FaultEvent(

                category=FaultCategory.NETWORK,

                severity=FaultSeverity.MEDIUM,

                description="High network latency",

                risk_score=0.65,

                timestamp=TimeUtils.now()

            )

        # ----------------------------------------------------
        # Security Faults
        # ----------------------------------------------------

        if state.security_alert:

            return FaultEvent(

                category=FaultCategory.SECURITY,

                severity=FaultSeverity.CRITICAL,

                description="Security alert detected",

                risk_score=0.99,

                timestamp=TimeUtils.now()

            )

        # ----------------------------------------------------
        # Healthy Device
        # ----------------------------------------------------

        return None



# ============================================================
# Action Selector
# ============================================================

class ActionSelector:
    """
    Selects an initial remediation action based on the
    diagnosed fault.
    """

    @staticmethod
    def select(fault):

        if fault is None:

            return RemediationAction.NONE

        # ----------------------------------------------------
        # Resource Faults
        # ----------------------------------------------------

        if fault.category == FaultCategory.RESOURCE:

            if "memory" in fault.description.lower():

                return RemediationAction.CLEAR_CACHE

            if "storage" in fault.description.lower():

                return RemediationAction.CLEANUP_STORAGE

            return RemediationAction.CLEAR_CACHE

        # ----------------------------------------------------
        # Application Faults
        # ----------------------------------------------------

        if fault.category == FaultCategory.APPLICATION:

            return RemediationAction.RESTART_APPLICATION

        # ----------------------------------------------------
        # Network Faults
        # ----------------------------------------------------

        if fault.category == FaultCategory.NETWORK:

            return RemediationAction.RESET_NETWORK

        # ----------------------------------------------------
        # Security Faults
        # ----------------------------------------------------

        if fault.category == FaultCategory.SECURITY:

            return RemediationAction.CLOUD_ASSISTED

        # ----------------------------------------------------
        # System Faults
        # ----------------------------------------------------

        if fault.category == FaultCategory.SYSTEM:

            return RemediationAction.RESTART_SERVICE

        return RemediationAction.NONE



from utils import TimeUtils


# ============================================================
# Diagnostic Engine
# ============================================================

class DiagnosticEngine:
    """
    Identifies the dominant fault affecting the device based
    on runtime telemetry.
    """

    @staticmethod
    def diagnose(state):

        # ----------------------------------------------------
        # Resource Faults
        # ----------------------------------------------------

        if state.memory_utilization >= 85:

            return FaultEvent(

    category=FaultCategory.RESOURCE,

    fault_code="MEMORY_HIGH",

    severity=FaultSeverity.HIGH,

    description="High memory utilization",

    risk_score=0.85,

    timestamp=TimeUtils.now()

)

        if state.storage_utilization >= 90:

            return FaultEvent(

                category=FaultCategory.RESOURCE,

                severity=FaultSeverity.HIGH,

                description="Storage almost full",

                risk_score=0.90,

                timestamp=TimeUtils.now()

            )

        # ----------------------------------------------------
        # Application Faults
        # ----------------------------------------------------

        if not state.application_running:

            return FaultEvent(

    category=FaultCategory.RESOURCE,

    fault_code="STORAGE_HIGH",

    severity=FaultSeverity.HIGH,

    description="Storage almost full",

    risk_score=0.90,

    timestamp=TimeUtils.now()

)

        # ----------------------------------------------------
        # Network Faults
        # ----------------------------------------------------

        if state.network_latency >= 250:

            return FaultEvent(

    category=FaultCategory.NETWORK,

    fault_code="NETWORK_LATENCY",

    severity=FaultSeverity.MEDIUM,

    description="High network latency",

    risk_score=0.65,

    timestamp=TimeUtils.now()

)

        # ----------------------------------------------------
        # Security Faults
        # ----------------------------------------------------

        if state.security_alert:

            return FaultEvent(

    category=FaultCategory.SECURITY,

    fault_code="SECURITY_ALERT",

    severity=FaultSeverity.CRITICAL,

    description="Security alert detected",

    risk_score=0.99,

    timestamp=TimeUtils.now()

)

        # ----------------------------------------------------
        # Healthy Device
        # ----------------------------------------------------

        return None

