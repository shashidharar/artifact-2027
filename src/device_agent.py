"""
ARIA Research Prototype
device_agent.py
"""

from typing import Optional
from models import (
    DeviceState, FaultEvent, FaultCategory, FaultSeverity,
    RemediationAction, AuthorizationDecision, RemediationResult
)
from utils import TimeUtils


class DiagnosticEngine:
    @staticmethod
    def diagnose(state: DeviceState) -> Optional[FaultEvent]:
        if state.memory_utilization >= 85:
            return FaultEvent(FaultCategory.RESOURCE,"MEMORY_HIGH",FaultSeverity.HIGH,
                              "High memory utilization",0.85,TimeUtils.now())
        if state.storage_utilization >= 90:
            return FaultEvent(FaultCategory.RESOURCE,"STORAGE_HIGH",FaultSeverity.HIGH,
                              "Storage almost full",0.90,TimeUtils.now())
        if not state.application_running:
            return FaultEvent(FaultCategory.APPLICATION,"APPLICATION_CRASH",FaultSeverity.HIGH,
                              "Application crash detected",0.88,TimeUtils.now())
        if state.network_latency >= 250:
            return FaultEvent(FaultCategory.NETWORK,"NETWORK_LATENCY",FaultSeverity.MEDIUM,
                              "High network latency",0.65,TimeUtils.now())
        if state.security_alert:
            return FaultEvent(FaultCategory.SECURITY,"SECURITY_ALERT",FaultSeverity.CRITICAL,
                              "Security threat detected",0.99,TimeUtils.now())
        return None


class ActionSelector:
    MAP = {
        "MEMORY_HIGH": RemediationAction.CLEAR_CACHE,
        "STORAGE_HIGH": RemediationAction.CLEANUP_STORAGE,
        "APPLICATION_CRASH": RemediationAction.RESTART_APPLICATION,
        "NETWORK_LATENCY": RemediationAction.RESET_NETWORK,
        "SECURITY_ALERT": RemediationAction.CLOUD_ASSISTED,
    }

    @staticmethod
    def select(fault):
        if fault is None:
            return RemediationAction.NONE
        return ActionSelector.MAP.get(fault.fault_code, RemediationAction.NONE)


class LocalPolicyEngine:
    @staticmethod
    def evaluate(action):
        if action in (
            RemediationAction.CLEAR_CACHE,
            RemediationAction.CLEANUP_STORAGE,
            RemediationAction.RESTART_APPLICATION,
            RemediationAction.RESET_NETWORK,
        ):
            return AuthorizationDecision.ALLOW
        if action == RemediationAction.CLOUD_ASSISTED:
            return AuthorizationDecision.ESCALATE
        if action == RemediationAction.APPLY_PATCH:
            return AuthorizationDecision.HUMAN_APPROVAL
        return AuthorizationDecision.REJECT


class LocalExecutor:
    @staticmethod
    def execute(state, action):
        old = state.health_score
        success = True
        if action == RemediationAction.CLEAR_CACHE:
            state.memory_utilization = max(0, state.memory_utilization - 20)
            state.health_score = min(1.0, state.health_score + 0.05)
        elif action == RemediationAction.CLEANUP_STORAGE:
            state.storage_utilization = max(0, state.storage_utilization - 20)
            state.health_score = min(1.0, state.health_score + 0.05)
        elif action == RemediationAction.RESTART_APPLICATION:
            state.application_running = True
            state.health_score = min(1.0, state.health_score + 0.08)
        elif action == RemediationAction.RESET_NETWORK:
            state.network_latency = max(10, state.network_latency - 100)
            state.health_score = min(1.0, state.health_score + 0.04)
        return success, old, state.health_score


class DeviceAgent:
    def run_cycle(self, state: DeviceState):
        fault = DiagnosticEngine.diagnose(state)
        if fault is None:
            return None
        action = ActionSelector.select(fault)
        decision = LocalPolicyEngine.evaluate(action)
        if decision != AuthorizationDecision.ALLOW:
            return RemediationResult(
                diagnosis=fault,
                action=action,
                decision=decision,
                previous_health=state.health_score,
                current_health=state.health_score,
                success=False,
                latency_ms=0.0
            )
        success, prev, curr = LocalExecutor.execute(state, action)
        return RemediationResult(
            diagnosis=fault,
            action=action,
            decision=decision,
            previous_health=prev,
            current_health=curr,
            success=success,
            latency_ms=1.0
        )