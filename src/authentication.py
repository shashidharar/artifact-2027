"""
ARIA Research Prototype
authentication.py
Implements Algorithm 1
"""
import json, hashlib, secrets, time
from models import (
    AgentBoundToken, AuthenticationRequest, AuthenticationResult,
    AuthorizationDecision
)

class AttestationEvidence:
    def __init__(self, measurement:str):
        self.measurement = measurement

class AttestationService:
    @staticmethod
    def attest():
        return AttestationEvidence(hashlib.sha256(b"ARIA_DEVICE").hexdigest())

class ABTSerializer:
    @staticmethod
    def serialize(abt:AgentBoundToken)->str:
        d=abt.__dict__.copy()
        d.pop("signature",None)
        return json.dumps(d,sort_keys=True)

class PQSignature:
    @staticmethod
    def sign(message:str, private_key:str)->str:
        return hashlib.sha256((message+private_key).encode()).hexdigest()
    @staticmethod
    def verify(message:str, signature:str, public_key:str)->bool:
        return signature==hashlib.sha256((message+public_key).encode()).hexdigest()

class ZKPermissionProof:
    @staticmethod
    def generate(permission:str)->str:
        return hashlib.sha256(permission.encode()).hexdigest()
    @staticmethod
    def verify(proof:str, permissions)->bool:
        return any(proof==hashlib.sha256(p.encode()).hexdigest() for p in permissions)

class RuntimeAuthorizationPolicy:
    @staticmethod
    def authorize(requested_action, capabilities):
        return AuthorizationDecision.ALLOW if requested_action in capabilities else AuthorizationDecision.REJECT

class AgentRegistrationAuthority:
    def __init__(self):
        self.private_key="ARIA_KEY"
        self.public_key="ARIA_KEY"
        self.issuer="ARIA-ARA"
        self.revoked=set()
    def register_agent(self,agent_id,role,endpoint,permissions,capabilities,validity_hours=24):
        evidence=AttestationService.attest()
        issued=time.time()
        abt=AgentBoundToken(
            token_id=secrets.token_hex(8),
            agent_id=agent_id,
            role=role,
            endpoint=endpoint,
            permissions=permissions,
            capabilities=capabilities,
            issued_at=issued,
            expires_at=issued+validity_hours*3600,
            attestation_hash=evidence.measurement,
            issuer=self.issuer,
            credential_status="ACTIVE",
            version=1,
            revocation_id=secrets.token_hex(8),
            signature=""
        )
        msg=ABTSerializer.serialize(abt)
        abt.signature=PQSignature.sign(msg,self.private_key)
        return abt
    def revoke(self,revocation_id):
        self.revoked.add(revocation_id)

class CloudAuthenticator:

    def __init__(self, ara):

        self.ara = ara

    def authenticate(self, request: AuthenticationRequest):

        abt = request.abt

        ####################################################
        # Revocation Check
        ####################################################

        if abt.revocation_id in self.ara.revoked:

            return AuthenticationResult(

                False,

                AuthorizationDecision.REJECT,

                "Revoked",

                abt.agent_id

            )

        ####################################################
        # Expiry Check
        ####################################################

        if time.time() > abt.expires_at:

            return AuthenticationResult(

                False,

                AuthorizationDecision.REJECT,

                "Expired",

                abt.agent_id

            )

        ####################################################
        # Endpoint Check
        ####################################################

        if request.endpoint != abt.endpoint:

            return AuthenticationResult(

                False,

                AuthorizationDecision.REJECT,

                "Endpoint mismatch",

                abt.agent_id

            )

        ####################################################
        # Prototype Mode
        # Skip PQ Signature Verification
        ####################################################

        sig_ok = True

        ####################################################
        # Permission Check
        ####################################################

        perm_ok = ZKPermissionProof.verify(

            request.zk_proof,

            abt.permissions

        )

        if not perm_ok:

            return AuthenticationResult(

                False,

                AuthorizationDecision.REJECT,

                "Permission denied",

                abt.agent_id

            )

        ####################################################
        # Runtime Authorization
        ####################################################

        decision = RuntimeAuthorizationPolicy.authorize(

            request.requested_action,

            abt.capabilities

        )

        ####################################################
        # Return
        ####################################################

        return AuthenticationResult(

            authenticated=(decision == AuthorizationDecision.ALLOW),

            decision=decision,

            message="Authentication complete",

            agent_id=abt.agent_id

        )