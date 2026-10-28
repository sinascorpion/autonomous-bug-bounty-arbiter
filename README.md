# Autonomous Bug Bounty Arbiter

A Trustless On-Chain Bug Bounty Pool & Multi-Validator Vulnerability Arbitration Protocol deployed on GenLayer Studio Next (Chain ID `61997`).

## Overview
Decentralized protocols face severe risks with off-chain vulnerability triage: centralized triagers extract heavy fees, disclose sensitive vulnerabilities before resolution, or stall indefinitely. **AutonomousBugBountyArbiter** transforms vulnerability disclosure into a trustless on-chain primitive using GenLayer Intelligent Contracts. Independent LLMs autonomously acquire the affected target source code directly from the repository on-chain via `gl.nondet.web.render()` and evaluate proofs of concept (PoCs) directly against the real code to award bounties or reject invalid submissions.

## Verified On-Chain Deployment
- **Network**: GenLayer Studio Next (Chain ID: `61997`)
- **Contract Address**: [`0x1F8d3f8594b2D0937DAe90985CA1638e905f21E4`](https://explorer-studio-dev.genlayer.com/address/0x1F8d3f8594b2D0937DAe90985CA1638e905f21E4)
- **Explorer URL**: https://explorer-studio-dev.genlayer.com/address/0x1F8d3f8594b2D0937DAe90985CA1638e905f21E4

## Key Architecture & Features
1. **Target Source Code Acquisition (`gl.nondet.web.render`)**: Validators independently acquire the actual target repository code on-chain before performing triage, ensuring disclosures are grounded in authentic evidence.
2. **Multi-Validator Severity Triage**: Employs GenLayer's non-deterministic VM (`gl.vm.run_nondet_unsafe`) where independent LLMs evaluate disclosures directly against the acquired code to determine severity (CRITICAL, HIGH, MEDIUM, LOW, INVALID).
3. **Fail-Closed Equivalence Checks**: Validates that independent validators reach consensus on the exact severity class and have substantive analytical rationale before funds can be released.
4. **Dynamic Tiered Payouts**: 
   - CRITICAL: Awards 100% of available bounty pool.
   - HIGH: Awards 50% tier allocation.
   - INVALID / OUT OF SCOPE: Rejects report and preserves the locked bounty pool.
5. **Contract-Native Value Transfer via `emit_transfer`**: When calling `withdraw_bounty()`, settled claimable balances trigger `_Beneficiary(beneficiary).emit_transfer(value=balance)` to directly disburse native GEN to the researcher's wallet, ensuring non-reentrancy and total fund conservation.

## Live On-Chain Activity (Studio Next 61997)
- **Contract Address**: `0x1F8d3f8594b2D0937DAe90985CA1638e905f21E4`
- **Deployment Transaction**: `0x105e89df8480ec238b2990a7461f2af6d229e37da0faf53d32cde19193a2556f`
- **Bounty Pool Creation**: `0x59fe5d1068f3145bbaabe27c2aad0b409c9f374c94fc5c979187a4803af8fb6e` (0.1 GEN locked)
- **Vulnerability Report Submission**: `0xd5da0906f03158841f96391f4f7706e261f0046f1cff836b6ffa6abfa895f0ba`
- **Autonomous AI Adjudication (Target Source Code Grounded On-Chain)**: `0x85825919b4c77e3b652ae0d433e16c52f4ab2bd0a21560232f396d203b12d773` (Adjudicated with 92% validator consensus and verified code snippet logged on-chain).

## License
MIT
