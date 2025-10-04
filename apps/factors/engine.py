import pandas as pd
import numpy as np

def zscore(series: pd.Series) -> pd.Series:
    return (series - series.mean()) / (series.std(ddof=0) + 1e-9)
