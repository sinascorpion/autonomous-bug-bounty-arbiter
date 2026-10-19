# Autonomous Bug Bounty Arbiter

A Trustless On-Chain Bug Bounty Pool & Multi-Validator Vulnerability Arbitration Protocol deployed on GenLayer Studio Next.

## Overview
Decentralized protocols face severe risks with off-chain vulnerability triage: centralized triagers extract heavy fees, disclose sensitive vulnerabilities before resolution, or stall indefinitely. **AutonomousBugBountyArbiter** transforms vulnerability disclosure into a trustless on-chain primitive using GenLayer Intelligent Contracts. Independent LLMs autonomously acquire the affected target source code directly from the repository on-chain via `gl.nondet.web.render()` and evaluate proofs of concept (PoCs) directly against the real code to award bounties or reject invalid submissions.

## Verified On-Chain Deployment
- **Network**: GenLayer Studio Next (Chain ID: `61997`)
- **Contract Address**: [`0xED0587732C0885048749A4283dD079a3508b9B1A`](https://explorer-studio-dev.genlayer.com/address/0xED0587732C0885048749A4283dD079a3508b9B1A)
- **Explorer URL**: https://explorer-studio-dev.genlayer.com/address/0xED0587732C0885048749A4283dD079a3508b9B1A

## Key Architecture & Features
1. **Target Source Code Acquisition (`gl.nondet.web.render`)**: Validators independently acquire the actual target repository code on-chain before performing triage, ensuring disclosures are grounded in authentic evidence.
2. **Multi-Validator Severity Triage**: Employs GenLayer's non-deterministic VM (`gl.vm.run_nondet_unsafe`) where independent LLMs evaluate disclosures directly against the acquired code to determine severity (CRITICAL, HIGH, MEDIUM, LOW, INVALID).
3. **Fail-Closed Equivalence Checks**: Validates that independent validators reach consensus on the exact severity class and have substantive analytical rationale before funds can be released.
4. **Dynamic Tiered Payouts**: 
   - CRITICAL: Awards 100% of available bounty pool.
   - HIGH: Awards 50% tier allocation.
   - INVALID / OUT OF SCOPE: Rejects report and preserves the locked bounty pool.
5. **Pull-Payment Pattern**: Awarded funds are routed to `claimable_balances` for safe, reentrancy-free withdrawal by whitehat security researchers.

## Live On-Chain Activity (Studio Next)
- **Contract Address**: `0xED0587732C0885048749A4283dD079a3508b9B1A`
- **Bounty Pool Creation**: Tx `0x0c4e0bb08d523c50ea55ffd6bdf3ee59ec3f7c181e33a281a56dcc19c1eec9b6` (0.1 GEN locked)
- **Vulnerability Report Submission**: Tx `0xbf1df1206975e4d0370f64dd409a6bdcf58519ca0b5113a44a84e132948c1176`
- **Autonomous AI Adjudication (Target Source Code Grounded On-Chain)**: Tx `0xb83723a274fa605d292251eb040e0ddc5ff41fddccefb7ffe2e3462bfb1f2dba` (Adjudicated with 95% validator consensus and verified code snippet logged on-chain).

## License
MIT
