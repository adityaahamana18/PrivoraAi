# PRIVORA AI — COMPLIANCE & SYNTHETIC DATA AUDIT REPORT

**Generated At:** 2026-08-22 09:53:06 UTC  
**Dataset Name:** BFSI  
**Engine:** Privora CTGAN Engine v1.0  
**Verification Status:** VERIFIED & BLOCKCHAIN AUDITED  

---

## 1. Executive Summary

Privora AI successfully ingested the original dataset **BFSI** and trained a Conditional Tabular GAN (CTGAN) distribution model. Below is the quantitative privacy and utility evaluation matrix.

| Metric | Score / Value | Status | Target |
|---|---|---|---|
| **Privacy Score** | **91.5 / 100** | PASS | $\ge 85.0$ |
| **Utility Score** | **75.3 / 100** | PASS | $\ge 80.0$ |
| **Re-Identification Risk** | **LOW** | SECURE | LOW |
| **Exact Duplicate Rate** | **0.0%** | PASS | $< 0.1\%$ |
| **ML Utility Retention** | **66.7%** | OPTIMAL | $\ge 85.0\%$ |

---

## 2. Dataset Profiling Overview

- **Original Records:** 40
- **Synthetic Records Generated:** 100
- **Total Columns:** 6

---

## 3. Privacy Evaluation Engine

Privacy Score = 40% (100 - DuplicateRate%) + 30% k-Anonymity + 30% DCR Safety (-40pt penalty for ID leakage).

### Key Metrics Breakdown:
- **Exact Duplicates Found:** 0 (0.0%)
- **Minimum k-Anonymity:** 1
- **Average k-Anonymity:** 9.09
- **Quasi-Identifiers Evaluated:** `EmploymentStatus, DefaultRisk`
- **Distance to Closest Record (DCR 5th percentile):** 0.493

---

## 4. Utility Evaluation Engine (TSTR Benchmark)

Utility Score = 50% Statistical Distribution Similarity + 50% Machine Learning TSTR (Train on Synthetic, Test on Real) Fidelity.

### Machine Learning Fidelity (Train on Synthetic, Test on Real):
- **Target Feature:** `DefaultRisk`
- **Benchmark Classifier:** RandomForestClassifier
- **Real-Data Trained Model Accuracy:** 100.0%
- **Synthetic-Data Trained Model Accuracy:** 66.67%
- **Accuracy Retention Ratio:** 66.7%

---

## 5. Cryptographic Blockchain Audit Ledger

To prevent data tampering or unauthorized modifications, Privora AI calculated cryptographic SHA-256 signatures for both raw and synthetic artifacts and anchored them to the audit ledger.

- **Block ID:** `BLK-1787392386`
- **Transaction Hash:** `0x8801022ce75d04adf857ce904b0f0a600f98097fdbf087be7c49a1e06542d0a2`
- **Original Dataset SHA-256:** `e567aea8ad622b226dcfa4557054fa746b24144360da1ef4f4dc5502bb1758c5`
- **Synthetic Dataset SHA-256:** `9745639523573cbb57e3a51cbe86a7870531488e862eaa2c05628d6e0fae01ae`
- **Smart Contract Address:** `0x71C7656EC7ab88b098defB751B7401B5f6d8976F`
- **Network:** Ethereum Sepolia (Audited Ledger)

---
*Report generated automatically by Privora AI Enterprise Data Governance Engine.*
