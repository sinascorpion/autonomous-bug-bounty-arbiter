# Autonomous Bug Bounty Arbiter

A Trustless On-Chain Bug Bounty Pool & Multi-Validator Vulnerability Arbitration Protocol deployed on GenLayer Studio Next.

## Overview
Decentralized protocols face severe risks with off-chain vulnerability triage: centralized triagers extract heavy fees, disclose sensitive vulnerabilities before resolution, or stall indefinitely. **AutonomousBugBountyArbiter** transforms vulnerability disclosure into a trustless on-chain primitive using GenLayer Intelligent Contracts. Independent LLMs evaluate proofs of concept (PoCs) directly against locked scope specifications to autonomously award bounty tranches.

## Verified On-Chain Deployment
- **Network**: GenLayer Studio Next (Chain ID: `61997`)
- **Contract Address**: [`0x81a5D23ad16F24683f7fe3b0E6ed165Ee1B5Ca7c`](https://explorer-studio-dev.genlayer.com/address/0x81a5D23ad16F24683f7fe3b0E6ed165Ee1B5Ca7c)
- **Explorer URL**: https://explorer-studio-dev.genlayer.com/address/0x81a5D23ad16F24683f7fe3b0E6ed165Ee1B5Ca7c

## Key Architecture & Features
1. **Multi-Validator Severity Triage**: Employs GenLayer's non-deterministic VM (`gl.vm.run_nondet_unsafe`) where independent LLMs evaluate disclosures against declared scope rules to determine severity (CRITICAL, HIGH, MEDIUM, LOW, INVALID).
2. **Fail-Closed Equivalence Checks**: Validates that independent validators reach consensus on the exact severity class and have substantive analytical rationale before funds can be released.
3. **Dynamic Tiered Payouts**: 
   - CRITICAL: Awards 100% of available bounty pool.
   - HIGH: Awards 50% tier allocation.
   - INVALID / OUT OF SCOPE: Rejects report and preserves the locked bounty pool.
4. **Pull-Payment Pattern**: Awarded funds are routed to `claimable_balances` for safe, reentrancy-free withdrawal by whitehat security researchers.

## Live On-Chain Activity
- **Bounty Pool Creation**: Tx `0x3bce6f9ed587e2715b278d78197de043704bd516de99697eeeafdaf8a75bf39e` (0.1 GEN deposited)
- **Vulnerability Report Submission**: Tx `0x81258a01fdda585742da2865b4f02492e4af494dd07aa1b101f1d6f14e77dcec`
- **Autonomous AI Adjudication**: Tx `0x78377d6b1f92bd376a95e5e837b2b6d74638031e2ce57ac120665924ee815927` (Adjudicated CRITICAL with 88% validator consensus, 0.1 GEN awarded on-chain).

## License
MIT
