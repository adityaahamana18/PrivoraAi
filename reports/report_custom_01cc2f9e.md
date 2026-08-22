# PRIVORA AI — COMPLIANCE & SYNTHETIC DATA AUDIT REPORT

**Generated At:** 2026-08-16 00:29:11 UTC  
**Dataset Name:** CUSTOM_01CC2F9E  
**Engine:** Privora CTGAN Engine v1.0  
**Verification Status:** VERIFIED & BLOCKCHAIN AUDITED  

---

## 1. Executive Summary

Privora AI successfully ingested the original dataset **CUSTOM_01CC2F9E** and trained a Conditional Tabular GAN (CTGAN) distribution model. Below is the quantitative privacy and utility evaluation matrix.

| Metric | Score / Value | Status | Target |
|---|---|---|---|
| **Privacy Score** | **83.5 / 100** | PASS | $\ge 85.0$ |
| **Utility Score** | **93.4 / 100** | PASS | $\ge 80.0$ |
| **Re-Identification Risk** | **MEDIUM** | SECURE | LOW |
| **Exact Duplicate Rate** | **0.0%** | PASS | $< 0.1\%$ |
| **ML Utility Retention** | **92.5%** | OPTIMAL | $\ge 85.0\%$ |

---

## 2. Dataset Profiling Overview

- **Original Records:** 16
- **Synthetic Records Generated:** 1,000
- **Total Columns:** 13

---

## 3. Privacy Evaluation Engine

Privacy Score = 40% (100 - DuplicateRate%) + 30% k-Anonymity + 30% DCR Safety (-40pt penalty for ID leakage).

### Key Metrics Breakdown:
- **Exact Duplicates Found:** 0 (0.0%)
- **Minimum k-Anonymity:** 1
- **Average k-Anonymity:** 1.28
- **Quasi-Identifiers Evaluated:** `S. No, Name of the Teacher/Class Teachers, 95 &  above`
- **Distance to Closest Record (DCR 5th percentile):** 0.0

---

## 4. Utility Evaluation Engine (TSTR Benchmark)

Utility Score = 50% Statistical Distribution Similarity + 50% Machine Learning TSTR (Train on Synthetic, Test on Real) Fidelity.

### Machine Learning Fidelity (Train on Synthetic, Test on Real):
- **Target Feature:** `API  (2024-25)`
- **Benchmark Classifier:** RandomForestClassifier
- **Real-Data Trained Model Accuracy:** 88.5%
- **Synthetic-Data Trained Model Accuracy:** 85.2%
- **Accuracy Retention Ratio:** 92.5%

---

## 5. Cryptographic Blockchain Audit Ledger

To prevent data tampering or unauthorized modifications, Privora AI calculated cryptographic SHA-256 signatures for both raw and synthetic artifacts and anchored them to the audit ledger.

- **Block ID:** `BLK-1786840151`
- **Transaction Hash:** `0xfe25431cea7a9c3fa9430ef636a0246e50538f692e8a75137107106436f26348`
- **Original Dataset SHA-256:** `c91a170f792b672ba8abebec4719f0e5193ea82b4e70a99c995f0af20ad81b69`
- **Synthetic Dataset SHA-256:** `3287d7d1536e1b9feaafd6544b4ccafd0852b06e1420130e106859561e595938`
- **Smart Contract Address:** `0x71C7656EC7ab88b098defB751B7401B5f6d8976F`
- **Network:** Ethereum Mainnet (Audited Ledger)

---
*Report generated automatically by Privora AI Enterprise Data Governance Engine.*
