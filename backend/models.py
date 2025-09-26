# backend/models.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class ArticleMetadata(BaseModel):
    article_id: int
    category_id: int
    created_at_ts: int
    publisher_id: int
    words_count: int

class UserInteraction(BaseModel):
    user_id: int
    session_id: str
    click_article_id: int
    click_timestamp: int
    click_environment: int
    click_deviceGroup: int
    click_os: int
    click_country: int
    click_region: int
    click_referrer_type: int

class RecommendationRequest(BaseModel):
    user_id: int
    method: str = "hybrid"  # popularity, content, clustering, hybrid
    exclude_seen: bool = True

class RecommendationResponse(BaseModel):
    user_id: int
    method: str
    recommendations: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    generated_at: datetime

class UserSegmentInfo(BaseModel):
    user_id: int
    segment: int
    segment_characteristics: Dict[str, Any]
    confidence: float

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    data_stats: Dict[str, Any]