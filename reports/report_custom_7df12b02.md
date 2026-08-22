# PRIVORA AI — COMPLIANCE & SYNTHETIC DATA AUDIT REPORT

**Generated At:** 2026-08-22 09:36:58 UTC  
**Dataset Name:** CUSTOM_7DF12B02  
**Engine:** Privora CTGAN Engine v1.0  
**Verification Status:** VERIFIED & BLOCKCHAIN AUDITED  

---

## 1. Executive Summary

Privora AI successfully ingested the original dataset **CUSTOM_7DF12B02** and trained a Conditional Tabular GAN (CTGAN) distribution model. Below is the quantitative privacy and utility evaluation matrix.

| Metric | Score / Value | Status | Target |
|---|---|---|---|
| **Privacy Score** | **88.6 / 100** | PASS | $\ge 85.0$ |
| **Utility Score** | **86.2 / 100** | PASS | $\ge 80.0$ |
| **Re-Identification Risk** | **LOW** | SECURE | LOW |
| **Exact Duplicate Rate** | **0.0%** | PASS | $< 0.1\%$ |
| **ML Utility Retention** | **87.4%** | OPTIMAL | $\ge 85.0\%$ |

---

## 2. Dataset Profiling Overview

- **Original Records:** 5,000
- **Synthetic Records Generated:** 1,000
- **Total Columns:** 16

---

## 3. Privacy Evaluation Engine

Privacy Score = 40% (100 - DuplicateRate%) + 30% k-Anonymity + 30% DCR Safety (-40pt penalty for ID leakage).

### Key Metrics Breakdown:
- **Exact Duplicates Found:** 0 (0.0%)
- **Minimum k-Anonymity:** 28
- **Average k-Anonymity:** 37.04
- **Quasi-Identifiers Evaluated:** `Gender, Cancer_Type, Laterality`
- **Distance to Closest Record (DCR 5th percentile):** 0.237

---

## 4. Utility Evaluation Engine (TSTR Benchmark)

Utility Score = 50% Statistical Distribution Similarity + 50% Machine Learning TSTR (Train on Synthetic, Test on Real) Fidelity.

### Machine Learning Fidelity (Train on Synthetic, Test on Real):
- **Target Feature:** `Country`
- **Benchmark Classifier:** RandomForestClassifier
- **Real-Data Trained Model Accuracy:** 10.07%
- **Synthetic-Data Trained Model Accuracy:** 8.8%
- **Accuracy Retention Ratio:** 87.4%

---

## 5. Cryptographic Blockchain Audit Ledger

To prevent data tampering or unauthorized modifications, Privora AI calculated cryptographic SHA-256 signatures for both raw and synthetic artifacts and anchored them to the audit ledger.

- **Block ID:** `BLK-1787391418`
- **Transaction Hash:** `0x99a5a6b534189e20943264ea8dfac5529d751135fa76638cb5d5946e4fe248ea`
- **Original Dataset SHA-256:** `3306242a97f2f798ff516af626f4268ed1c5d909840246b9499ecabf4ef819b6`
- **Synthetic Dataset SHA-256:** `3b30c872446f26ddfe011e0320596e1094e5f066e584e477cdc84356372ba8f3`
- **Smart Contract Address:** `0x71C7656EC7ab88b098defB751B7401B5f6d8976F`
- **Network:** Ethereum Sepolia (Audited Ledger)

---
*Report generated automatically by Privora AI Enterprise Data Governance Engine.*
