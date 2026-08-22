import sys
import os
import site
import warnings

user_site = site.getusersitepackages()
if user_site and user_site not in sys.path and os.path.exists(user_site):
    sys.path.insert(0, user_site)

import pandas as pd
import numpy as np

from typing import Dict, Any, List

class SmartExcelCleaner:
    @staticmethod
    def auto_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
        """Clean human-formatted Excel sheets without truncating rows or erasing NaNs."""
        if df.empty:
            return df

        # If df already has clean column headers (e.g. standard CSV file upload), preserve full dataset rows
        has_clean_headers = all(isinstance(c, str) and not c.startswith("Unnamed:") for c in df.columns[:3]) if len(df.columns) >= 2 else False

        if not has_clean_headers:
            # Detect actual header row among top 20 rows
            best_header_idx = None
            max_valid_cols = 0
            all_rows_sample = [df.columns.tolist()] + df.head(20).values.tolist()

            for idx, row in enumerate(all_rows_sample):
                valid_strs = [str(val).strip() for val in row if pd.notna(val) and str(val).strip() != "" and not str(val).startswith("Unnamed:") and not str(val).replace('.', '', 1).isdigit()]
                if len(valid_strs) > max_valid_cols:
                    max_valid_cols = len(valid_strs)
                    best_header_idx = idx

            if best_header_idx is not None and max_valid_cols >= 2:
                # Construct full dataframe using ALL rows starting after header row
                header_vals = [str(val).strip().replace('\n', ' ') for val in all_rows_sample[best_header_idx]]
                if best_header_idx == 0:
                    data_rows = df.values
                else:
                    data_rows = df.iloc[best_header_idx:].values
                df = pd.DataFrame(data_rows, columns=header_vals)

        # Clean column names & drop completely empty padding columns
        valid_cols = []
        for col in df.columns:
            col_str = str(col).strip()
            if col_str and not col_str.startswith("Unnamed:") and not col_str.lower().startswith("max marks") and not col_str.lower().startswith("subject name"):
                valid_cols.append(col)

        if valid_cols:
            df = df[valid_cols]

        df = df.dropna(how='all', axis=1)
        df = df.dropna(how='all', axis=0)

        # Deduplicate column names
        dedup_cols = []
        col_counts = {}
        for c in df.columns:
            c_name = str(c).strip()
            if c_name in col_counts:
                col_counts[c_name] += 1
                dedup_cols.append(f"{c_name}_{col_counts[c_name]}")
            else:
                col_counts[c_name] = 0
                dedup_cols.append(c_name)
        df.columns = dedup_cols

        # Preserve exact missingness (np.nan) without replacing with empty strings
        for idx, col in enumerate(df.columns):
            col_series = df.iloc[:, idx]
            # Replace string representations of NaN with actual np.nan
            if col_series.dtype == object:
                s_replaced = col_series.replace({'nan': np.nan, 'NaN': np.nan, 'None': np.nan, 'null': np.nan, 'NULL': np.nan, '': np.nan})
                df[col] = s_replaced

        return df.reset_index(drop=True)


class DataProfiler:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def detect_column_types(self) -> Dict[str, str]:
        """Detect explicit column types (numerical, categorical, boolean, datetime, id)."""
        column_types = {}
        total_rows = len(self.df)

        for col in self.df.columns:
            col_lower = str(col).lower().strip()
            unique_cnt = self.df[col].nunique(dropna=True)
            non_null_s = self.df[col].dropna()

            # 1. Primary Key / ID Detection (Strict match)
            if col_lower in ['id', 'patient_id', 'patientid', 'user_id', 'userid', 'roll_no', 'rollno', 'uuid']:
                column_types[col] = "id"
                continue

            if (col_lower.endswith('_id') or col_lower.startswith('id_')) and unique_cnt > 0.80 * total_rows:
                column_types[col] = "id"
                continue

            # 2. Datetime Detection
            if any(kw in col_lower for kw in ['date', 'time', 'timestamp', 'dob', 'created_at', 'updated_at', 'joined']):
                column_types[col] = "datetime"
                continue

            if non_null_s.dtype == object and len(non_null_s) > 0:
                sample_s = non_null_s.astype(str)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    parsed = pd.to_datetime(sample_s.head(50), errors='coerce', format='mixed')
                if parsed.notna().mean() > 0.80:
                    column_types[col] = "datetime"
                    continue

            # 3. Boolean Detection
            if non_null_s.dtype == bool or set(non_null_s.unique()).issubset({True, False, 1, 0, 'True', 'False', 'true', 'false', 'T', 'F', '1', '0'}):
                if unique_cnt <= 2:
                    column_types[col] = "boolean"
                    continue

            # 4. Categorical vs Numerical Detection
            if pd.api.types.is_numeric_dtype(non_null_s.dtype):
                if unique_cnt < 10 and not any(kw in col_lower for kw in ['age', 'score', 'mark', 'income', 'salary', 'time', 'month', 'val', 'price', 'cost']):
                    column_types[col] = "categorical"
                else:
                    column_types[col] = "numerical"
            else:
                column_types[col] = "categorical"

        return column_types

    def profile(self) -> Dict[str, Any]:
        """Generate comprehensive metadata profile."""
        col_types = self.detect_column_types()
        profile_cols = []

        for col in self.df.columns:
            sdtype = col_types.get(col, "categorical")
            s = self.df[col].dropna()
            
            c_info = {
                "name": col,
                "sdtype": sdtype,
                "null_count": int(self.df[col].isnull().sum()),
                "unique_count": int(self.df[col].nunique(dropna=True))
            }

            if sdtype == "numerical" and len(s) > 0:
                s_num = pd.to_numeric(s, errors='coerce').dropna()
                c_info["min"] = float(s_num.min()) if not s_num.empty else 0.0
                c_info["max"] = float(s_num.max()) if not s_num.empty else 0.0
                c_info["mean"] = float(s_num.mean()) if not s_num.empty else 0.0
                c_info["std"] = float(s_num.std()) if not s_num.empty else 0.0
            elif sdtype == "categorical" and len(s) > 0:
                c_info["top_categories"] = s.value_counts().head(5).to_dict()

            profile_cols.append(c_info)

        return {
            "num_rows": len(self.df),
            "num_columns": len(self.df.columns),
            "columns": profile_cols,
            "column_types": col_types
        }
