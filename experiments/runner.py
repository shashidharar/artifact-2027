"""
============================================================
ARIA Research Prototype
Benchmark Runner
============================================================
"""

import time

from experiments.scenarios import SCENARIOS
from device_agent import DeviceAgent
from authentication import (
    AgentRegistrationAuthority,
    CloudAuthenticator,
    ZKPermissionProof,
)
from cloud import CloudOrchestrator
from models import AuthenticationRequest


class BenchmarkRunner:

    def __init__(self):

        self.device_agent = DeviceAgent()

        self.ara = AgentRegistrationAuthority()

        self.authenticator = CloudAuthenticator(self.ara)

        self.cloud = CloudOrchestrator()

    ##########################################################
    # Execute benchmark
    ##########################################################

    def run(self):

        results = []

        for scenario in SCENARIOS:

            print("=" * 70)
            print(
                f"Running Scenario {scenario['id']} : {scenario['name']}"
            )

            state = scenario["state"]

            ####################################################
            # Device Agent
            ####################################################

            t0 = time.perf_counter()

            remediation = self.device_agent.run_cycle(state)

            t1 = time.perf_counter()

            diagnosis_latency = (t1 - t0) * 1000

            ####################################################
            # No diagnosis
            ####################################################

            if remediation is None:

                results.append(
                    {
                        "Scenario": scenario["name"],
                        "Diagnosis(ms)": round(
                            diagnosis_latency, 3
                        ),
                        "Authentication(ms)": 0,
                        "Cloud(ms)": 0,
                        "Success": False,
                        "Health Before": state.health_score,
                        "Health After": state.health_score,
                        "Recommendation": "NONE",
                        "Confidence": 0.0,
                    }
                )

                continue

            ####################################################
            # Register Agent
            ####################################################

            abt = self.ara.register_agent(
                agent_id="Agent-001",
                role="DeviceAgent",
                endpoint="device://android001",
                permissions=[
                    "restart_service",
                    "clear_cache",
                    "cleanup_storage",
                    "restart_application",
                    "reset_network",
                    "cloud_assisted",
                ],
                capabilities=[
                    "resource",
                    "application",
                    "network",
                    "security",
                ],
            )

                        ####################################################
            # Authentication
            ####################################################

            category = remediation.diagnosis.category.value.lower()

            proof = ZKPermissionProof.generate(
                remediation.action.value
            )

            request = AuthenticationRequest(

                abt=abt,

                endpoint="device://android001",

                nonce="ARIA_NONCE",

                zk_proof=proof,

                requested_action=category,

                timestamp=time.time(),

                signature="prototype"

            )

            print("\n========== RUNNER DEBUG ==========")
            print("Scenario          :", scenario["name"])
            print("Requested Action  :", request.requested_action)
            print("Endpoint          :", request.endpoint)
            print("Permissions       :", abt.permissions)
            print("Capabilities      :", abt.capabilities)
            print("==================================")

            t2 = time.perf_counter()

            auth = self.authenticator.authenticate(
                request
            )

            t3 = time.perf_counter()

            authentication_latency = (

                t3 - t2

            ) * 1000

            print(auth)
            print("Authenticated =", auth.authenticated)

            ####################################################
            # Cloud
            ####################################################

            t4 = time.perf_counter()

            cloud_response = self.cloud.process(
                auth,
                remediation.diagnosis,
            )

            t5 = time.perf_counter()

            cloud_latency = (t5 - t4) * 1000

            ####################################################
            # Debug
            ####################################################

            print("=" * 60)
            print(scenario["name"])
            print("Remediation Success :", remediation.success)
            print("Decision            :", remediation.decision)
            print("Action              :", remediation.action)
            print(
                "Cloud Recommendation:",
                cloud_response.recommendation,
            )
            print("=" * 60)

            ####################################################
            # Store Results
            ####################################################

            results.append(
                {
                    "Scenario": scenario["name"],
                    "Diagnosis(ms)": round(
                        diagnosis_latency, 3
                    ),
                    "Authentication(ms)": round(
                        authentication_latency, 3
                    ),
                    "Cloud(ms)": round(
                        cloud_latency, 3
                    ),
                    "Success": remediation.success,
                    "Health Before": remediation.previous_health,
                    "Health After": remediation.current_health,
                    "Recommendation": cloud_response.recommendation.value,
                    "Confidence": round(
                        cloud_response.confidence,
                        3,
                    ),
                }
            )

        return results