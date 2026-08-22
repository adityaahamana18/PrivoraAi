# PRIVORA AI — COMPLIANCE & SYNTHETIC DATA AUDIT REPORT

**Generated At:** 2026-08-15 23:18:17 UTC  
**Dataset Name:** CUSTOM_E8A7C527  
**Engine:** Privora CTGAN Engine v1.0  
**Verification Status:** VERIFIED & BLOCKCHAIN AUDITED  

---

## 1. Executive Summary

Privora AI successfully ingested the original dataset **CUSTOM_E8A7C527** and trained a Conditional Tabular GAN (CTGAN) distribution model. Below is the quantitative privacy and utility evaluation matrix.

| Metric | Score / Value | Status | Target |
|---|---|---|---|
| **Privacy Score** | **85.6 / 100** | PASS | $\ge 85.0$ |
| **Utility Score** | **82.3 / 100** | PASS | $\ge 80.0$ |
| **Re-Identification Risk** | **LOW** | SECURE | LOW |
| **Exact Duplicate Rate** | **0.0%** | PASS | $< 0.1\%$ |
| **ML Utility Retention** | **92.5%** | OPTIMAL | $\ge 85.0\%$ |

---

## 2. Dataset Profiling Overview

- **Original Records:** 14
- **Synthetic Records Generated:** 50
- **Total Columns:** 4

---

## 3. Privacy Evaluation Engine

Privacy Score = 40% (100 - DuplicateRate%) + 30% k-Anonymity + 30% Distance-to-Closest-Record (DCR) Safety.

### Key Metrics Breakdown:
- **Exact Duplicates Found:** 0 (0.0%)
- **Minimum k-Anonymity:** 2
- **Average k-Anonymity:** 4.55
- **Quasi-Identifiers Evaluated:** `3`
- **Distance to Closest Record (DCR 5th percentile):** 0.082

---

## 4. Utility Evaluation Engine (TSTR Benchmark)

Utility Score = 50% Statistical Distribution Similarity + 50% Machine Learning TSTR (Train on Synthetic, Test on Real) Fidelity.

### Machine Learning Fidelity (Train on Synthetic, Test on Real):
- **Target Feature:** `4`
- **Benchmark Classifier:** RandomForestClassifier
- **Real-Data Trained Model Accuracy:** 88.5%
- **Synthetic-Data Trained Model Accuracy:** 85.2%
- **Accuracy Retention Ratio:** 92.5%

---

## 5. Cryptographic Blockchain Audit Ledger

To prevent data tampering or unauthorized modifications, Privora AI calculated cryptographic SHA-256 signatures for both raw and synthetic artifacts and anchored them to the audit ledger.

- **Block ID:** `BLK-1786835897`
- **Transaction Hash:** `0x04e4d77ba312ee5f311f6d44ac94758b3299a4c39eaf40799fc13664c6af15da`
- **Original Dataset SHA-256:** `2c7fecae18089d02a77a2e634afe93e097d0f1fb9f3ef6ce06968db062ae7ea4`
- **Synthetic Dataset SHA-256:** `e7044808407458ae322d6ae344f9c20ecd31011e14f2be4669965dd34df15201`
- **Smart Contract Address:** `0x71C7656EC7ab88b098defB751B7401B5f6d8976F`
- **Network:** Ethereum Mainnet (Audited Ledger)

---
*Report generated automatically by Privora AI Enterprise Data Governance Engine.*
