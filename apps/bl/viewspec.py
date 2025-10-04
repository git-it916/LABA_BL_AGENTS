from pydantic import BaseModel, Field
import numpy as np

class BLView(BaseModel):
    P: np.ndarray = Field(..., description="(k,n) pick matrix")
    q: np.ndarray = Field(..., description="(k,) view returns")
    Omega: np.ndarray = Field(..., description="(k,k) view uncertainty (PD)")
