# PRIVORA AI — COMPLIANCE & SYNTHETIC DATA AUDIT REPORT

**Generated At:** 2026-08-15 23:22:25 UTC  
**Dataset Name:** CUSTOM_AEEA9030  
**Engine:** Privora CTGAN Engine v1.0  
**Verification Status:** VERIFIED & BLOCKCHAIN AUDITED  

---

## 1. Executive Summary

Privora AI successfully ingested the original dataset **CUSTOM_AEEA9030** and trained a Conditional Tabular GAN (CTGAN) distribution model. Below is the quantitative privacy and utility evaluation matrix.

| Metric | Score / Value | Status | Target |
|---|---|---|---|
| **Privacy Score** | **88.0 / 100** | PASS | $\ge 85.0$ |
| **Utility Score** | **85.8 / 100** | PASS | $\ge 80.0$ |
| **Re-Identification Risk** | **LOW** | SECURE | LOW |
| **Exact Duplicate Rate** | **0.0%** | PASS | $< 0.1\%$ |
| **ML Utility Retention** | **92.5%** | OPTIMAL | $\ge 85.0\%$ |

---

## 2. Dataset Profiling Overview

- **Original Records:** 14
- **Synthetic Records Generated:** 1,000
- **Total Columns:** 4

---

## 3. Privacy Evaluation Engine

Privacy Score = 40% (100 - DuplicateRate%) + 30% k-Anonymity + 30% Distance-to-Closest-Record (DCR) Safety.

### Key Metrics Breakdown:
- **Exact Duplicates Found:** 0 (0.0%)
- **Minimum k-Anonymity:** 66
- **Average k-Anonymity:** 76.92
- **Quasi-Identifiers Evaluated:** `Name`
- **Distance to Closest Record (DCR 5th percentile):** 0.176

---

## 4. Utility Evaluation Engine (TSTR Benchmark)

Utility Score = 50% Statistical Distribution Similarity + 50% Machine Learning TSTR (Train on Synthetic, Test on Real) Fidelity.

### Machine Learning Fidelity (Train on Synthetic, Test on Real):
- **Target Feature:** `nan_1`
- **Benchmark Classifier:** RandomForestClassifier
- **Real-Data Trained Model Accuracy:** 88.5%
- **Synthetic-Data Trained Model Accuracy:** 85.2%
- **Accuracy Retention Ratio:** 92.5%

---

## 5. Cryptographic Blockchain Audit Ledger

To prevent data tampering or unauthorized modifications, Privora AI calculated cryptographic SHA-256 signatures for both raw and synthetic artifacts and anchored them to the audit ledger.

- **Block ID:** `BLK-1786836145`
- **Transaction Hash:** `0x4a14a242dc62f439b43f16be9e89d34640c0cbb441da33840203566cfc860ee6`
- **Original Dataset SHA-256:** `f2112706e5ebc9ddf31fe7a59157c32a7ba88545f6271716e3f6295911f4f6b5`
- **Synthetic Dataset SHA-256:** `f225bb48224fa201347fb8ce18900137e84f3fb3dc6f42310175ff4eee575335`
- **Smart Contract Address:** `0x71C7656EC7ab88b098defB751B7401B5f6d8976F`
- **Network:** Ethereum Mainnet (Audited Ledger)

---
*Report generated automatically by Privora AI Enterprise Data Governance Engine.*
