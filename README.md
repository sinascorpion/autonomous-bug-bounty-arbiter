# Autonomous Bug Bounty Arbiter

An experimental GenLayer Intelligent Contract for sponsor-authorized, single-report bounty pools, AI-assisted triage, and claimable GEN rewards. The deployed source is [contract.py](contract.py).

## Deployment

Studio-dev (chain ID 61997): [contract 0x0017f904c9106E4098d4Dc990f65e9e046C6DDCc](https://explorer-studio-dev.genlayer.com/address/0x0017f904c9106E4098d4Dc990f65e9e046C6DDCc). The [deployment transaction](https://explorer-studio-dev.genlayer.com/tx/0xf221bb99959be5e45f489c7ca626ac70cc046999ee39cf110480c33cbaaaca63) was accepted with successful execution. Studio-dev is a test network and may reset.

## Replay protection and use

Each bounty pool is restricted to one report for its entire lifetime, even after rejection or adjudication. The sponsor creates and funds a pool, calls `authorize_reporter` with the researcher's address, and the authorized researcher submits one report. Before creating a report ID, the contract checks that the pool has no registered report and permanently records the new ID against that pool. Before allocating any award, adjudication checks that the report is the pool's registered report, that its status is pending, and that it has not already received an award. Rewritten titles or proofs cannot obtain a second report or award from the same pool.

This is an intentionally restrictive per-pool limit, not a semantic similarity classifier: a second, different vulnerability also needs a separate pool. A sponsor may replace the authorized researcher only before the first submission. The sponsor controls access and can censor researchers. The protection is per pool, not across different pools.

The sponsor can call `close_bounty_pool` to request the return of unallocated funds before submission or after adjudication. Closure is blocked while a report is pending. If adjudication repeatedly fails or never reaches a decision, funds may remain locked indefinitely. Awarded balances remain claimable by the researcher via `withdraw_bounty`.

The leader and validators independently fetch and assess the first 4,000 characters of the target source, and validation requires identical fetched text and matching severity. CRITICAL, HIGH, MEDIUM and LOW allocate respectively 100%, 50%, 20% and 5% of the remaining pool; INVALID allocates nothing.

## Limitations

This is an unaudited experiment. The LLM does not execute the proof of concept or guarantee exploitability. Its confidence is model output, not a measured percentage of validator agreement. The source URL can change, scope is sponsor-defined, and only the first 4,000 characters are assessed. Reports and proofs are public. Native transfer delivery and the complete lifecycle of this revision have not been independently tested on the network. Do not rely on it to safeguard funds.

## Tests

Run `python -m unittest test_replay -v` for mock tests covering sponsor authorization, rejected and adjudicated reports, rewritten duplicates, separate pools, and sponsor refund accounting. Mock tests do not prove GenVM consensus, transfers or end-to-end network behavior. Never commit private keys.
