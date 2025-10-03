// Types for the recommendation system

export interface ArticleMetadata {
  article_id: number;
  category_id: number;
  words_count: number;
  created_date: string;
}

export interface Recommendation {
  article_id: number;
  score: number;
  reason: string;
  metadata: ArticleMetadata;
}

export interface UserStats {
  user_id: number;
  total_interactions: number;
  unique_articles: number;
  is_new_user: boolean;
}

export interface RecommendationResponse {
  user_id: number;
  method: string;
  actual_method: string;
  fallback_applied: boolean;
  recommendations: Recommendation[];
  metadata: {
    requested_method: string;
    actual_method: string;
    fallback_applied: boolean;
    fallback_reason: string | null;
    parameters: {
      n_recommendations: number;
      exclude_seen: boolean;
    };
    user_stats: UserStats;
    results_count: number;
  };
  generated_at: string;
}

export interface PopularArticle {
  rank: number;
  article_id: number;
  popularity_score: number;
  unique_users: number;
  total_clicks: number;
  metadata: ArticleMetadata;
}

export interface RecentArticle {
  rank: number;
  article_id: number;
  created_date: string;
  category_id: number;
  words_count: number;
  age_hours: number;
  metadata: ArticleMetadata;
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
  data_stats: {
    users_count: number;
    articles_count: number;
    interactions_count: number;
  };
}

export interface UserSegmentInfo {
  user_id: number;
  segment: number;
  segment_characteristics: {
    size: number;
    avg_clicks: number;
    avg_diversity: number;
    avg_words_preference: number;
    activity_level: number;
  };
  confidence: number;
}

export type RecommendationMethod = 'popularity' | 'content' | 'clustering' | 'hybrid';

export interface ActiveUser {
  user_id: number;
  total_clicks: number;
  unique_articles: number;
}
