# ARIA: Autonomous Remediation and Intelligence Agent

This repository contains the publicly releasable prototype and controlled experiments for ARIA (Autonomous Remediation and Intelligence Agent), a multi-agent framework for autonomous mobile-device remediation with policy-aware zero-trust authorization.

The artifact accompanies the paper submitted to USENIX Security 2027.

## Repository Structure

ARIA/
├── README.md
├── LICENSE
├── src/
├── experiments/
└── scripts/

* `src/` — Prototype implementation of the ARIA authentication, authorization, and remediation workflow.
* `experiments/` — Experimental code for security evaluation, remediation benchmarking, and scalability evaluation.
* `scripts/` — Scripts for running the provided experiments.
* `LICENSE` — CC BY-NC 4.0 license.

## Artifact Scope

The artifact provides the controlled prototype and experiments used to evaluate the security and recovery properties reported in the paper.

The artifact includes:

* Agent-Bound Token (ABT)-based authentication.
* Zero-knowledge proof (ZKP)-based permission verification.
* Policy-based authorization.
* Remediation decision and execution workflow.
* Security experiments against representative attack classes.
* A 20-scenario remediation benchmark.
* Controlled scalability experiments with simulated Device Agents.

The artifact is intended to allow reviewers to inspect and reproduce the publicly releasable experimental workflow.

## Prototype Environment

The controlled prototype is implemented using Python and can be executed in a Google Colab environment.

The prototype uses test credentials and experimental parameters. It does not require production credentials or proprietary Samsung infrastructure.

## Authentication and Authorization

ARIA separates agent authentication from authorization. An ABT binds the agent identity and associated permissions/capabilities to a cryptographically verifiable credential. A requested privileged operation must additionally satisfy the required authorization relation and applicable policy before execution.

## Security Evaluation

The artifact contains experiments for five representative attack classes considered in the paper:

1. Agent impersonation
2. Replay attack
3. Privilege escalation
4. Policy bypass
5. Unauthorized remediation recommendation

The security evaluation comprises **4,750 attack attempts**.

For the evaluated attack cases, all unauthorized requests were rejected and no unauthorized remediation execution was observed.


## Remediation Benchmark

The artifact includes the controlled remediation benchmark used in the paper.

The benchmark contains 20 representative scenarios covering:

* system faults;
* security attacks;
* application and service failures; and
* network infrastructure events.

The benchmark measures recovery-path latency and remediation success.

These experiments use simulated Device Agents and therefore do not represent a physical deployment of 500 mobile devices.

## Running the Artifact

The primary experimental workflow is provided in the files under `experiments/` and `scripts/`.

For Google Colab execution:

1. Open the provided notebook or Python entry point, if included.
2. Install the required Python dependencies.
3. Run the prototype initialization.
4. Execute the authentication and authorization workflow.
5. Run the security experiments.
6. Run the 20-scenario remediation benchmark.
7. Run the scalability experiments.

The exact execution commands and dependencies are provided with the corresponding experiment files.

## Limitations

The artifact represents the publicly releasable prototype and controlled experiments.

The scalability evaluation uses simulated Device Agents and does not represent a 500-device physical deployment.

The security evaluation covers the attack classes defined in the paper's threat model and is not intended to establish security against every possible attack.

## Confidentiality

The repository contains only software and experimental material approved for public release.

It does not contain:

* production credentials;
* private cryptographic keys;
* internal certificates;
* proprietary source code;

## License

This artifact is released under the **Creative Commons Attribution-NonCommercial International (CC BY-NC)** license.

See the `LICENSE` file for the complete license terms.

Third-party software and dependencies remain subject to their respective licenses.
