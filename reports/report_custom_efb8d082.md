# PRIVORA AI — COMPLIANCE & SYNTHETIC DATA AUDIT REPORT

**Generated At:** 2026-08-19 06:27:00 UTC  
**Dataset Name:** CUSTOM_EFB8D082  
**Engine:** Privora CTGAN Engine v1.0  
**Verification Status:** VERIFIED & BLOCKCHAIN AUDITED  

---

## 1. Executive Summary

Privora AI successfully ingested the original dataset **CUSTOM_EFB8D082** and trained a Conditional Tabular GAN (CTGAN) distribution model. Below is the quantitative privacy and utility evaluation matrix.

| Metric | Score / Value | Status | Target |
|---|---|---|---|
| **Privacy Score** | **92.5 / 100** | PASS | $\ge 85.0$ |
| **Utility Score** | **91.7 / 100** | PASS | $\ge 80.0$ |
| **Re-Identification Risk** | **LOW** | SECURE | LOW |
| **Exact Duplicate Rate** | **0.0%** | PASS | $< 0.1\%$ |
| **ML Utility Retention** | **100.0%** | OPTIMAL | $\ge 85.0\%$ |

---

## 2. Dataset Profiling Overview

- **Original Records:** 20
- **Synthetic Records Generated:** 3,000
- **Total Columns:** 16

---

## 3. Privacy Evaluation Engine

Privacy Score = 40% (100 - DuplicateRate%) + 30% k-Anonymity + 30% DCR Safety (-40pt penalty for ID leakage).

### Key Metrics Breakdown:
- **Exact Duplicates Found:** 0 (0.0%)
- **Minimum k-Anonymity:** 4
- **Average k-Anonymity:** 111.11
- **Quasi-Identifiers Evaluated:** `Gender, Cancer_Type, Laterality`
- **Distance to Closest Record (DCR 5th percentile):** 0.497

---

## 4. Utility Evaluation Engine (TSTR Benchmark)

Utility Score = 50% Statistical Distribution Similarity + 50% Machine Learning TSTR (Train on Synthetic, Test on Real) Fidelity.

### Machine Learning Fidelity (Train on Synthetic, Test on Real):
- **Target Feature:** `Country`
- **Benchmark Classifier:** RandomForestClassifier
- **Real-Data Trained Model Accuracy:** 50.0%
- **Synthetic-Data Trained Model Accuracy:** 50.0%
- **Accuracy Retention Ratio:** 100.0%

---

## 5. Cryptographic Blockchain Audit Ledger

To prevent data tampering or unauthorized modifications, Privora AI calculated cryptographic SHA-256 signatures for both raw and synthetic artifacts and anchored them to the audit ledger.

- **Block ID:** `BLK-1787120820`
- **Transaction Hash:** `0xe3c6ca9b39590c29cfd64ea9f28d281e024c3bdc4af55bda6d6dc7922a61d61e`
- **Original Dataset SHA-256:** `57da88fe78ab389575b54ee5823459e72b035941796cc1c2024e94e07f6cebcf`
- **Synthetic Dataset SHA-256:** `27ec1247fe5e3d27776338927c03ab89930aa6d0042db97be0ab3974a4fabb63`
- **Smart Contract Address:** `0x71C7656EC7ab88b098defB751B7401B5f6d8976F`
- **Network:** Ethereum Sepolia (Audited Ledger)

---
*Report generated automatically by Privora AI Enterprise Data Governance Engine.*
