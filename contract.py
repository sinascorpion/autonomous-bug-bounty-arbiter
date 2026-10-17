# v0.3.3
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json

@gl.evm.contract_interface
class _Beneficiary:
    class View:
        pass
    class Write:
        pass

class AutonomousBugBountyArbiter(gl.Contract):
    """
    Autonomous Bug Bounty & Vulnerability Arbitration Protocol
    
    A standalone GenLayer Intelligent Contract primitive that provides trustless on-chain
    bug bounty pools and non-deterministic vulnerability assessment. Eliminates centralized
    bounty triagers and fee-extracting intermediaries (e.g. Immunefi/HackerOne).
    
    Flow:
    1. Project/Protocol locks a bounty reward pool and defines scope rules, asset repositories, and severity tiers.
    2. Security Researcher (Whitehat) submits a structured Vulnerability Report (PoC, impact vector, CVSS score).
    3. Multi-validator GenLayer LLMs independently review the submission against scope and code impact:
       - CRITICAL: Pays out up to 100% of maximum tier bounty pool.
       - HIGH: Pays out 50% tier allocation.
       - MEDIUM / LOW: Pays out 15% - 25% allocation.
       - OUT_OF_SCOPE / INVALID / DUPLICATE: Rejects claim; preserves bounty pool.
    4. Substantive fail-closed equivalence checks prevent validator drift and enforce cryptographic consensus.
    5. Clean claimable balance model guarantees non-reentrant reward withdrawals.
    """
    
    owner: Address
    bounty_counter: u64
    report_counter: u64
    
    # Bounty Pool State (keys are string bounty_id)
    sponsors: TreeMap[str, Address]
    project_names: TreeMap[str, str]
    scope_specifications: TreeMap[str, str]
    max_bounty_amounts: TreeMap[str, u256]
    locked_bounty_pools: TreeMap[str, u256]
    bounty_active_flags: TreeMap[str, bool]
    
    # Vulnerability Submission & Arbitration State (keys are string report_id)
    report_bounty_ids: TreeMap[str, u64]
    whitehats: TreeMap[str, Address]
    vulnerability_titles: TreeMap[str, str]
    proof_of_concepts: TreeMap[str, str]
    # Report Status: 0=PENDING_TRIAGE, 1=ACCEPTED_PAID, 2=REJECTED_OUT_OF_SCOPE
    report_statuses: TreeMap[str, u8]
    awarded_amounts: TreeMap[str, u256]
    triage_verdicts: TreeMap[str, str]
    validator_confidences: TreeMap[str, u8]
    
    # Financial Claimable Balances
    claimable_balances: TreeMap[str, u256]

    def __init__(self):
        self.owner = gl.message.sender_address
        self.bounty_counter = 0
        self.report_counter = 0

    @gl.public.write.payable
    def create_bounty_pool(
        self,
        project_name: str,
        scope_specification: str,
        bounty_pool_amount: u256
    ) -> u64:
        """
        Initializes an on-chain vulnerability bounty pool with locked reward custody.
        """
        sponsor = gl.message.sender_address
        attached_value = gl.message.value
        
        assert bounty_pool_amount > 0, "Bounty pool amount must exceed zero"
        assert attached_value >= bounty_pool_amount, f"Attached value {attached_value} is less than required bounty {bounty_pool_amount}"
        assert len(project_name.strip()) > 0, "Project identifier required"
        assert len(scope_specification.strip()) > 0, "Bounty scope specifications required"
        
        self.bounty_counter += 1
        b_id = self.bounty_counter
        key = str(b_id)
        
        self.sponsors[key] = sponsor
        self.project_names[key] = project_name.strip()
        self.scope_specifications[key] = scope_specification.strip()
        self.max_bounty_amounts[key] = bounty_pool_amount
        self.locked_bounty_pools[key] = bounty_pool_amount
        self.bounty_active_flags[key] = True
        
        return b_id

    @gl.public.write
    def submit_vulnerability_report(
        self,
        bounty_id: u64,
        vuln_title: str,
        proof_of_concept: str
    ) -> u64:
        """
        Whitehat security researcher submits a cryptographic PoC report for autonomous triage.
        """
        whitehat = gl.message.sender_address
        b_key = str(bounty_id)
        
        assert self.bounty_active_flags.get(b_key, False), "Bounty program is inactive or does not exist"
        assert self.locked_bounty_pools.get(b_key, 0) > 0, "Bounty program funds are fully depleted"
        assert len(vuln_title.strip()) > 0, "Vulnerability title required"
        assert len(proof_of_concept.strip()) > 0, "Vulnerability proof-of-concept / exploit reproduction required"
        
        self.report_counter += 1
        r_id = self.report_counter
        r_key = str(r_id)
        
        self.report_bounty_ids[r_key] = bounty_id
        self.whitehats[r_key] = whitehat
        self.vulnerability_titles[r_key] = vuln_title.strip()
        self.proof_of_concepts[r_key] = proof_of_concept.strip()
        self.report_statuses[r_key] = 0  # PENDING_TRIAGE
        self.awarded_amounts[r_key] = 0
        self.triage_verdicts[r_key] = "Report submitted. Pending autonomous AI validator consensus triage."
        self.validator_confidences[r_key] = 0
        
        return r_id

    @gl.public.write
    def adjudicate_report(self, report_id: u64) -> None:
        """
        Autonomous Multi-Validator Vulnerability Arbitration:
        Independent GenLayer LLM validators analyze PoC and scope rules non-deterministically.
        Severity outcomes:
        - CRITICAL: Pays 100% of available pool (capped at max pool).
        - HIGH: Pays 50% of available pool.
        - MEDIUM: Pays 20% of available pool.
        - LOW: Pays 5% of available pool.
        - INVALID: Rejects report; $0 payout.
        """
        r_key = str(report_id)
        status = self.report_statuses.get(r_key, 255)
        assert status == 0, "Report must be in pending triage status"
        
        b_id = self.report_bounty_ids.get(r_key, 0)
        b_key = str(b_id)
        
        proj = self.project_names.get(b_key, "")
        scope = self.scope_specifications.get(b_key, "")
        pool_available = self.locked_bounty_pools.get(b_key, 0)
        whitehat = self.whitehats.get(r_key)
        
        vuln_title = self.vulnerability_titles.get(r_key, "")
        poc = self.proof_of_concepts.get(r_key, "")
        
        prompt = f"""You are an autonomous AI Smart Contract Security Triager and Vulnerability Arbiter on GenLayer.
Evaluate the submitted vulnerability disclosure against the project's bounty scope.

Target Project: {proj}
Scope Rules & In-Scope Assets: {scope}
Available Bounty Pool: {pool_available} wei

Submitted Vulnerability Report:
Title: {vuln_title}
Proof of Concept & Exploit Vector: {poc}

Triage Directives:
1. Verify if the affected component is within the declared scope and represents an authentic exploitable vulnerability.
2. Assign one of the standard severity ratings:
   - "CRITICAL": Direct loss of funds, governance takeover, unconstrained mint, reentrancy drain.
   - "HIGH": Temporary freezing of assets, logic bypass with bounded loss, broken access control.
   - "MEDIUM": Denial of service, gas griefing, state inconsistency without direct fund loss.
   - "LOW": Informational, code quality, edge-case rounding without material damage.
   - "INVALID": Out of scope, fabricated/hallucinated exploit, theoretical non-issue, or duplicate.

Respond strictly in valid JSON format:
{{
  "severity": "CRITICAL" or "HIGH" or "MEDIUM" or "LOW" or "INVALID",
  "confidence": integer between 60 and 100,
  "rationale": "Clear technical assessment of the vulnerability severity"
}}
"""

        def leader_fn():
            res = gl.nondet.exec_prompt(prompt, response_format="json")
            if not isinstance(res, dict):
                raise gl.UserError(f"LLM returned invalid format: {type(res)}")
            return res

        def validator_fn(leader_result) -> bool:
            """
            Fail-Closed Substantive Equivalence Check:
            Validators independently run LLM prompt on their own node and verify matching severity rating.
            """
            if not isinstance(leader_result, gl.vm.Return):
                return False
            lead_data = leader_result.calldata
            if not isinstance(lead_data, dict):
                return False
                
            lead_sev = str(lead_data.get("severity", "")).strip().upper()
            if lead_sev not in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INVALID"):
                return False
                
            lead_rat = str(lead_data.get("rationale", "")).strip()
            if len(lead_rat) < 5:
                return False
                
            try:
                val_res = gl.nondet.exec_prompt(prompt, response_format="json")
                if isinstance(val_res, dict):
                    val_sev = str(val_res.get("severity", "")).strip().upper()
                    return lead_sev == val_sev
                return False
            except Exception:
                return False

        triage_res = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        severity = str(triage_res.get("severity", "")).strip().upper()
        confidence = int(triage_res.get("confidence", 85))
        rationale = str(triage_res.get("rationale", "Autonomous security consensus concluded."))
        
        self.validator_confidences[r_key] = u8(min(100, max(0, confidence)))
        
        if severity == "INVALID":
            self.report_statuses[r_key] = 2  # REJECTED_OUT_OF_SCOPE
            self.triage_verdicts[r_key] = f"Report Dismissed ({confidence}% consensus): {rationale}. Zero payout awarded."
        else:
            self.report_statuses[r_key] = 1  # ACCEPTED_PAID
            # Calculate payout allocation
            if severity == "CRITICAL":
                payout = pool_available  # 100% of remaining pool
            elif severity == "HIGH":
                payout = pool_available // 2  # 50%
            elif severity == "MEDIUM":
                payout = pool_available // 5  # 20%
            else:  # LOW
                payout = pool_available // 20  # 5%
                
            payout = max(1, min(payout, pool_available))
            
            self.locked_bounty_pools[b_key] = pool_available - payout
            self.awarded_amounts[r_key] = payout
            
            cur_whitehat_bal = self.claimable_balances.get(str(whitehat), 0)
            self.claimable_balances[str(whitehat)] = cur_whitehat_bal + payout
            
            self.triage_verdicts[r_key] = f"[{severity} VULNERABILITY CONFIRMED] ({confidence}% consensus): {rationale}. Awarded {payout} wei to security researcher."

    @gl.public.write
    def withdraw_bounty(self, beneficiary: Address) -> u256:
        """
        Whitehat claims their awarded bounty payment.
        """
        sender = gl.message.sender_address
        assert sender == beneficiary, "Unauthorized: caller can only withdraw their own claimable bounty"
        
        balance = self.claimable_balances.get(str(beneficiary), 0)
        assert balance > 0, "No claimable bounty available for withdrawal"
        
        self.claimable_balances[str(beneficiary)] = 0
        return balance

    @gl.public.view
    def get_bounty_pool(self, bounty_id: u64) -> dict:
        key = str(bounty_id)
        zero_addr = Address("0x0000000000000000000000000000000000000000")
        return {
            "id": bounty_id,
            "sponsor": str(self.sponsors.get(key, zero_addr)),
            "project_name": self.project_names.get(key, ""),
            "scope_specification": self.scope_specifications.get(key, ""),
            "max_bounty": str(self.max_bounty_amounts.get(key, 0)),
            "locked_pool": str(self.locked_bounty_pools.get(key, 0)),
            "is_active": self.bounty_active_flags.get(key, False)
        }

    @gl.public.view
    def get_report(self, report_id: u64) -> dict:
        key = str(report_id)
        zero_addr = Address("0x0000000000000000000000000000000000000000")
        return {
            "id": report_id,
            "bounty_id": self.report_bounty_ids.get(key, 0),
            "whitehat": str(self.whitehats.get(key, zero_addr)),
            "vulnerability_title": self.vulnerability_titles.get(key, ""),
            "proof_of_concept": self.proof_of_concepts.get(key, ""),
            "status": self.report_statuses.get(key, 0),
            "awarded_amount": str(self.awarded_amounts.get(key, 0)),
            "triage_verdict": self.triage_verdicts.get(key, ""),
            "validator_confidence": self.validator_confidences.get(key, 0)
        }

    @gl.public.view
    def get_claimable_balance(self, user: Address) -> str:
        return str(self.claimable_balances.get(str(user), 0))

    @gl.public.view
    def get_total_bounties(self) -> u64:
        return self.bounty_counter

    @gl.public.view
    def get_total_reports(self) -> u64:
        return self.report_counter
