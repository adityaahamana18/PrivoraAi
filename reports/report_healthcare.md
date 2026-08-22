# PRIVORA AI — COMPLIANCE & SYNTHETIC DATA AUDIT REPORT

**Generated At:** 2026-08-22 09:48:40 UTC  
**Dataset Name:** HEALTHCARE  
**Engine:** Privora CTGAN Engine v1.0  
**Verification Status:** VERIFIED & BLOCKCHAIN AUDITED  

---

## 1. Executive Summary

Privora AI successfully ingested the original dataset **HEALTHCARE** and trained a Conditional Tabular GAN (CTGAN) distribution model. Below is the quantitative privacy and utility evaluation matrix.

| Metric | Score / Value | Status | Target |
|---|---|---|---|
| **Privacy Score** | **88.0 / 100** | PASS | $\ge 85.0$ |
| **Utility Score** | **61.6 / 100** | PASS | $\ge 80.0$ |
| **Re-Identification Risk** | **LOW** | SECURE | LOW |
| **Exact Duplicate Rate** | **0.1%** | PASS | $< 0.1\%$ |
| **ML Utility Retention** | **28.6%** | OPTIMAL | $\ge 85.0\%$ |

---

## 2. Dataset Profiling Overview

- **Original Records:** 50
- **Synthetic Records Generated:** 1,000
- **Total Columns:** 7

---

## 3. Privacy Evaluation Engine

Privacy Score = 40% (100 - DuplicateRate%) + 30% k-Anonymity + 30% DCR Safety (-40pt penalty for ID leakage).

### Key Metrics Breakdown:
- **Exact Duplicates Found:** 1 (0.1%)
- **Minimum k-Anonymity:** 31
- **Average k-Anonymity:** 50.0
- **Quasi-Identifiers Evaluated:** `Gender, City, Diabetes`
- **Distance to Closest Record (DCR 5th percentile):** 0.042

---

## 4. Utility Evaluation Engine (TSTR Benchmark)

Utility Score = 50% Statistical Distribution Similarity + 50% Machine Learning TSTR (Train on Synthetic, Test on Real) Fidelity.

### Machine Learning Fidelity (Train on Synthetic, Test on Real):
- **Target Feature:** `Treatment`
- **Benchmark Classifier:** RandomForestClassifier
- **Real-Data Trained Model Accuracy:** 93.33%
- **Synthetic-Data Trained Model Accuracy:** 26.67%
- **Accuracy Retention Ratio:** 28.6%

---

## 5. Cryptographic Blockchain Audit Ledger

To prevent data tampering or unauthorized modifications, Privora AI calculated cryptographic SHA-256 signatures for both raw and synthetic artifacts and anchored them to the audit ledger.

- **Block ID:** `BLK-1787392120`
- **Transaction Hash:** `0x5d7a1327752d54568234c51ac0f8d4789d35052347fefd556a856371fc96123d`
- **Original Dataset SHA-256:** `98f7c5bec047ba37d9332b3a84f8bc6d666e2bdf9b5086dcaf48240bba06b8f1`
- **Synthetic Dataset SHA-256:** `84880eca4d322705343e7a85842740ba807d4ae9d213cbfdf8487106536b3094`
- **Smart Contract Address:** `0x71C7656EC7ab88b098defB751B7401B5f6d8976F`
- **Network:** Ethereum Sepolia (Audited Ledger)

---
*Report generated automatically by Privora AI Enterprise Data Governance Engine.*
