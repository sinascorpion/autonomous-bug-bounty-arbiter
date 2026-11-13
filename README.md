# Autonomous Bug Bounty Arbiter

An experimental GenLayer Intelligent Contract for funded bounty pools, AI-assisted vulnerability triage, and claimable GEN rewards. The source is [contract.py](contract.py).

## Deployment status

No current Studio-dev deployment of this revision has been verified. Earlier submitted addresses returned “contract not found” on Studio-dev. Do not use those addresses as evidence for this revision. Studio-dev (chain 61997) and Studionet (chain 61999) are separate networks; preview state can be reset. Before submitting evidence, verify the network, deployment transaction, successful execution, contract address, source and matching Explorer page.

## How it works

A sponsor supplies a source URL, scope and exactly the pool amount. A researcher submits a report. The leader and validators fetch and assess the first 4,000 characters of the target source; validation requires the same fetched text and severity. A successful decision allocates a portion of the remaining pool to a claimable balance, and the researcher can call `withdraw_bounty` to request a native GEN transfer.

Fetch failures and empty evidence abort adjudication. Adjudication also rejects a depleted pool. Excess deposits are rejected rather than retained.

## Limitations

This is an experiment, not an audited security system. The LLM evaluates a report; it does not execute the proof of concept or guarantee that a vulnerability is real. Its reported confidence is model output, not a measured percentage of validator agreement. Only the first 4,000 characters are examined, the URL can serve mutable content, and sponsor-defined scope is not independently authenticated. Reports and proofs of concept are public. Duplicate reports can receive multiple awards; there is no sponsor refund or pool closure mechanism. Do not fund with assets you cannot afford to lose.

The selected payout rates are 100% of the remaining pool for CRITICAL, 50% for HIGH, 20% for MEDIUM and 5% for LOW; INVALID gets no payout.

## Testing and deployment

The current source has received a Python syntax check only; its execution, transfers and complete lifecycle on the target network have not been verified for this revision. Deploy using tooling compatible with the target network, including the required fee distribution for Consensus v0.6. Confirm both consensus and execution results, and verify the exact address on its matching Explorer before submitting. Never commit private keys or credentials.
