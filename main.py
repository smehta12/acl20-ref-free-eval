import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

from ref_free_metrics.supert import Supert

app = FastAPI()

class RankingInput(BaseModel):
    doc_id: str
    doc: str
    summaries: List[str]

@app.get("/", tags=["root"])
def home():
    return "Welcome to Summary Raking Service based on SUPERT!"


@app.post("/rank", tags=["ranking"])
def rank(ranking_input: RankingInput):
    source_doc = [(ranking_input.doc_id, ranking_input.doc)]
    supert = Supert(source_doc)
    scores = supert(ranking_input.summaries)

    summary_scores = dict(zip(ranking_input.summaries, scores))
    sorted_by_scores = dict(sorted(summary_scores.items(), key=lambda item: item[1], reverse=True))

    return sorted_by_scores

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True, log_level="info")
