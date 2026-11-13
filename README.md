# Autonomous Bug Bounty Arbiter

A Trustless On-Chain Bug Bounty Pool & Multi-Validator Vulnerability Arbitration Protocol deployed on GenLayer Studio (Chain ID `61999` / `61997`).

## Overview
Decentralized protocols face severe risks with off-chain vulnerability triage: centralized triagers extract heavy fees, disclose sensitive vulnerabilities before resolution, or stall indefinitely. **AutonomousBugBountyArbiter** transforms vulnerability disclosure into a trustless on-chain primitive using GenLayer Intelligent Contracts. Independent LLMs autonomously acquire the affected target source code directly from the repository on-chain via `gl.nondet.web.render()` and evaluate proofs of concept (PoCs) directly against the real code to award bounties or reject invalid submissions.

## Verified On-Chain Deployment
- **Network**: GenLayer Studio Network (Chain ID: `61999` / `61997`)
- **Contract Address**: [`0xBCEfB2b5408D874c6095b3f048427A6b9f32D6FD`](https://studio.genlayer.com/explorer/address/0xBCEfB2b5408D874c6095b3f048427A6b9f32D6FD)
- **Studio Explorer URL**: https://studio.genlayer.com/explorer/address/0xBCEfB2b5408D874c6095b3f048427A6b9f32D6FD
- **Legacy Explorer Endpoint**: https://explorer-studio-dev.genlayer.com/address/0xBCEfB2b5408D874c6095b3f048427A6b9f32D6FD

## Key Architecture & Features
1. **Target Source Code Acquisition (`gl.nondet.web.render`)**: Validators independently acquire the actual target repository code on-chain before performing triage, ensuring disclosures are grounded in authentic evidence.
2. **Multi-Validator Severity Triage**: Employs GenLayer's non-deterministic VM (`gl.vm.run_nondet_unsafe`) where independent LLMs evaluate disclosures directly against the acquired code to determine severity (CRITICAL, HIGH, MEDIUM, LOW, INVALID).
3. **Fail-Closed Equivalence Checks**: Validates that independent validators reach consensus on the exact severity class and have substantive analytical rationale before funds can be released.
4. **Dynamic Tiered Payouts**: 
   - CRITICAL: Awards 100% of available bounty pool.
   - HIGH: Awards 50% tier allocation.
   - MEDIUM: Awards 20% tier allocation.
   - LOW: Awards 5% tier allocation.
   - INVALID / OUT OF SCOPE: Rejects report and preserves the locked bounty pool.
5. **Contract-Native Value Transfer via `emit_transfer`**: When calling `withdraw_bounty()`, settled claimable balances trigger `_Beneficiary(beneficiary).emit_transfer(value=balance)` to directly disburse native GEN to the researcher's wallet, ensuring non-reentrancy and total fund conservation.

## Live On-Chain Activity
- **Contract Address**: `0xBCEfB2b5408D874c6095b3f048427A6b9f32D6FD`
- **Deployment Transaction**: `0x1e554a84ac2794556e514cb9b1dd2f6211812ee4d9fad79e7e515afb3cbab3c8`
- **Bounty Pool Creation**: `0x8900e6c3b922501e69c5e0e79a1de8f0aa88384f661e7f6007bfd53a579a15a2` (0.01 GEN locked)
- **Vulnerability Report 1 Submission**: `0x89903d163e5cedb368af9161ef3120dd91024f2d5288aa4da84a7478d3e6a3e1`
- **Autonomous AI Adjudication 1 (Grounded Dismissal)**: `0xfa42c6649bb3ee0ac74b521583fe0f85e49fd2db7b4595a8546575b08da2a534` (Dismissed non-reproducible report with 82% validator consensus).
- **Vulnerability Report 2 Submission**: `0x695989deef014a2d57cb800c096e4f654130a7a9c983292e347728a9a26d633a`
- **Autonomous AI Adjudication 2 (Grounded Confirmation & Bounty Allocation)**: `0x6eb4895e639d3eb8d8efce42fc4c584716d3136f666ecb0b5817e7b5e9e90743` (Confirmed LOW severity against acquired code, awarded 500,000,000,000,000 wei).
- **Native Bounty Withdrawal**: `0x0b8da79372d4ebdbea5a6f7d08f76e5afb930218da9c5469fa54ed0270d6e815` (Direct payout via `_Beneficiary.emit_transfer`).

## License
MIT
