import sys
import os
import site

user_site = site.getusersitepackages()
if user_site and user_site not in sys.path and os.path.exists(user_site):
    sys.path.insert(0, user_site)

import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional


class PrivoraGenerator:
    def __init__(self, epochs: int = 300):
        self.epochs = epochs
        self.synthesizer = None
        self.metadata = None
        self.is_trained = False
        self.used_fallback = False
        self.column_stats = {}
        self.real_df_reference = None

    def fit(self, data: pd.DataFrame, epochs: Optional[int] = None, engine: str = "ctgan") -> Dict[str, Any]:
        """Fit the CTGAN or fallback synthesizer on real dataframe."""
        if epochs is not None:
            self.epochs = epochs
            
        print(f"[PrivoraGenerator] Fitting model on {len(data)} rows with engine={engine}, epochs={self.epochs}...")
        self.real_df_reference = data.copy()

        # Learn strict statistical baseline profiles for calibration
        self._fit_fallback(data)

        if engine.lower() in ["copula", "statistical", "gaussian"]:
            self.is_trained = True
            self.used_fallback = True
            return {"status": "success", "engine": "StatisticalCopulaEngine", "epochs": self.epochs}

        try:
            from sdv.metadata import SingleTableMetadata
            from sdv.single_table import CTGANSynthesizer

            metadata = SingleTableMetadata()
            metadata.detect_from_dataframe(data)
            self.metadata = metadata

            effective_epochs = min(self.epochs, 20)
            synthesizer = CTGANSynthesizer(
                metadata=metadata,
                epochs=effective_epochs,
                verbose=False
            )
            synthesizer.fit(data)
            self.synthesizer = synthesizer
            self.is_trained = True
            self.used_fallback = False
            return {"status": "success", "engine": "CTGAN", "epochs": effective_epochs}
            
        except Exception as e:
            print(f"[PrivoraGenerator] SDV CTGAN warning/fallback: {e}. Utilizing Statistical Copula Engine.")
            self.is_trained = True
            self.used_fallback = True
            return {"status": "success", "engine": "StatisticalCopulaEngine", "warning": str(e)}

    def _fit_fallback(self, data: pd.DataFrame):
        """Statistical copula engine using strict schema type profiling."""
        from profiler import DataProfiler

        self.column_stats = {}
        self.column_stats['columns_order'] = data.columns.tolist()
        self.column_stats['dtypes'] = data.dtypes.to_dict()

        profiler = DataProfiler(data)
        col_types = profiler.detect_column_types()
        self.column_stats['col_types'] = col_types

        id_cols = [c for c, t in col_types.items() if t == "id"]
        datetime_cols = [c for c, t in col_types.items() if t == "datetime"]
        boolean_cols = [c for c, t in col_types.items() if t == "boolean"]
        categorical_cols = [c for c, t in col_types.items() if t == "categorical"]
        numeric_cols = [c for c, t in col_types.items() if t == "numerical"]

        # 1. Missingness per column (Preserve np.nan rates)
        missingness = {}
        for col in data.columns:
            missingness[col] = data[col].isnull().mean()
        self.column_stats['missingness'] = missingness

        # 2. Learn numeric distributions & exact bounds
        if numeric_cols:
            num_data = data[numeric_cols].copy()
            for c in numeric_cols:
                num_data[c] = pd.to_numeric(num_data[c], errors='coerce').fillna(data[c].mean() if pd.api.types.is_numeric_dtype(data[c]) else 0)
            
            means = num_data.mean()
            stds = num_data.std().fillna(1.0)
            covs = num_data.cov()
            self.column_stats['numeric'] = {
                'cols': numeric_cols,
                'means': means,
                'stds': stds,
                'covs': covs,
                'min': data[numeric_cols].min(),
                'max': data[numeric_cols].max(),
                'is_int': {c: pd.api.types.is_integer_dtype(data[c]) or 'age' in c.lower() or 'roll' in c.lower() or 'cycle' in c.lower() or 'month' in c.lower() for c in numeric_cols}
            }

        # 3. Learn categorical PMF probabilities
        self.column_stats['categorical'] = {}
        for col in categorical_cols:
            valid_s = data[col].dropna()
            if valid_s.empty:
                probs = pd.Series({'Unknown': 1.0})
            else:
                probs = valid_s.value_counts(normalize=True)
            self.column_stats['categorical'][col] = probs

        # 4. Learn boolean PMF probabilities
        self.column_stats['boolean'] = {}
        for col in boolean_cols:
            valid_s = data[col].dropna()
            if valid_s.empty:
                probs = pd.Series({True: 0.5, False: 0.5})
            else:
                probs = valid_s.value_counts(normalize=True)
            self.column_stats['boolean'][col] = probs

        # 5. Learn Datetime ranges & format
        self.column_stats['datetime'] = {}
        for col in datetime_cols:
            valid_dt = pd.to_datetime(data[col].dropna(), errors='coerce').dropna()
            if valid_dt.empty:
                min_dt, max_dt = pd.Timestamp("2020-01-01"), pd.Timestamp("2024-01-01")
            else:
                min_dt, max_dt = valid_dt.min(), valid_dt.max()
            self.column_stats['datetime'][col] = {
                'min_ts': int(min_dt.timestamp()),
                'max_ts': int(max_dt.timestamp())
            }

        # 6. Learn ID pattern prefix
        self.column_stats['id_patterns'] = {}
        for col in id_cols:
            valid_ids = data[col].dropna()
            sample_val = str(valid_ids.iloc[0]) if not valid_ids.empty else "P-000"
            raw_prefix = ''.join([c for c in sample_val if not c.isdigit()]) or "P-"
            prefix = f"SYN-{raw_prefix}" if not raw_prefix.startswith("SYN") else raw_prefix
            num_digits = max(4, sum(1 for c in sample_val if c.isdigit()))
            self.column_stats['id_patterns'][col] = {'prefix': prefix, 'digits': num_digits}

    def sample(self, num_rows: int = 1000) -> pd.DataFrame:
        """Sample synthetic dataframe from trained model with distribution calibration."""
        if not self.is_trained:
            raise ValueError("Generator must be fitted before sampling.")

        if self.synthesizer is not None and not self.used_fallback:
            try:
                raw_synth = self.synthesizer.sample(num_rows=num_rows)
            except Exception:
                raw_synth = self._sample_fallback(num_rows)
        else:
            raw_synth = self._sample_fallback(num_rows)

        # High-Fidelity Distribution Alignment & Missingness Calibrator
        calibrated_synth = self._calibrate_distributions(raw_synth, num_rows)
        return calibrated_synth

    def _sample_fallback(self, num_rows: int) -> pd.DataFrame:
        """Generate synthetic rows with strict schema data-type preservation."""
        synth_df = pd.DataFrame()
        col_types = self.column_stats.get('col_types', {})

        # 1. ID Columns
        id_cols = [c for c, t in col_types.items() if t == "id"]
        for col in id_cols:
            pat = self.column_stats.get('id_patterns', {}).get(col, {'prefix': 'SYN-P-', 'digits': 6})
            prefix = pat['prefix']
            digits = pat['digits']
            synth_df[col] = [f"{prefix}{i+1:0{digits}d}" for i in range(num_rows)]

        # 2. Datetime Columns
        dt_cols = [c for c, t in col_types.items() if t == "datetime"]
        for col in dt_cols:
            dt_info = self.column_stats.get('datetime', {}).get(col, {'min_ts': 1577836800, 'max_ts': 1704067200})
            min_ts = dt_info['min_ts']
            max_ts = dt_info['max_ts']
            rand_ts = np.random.randint(min_ts, max(min_ts + 1, max_ts), size=num_rows)
            synth_df[col] = pd.to_datetime(rand_ts, unit='s').strftime('%Y-%m-%d')

        # 3. Boolean Columns
        bool_cols = [c for c, t in col_types.items() if t == "boolean"]
        for col in bool_cols:
            probs = self.column_stats.get('boolean', {}).get(col)
            if probs is not None and not probs.empty:
                vals = probs.index.tolist()
                p_vals = np.array(probs.values) / np.sum(probs.values)
                synth_df[col] = np.random.choice(vals, size=num_rows, p=p_vals)

        # 4. Categorical Columns
        cat_cols = [c for c, t in col_types.items() if t == "categorical"]
        for col in cat_cols:
            probs = self.column_stats.get('categorical', {}).get(col)
            if probs is not None and not probs.empty:
                cats = probs.index.tolist()
                p_vals = np.array(probs.values) / np.sum(probs.values)
                synth_df[col] = np.random.choice(cats, size=num_rows, p=p_vals)

        # 5. Numerical Columns
        if 'numeric' in self.column_stats and self.column_stats['numeric']['cols']:
            n_info = self.column_stats['numeric']
            cols = n_info['cols']
            means = n_info['means'].values
            covs = n_info['covs'].values

            covs = np.nan_to_num(covs) + np.eye(len(cols)) * 1e-5
            samples = np.random.multivariate_normal(means, covs, size=num_rows)

            for idx, col in enumerate(cols):
                col_samples = samples[:, idx]
                c_min = n_info['min'][col]
                c_max = n_info['max'][col]

                if pd.notna(c_min) and pd.notna(c_max):
                    col_samples = np.clip(col_samples, c_min, c_max)

                if n_info['is_int'].get(col, False):
                    col_samples = np.round(col_samples).astype(int)

                synth_df[col] = col_samples

        cols_order = self.column_stats.get('columns_order', synth_df.columns.tolist())
        for c in cols_order:
            if c not in synth_df.columns:
                synth_df[c] = np.nan

        return synth_df[cols_order].copy()

    def _calibrate_distributions(self, synth_df: pd.DataFrame, num_rows: int) -> pd.DataFrame:
        """High-Fidelity Distribution Alignment & Missingness Calibrator."""
        calibrated = synth_df.copy()

        # 1. Categorical & Boolean PMF Frequency Rebalancer
        cat_stats = self.column_stats.get('categorical', {})
        bool_stats = self.column_stats.get('boolean', {})

        all_cats = {**cat_stats, **bool_stats}
        for col, probs in all_cats.items():
            if col in calibrated.columns and probs is not None and not probs.empty:
                categories = probs.index.tolist()
                p_vals = np.array(probs.values) / np.sum(probs.values)
                calibrated[col] = np.random.choice(categories, size=num_rows, p=p_vals)

        # 2. Numerical Quantile & Mean/Std Distribution Alignment
        if 'numeric' in self.column_stats and self.column_stats['numeric']['cols']:
            n_info = self.column_stats['numeric']
            cols = n_info['cols']
            means = n_info['means']
            stds = n_info['stds']
            mins = n_info['min']
            maxs = n_info['max']

            for col in cols:
                if col in calibrated.columns:
                    target_mean = means[col]
                    target_std = stds[col]
                    curr_s = pd.to_numeric(calibrated[col], errors='coerce').dropna()

                    if len(curr_s) > 0:
                        curr_mean = curr_s.mean()
                        curr_std = curr_s.std()

                        if curr_std > 1e-6 and pd.notna(target_std) and target_std > 1e-6:
                            calibrated_col = target_mean + (target_std / curr_std) * (calibrated[col] - curr_mean)
                        else:
                            calibrated_col = calibrated[col] + (target_mean - curr_mean)

                        c_min = mins[col]
                        c_max = maxs[col]
                        if pd.notna(c_min) and pd.notna(c_max):
                            calibrated_col = np.clip(calibrated_col, c_min, c_max)

                        if n_info['is_int'].get(col, False):
                            calibrated_col = np.round(calibrated_col).astype(int)

                        calibrated[col] = calibrated_col

        # 3. Exact Missingness (NaN) Injection matching real dataset missingness rates
        missingness = self.column_stats.get('missingness', {})
        id_cols = [c for c, t in self.column_stats.get('col_types', {}).items() if t == "id"]
        for col in calibrated.columns:
            p_missing = missingness.get(col, 0.0)
            if p_missing > 0.005 and col not in id_cols:
                mask = np.random.rand(num_rows) < p_missing
                calibrated.loc[mask, col] = np.nan

        # 4. Exact Data-Type Harmonization
        target_dtypes = self.column_stats.get('dtypes', {})
        res_df = calibrated.copy()

        for col, target_dtype in target_dtypes.items():
            if col in res_df.columns:
                try:
                    if pd.api.types.is_integer_dtype(target_dtype):
                        s_num = pd.to_numeric(res_df[col], errors='coerce')
                        if s_num.isnull().any():
                            res_df[col] = s_num.round().astype('Int64')
                        else:
                            res_df[col] = s_num.round().astype(int)
                    elif pd.api.types.is_float_dtype(target_dtype):
                        res_df[col] = pd.to_numeric(res_df[col], errors='coerce')
                except Exception:
                    pass

        return res_df

    def save(self, filepath: str):
        """Save trained synthesizer model to file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if self.synthesizer is not None and not self.used_fallback:
            try:
                self.synthesizer.save(filepath)
                return
            except Exception:
                pass

        with open(filepath, 'wb') as f:
            pickle.dump({'column_stats': self.column_stats, 'used_fallback': True}, f)

    @classmethod
    def load(cls, filepath: str) -> "PrivoraGenerator":
        """Load trained synthesizer model from file."""
        inst = cls()
        try:
            from sdv.single_table import CTGANSynthesizer
            inst.synthesizer = CTGANSynthesizer.load(filepath)
            inst.is_trained = True
            inst.used_fallback = False
        except Exception:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
                inst.column_stats = data.get('column_stats', {})
                inst.used_fallback = True
                inst.is_trained = True
        return inst
