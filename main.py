from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="SHL Recommendation API")


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


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: QueryRequest):
    """Placeholder recommendation endpoint.

    Replace the placeholder logic below with a search over your SHL dataset
    (CSV, database, etc.). The endpoint accepts a JSON body matching
    `QueryRequest` and returns a `RecommendationResponse` with the top
    recommended `Assessment` objects.
    """
    # Example placeholder response (replace with real search results)
    sample = Assessment(
        url="https://example.com",
        name="Python Test",
        adaptive_support="No",
        description="Measures Python skills",
        duration=30,
        remote_support="Yes",
        test_type=["Knowledge & Skills"],
    )

    return RecommendationResponse(recommended_assessments=[sample])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
