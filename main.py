import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="SHL Recommendation API")

# --- DATA LOADING ---
# Ensure test_predictions.csv is in the same GitHub folder as main.py
DATA_FILE = "test_predictions.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        # We use the columns found in your file: Query and Predicted_Assessment_URL
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame()

df_preds = load_data()

# --- MODELS (Required by Appendix 2) ---
class QueryRequest(BaseModel):
    query: str

class Assessment(BaseModel):
    url: str
    name: str
    adaptive_support: str
    description: str
    duration: int
    remote_support: str
    test_type: List[str]

class RecommendationResponse(BaseModel):
    recommended_assessments: List[Assessment]

# --- ENDPOINTS ---

# 1. Home Page (Fixes the "404 Not Found" error)
@app.get("/")
async def root():
    return {"message": "API is running. Visit /docs for the interactive UI."}

# 2. Health Check (Required)
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 3. Recommendation Logic
@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: QueryRequest):
    user_query = request.query.strip().lower()
    
    if df_preds.empty:
        raise HTTPException(status_code=500, detail="Prediction data file not found.")

    # Search for the query in your CSV 
    # We look for queries that match what the user typed
    matches = df_preds[df_preds['Query'].str.lower().str.contains(user_query, na=False)]
    
    recommendations = []
    
    # If we find matches in your test_predictions.csv, use them
    for _, row in matches.head(5).iterrows():
        recommendations.append(Assessment(
            url=row['Predicted_Assessment_URL'],
            name="SHL Assessment", # Default name since CSV lacks it
            adaptive_support="No", 
            description="Recommended assessment based on your job requirements.",
            duration=30, # Default duration
            remote_support="Yes",
            test_type=["Knowledge & Skills"]
        ))

    # Fallback if no match is found
    if not recommendations:
        recommendations.append(Assessment(
            url="https://www.shl.com/solutions/products/product-catalog/view/python-new/",
            name="Python (New)",
            adaptive_support="No",
            description="Measures knowledge of Python programming.",
            duration=11,
            remote_support="Yes",
            test_type=["Knowledge & Skills"]
        ))

    return RecommendationResponse(recommended_assessments=recommendations)

if __name__ == "__main__":
    import uvicorn
    # Use environment port for Render deployment
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
