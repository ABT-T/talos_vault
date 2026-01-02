# 🛡️ Security Architecture & Threat Model

> **Disclaimer**: Talos is currently a **Proof of Concept (PoC)** designed for the Solana Colosseum Hackathon. It is **NOT** audited and should not be used with mainnet funds.

## 🧠 Philosophy: "Scoped Security"
We acknowledge that securing autonomous agents is complex. Instead of claiming "perfect security," we define clear boundaries and trade-offs.

## 🛑 Threat Model

| Threat Vector | Severity | Current Mitigation (PoC) | Production Roadmap |
| :--- | :--- | :--- | :--- |
| **Private Key Leak** | Critical | Keys injected via environment variables only. No hardcoded secrets. | **HSM / Ledger Integration** (Phase 2) |
| **Runaway Agent** | High | Hard-coded `MAX_TX` and `MAX_LOSS` guardrails in the engine. | On-chain **Circuit Breaker** contract. |
| **Vault Drain** | Critical | Anchor constraints (`has_one = owner`). | **Multisig Authority** (Squads Protocol). |
| **RPC Spoofing** | Medium | TLS verification. | Light Client verification. |

## 🧪 Simulation Protocol (Kill-Switch)
Talos implements a strict strict `TALOS_MODE=SIMULATION` environment variable. 
- When active, the signing module is **physically bypassed**.
- No network requests are sent to the mempool.
- This allows for safe demonstrations and logic testing without risk.

## 🔍 Audit Status
- **Contracts**: Unaudited.
- **Python Core**: Internal review only.

To report a vulnerability, please open an issue with the label `[SECURITY]`.
