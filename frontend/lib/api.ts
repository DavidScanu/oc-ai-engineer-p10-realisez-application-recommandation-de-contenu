// API client for the recommendation backend

import {
  RecommendationResponse,
  PopularArticle,
  RecentArticle,
  HealthResponse,
  UserSegmentInfo,
  RecommendationMethod,
  ActiveUser
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  private async fetch<T>(endpoint: string, options?: RequestInit): Promise<T> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
        const errorMessage = error.detail || `HTTP error! status: ${response.status}`;
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      // Better error handling for network errors
      if (error instanceof Error) {
        throw error;
      }
      throw new Error(`Network error: ${String(error)}`);
    }
  }

  // Health check
  async getHealth(): Promise<HealthResponse> {
    return this.fetch<HealthResponse>('/health');
  }

  // Get recommendations for a user
  async getRecommendations(
    userId: number,
    method: RecommendationMethod = 'hybrid',
    nRecommendations: number = 5,
    excludeSeen: boolean = true
  ): Promise<RecommendationResponse> {
    const params = new URLSearchParams({
      method,
      n_recommendations: nRecommendations.toString(),
      exclude_seen: excludeSeen.toString(),
    });

    return this.fetch<RecommendationResponse>(
      `/recommend/${userId}?${params}`,
      { method: 'POST' }
    );
  }

  // Get list of users
  async getUsers(limit: number = 100): Promise<number[]> {
    return this.fetch<number[]>(`/users?limit=${limit}`);
  }

  // Get most active users
  async getMostActiveUsers(limit: number = 20): Promise<ActiveUser[]> {
    return this.fetch<ActiveUser[]>(`/users/active?limit=${limit}`);
  }

  // Get user statistics
  async getUserStats(userId: number): Promise<Record<string, unknown>> {
    return this.fetch(`/users/${userId}/stats`);
  }

  // Get user segment information
  async getUserSegment(userId: number): Promise<UserSegmentInfo> {
    return this.fetch<UserSegmentInfo>(`/users/${userId}/segment`);
  }

  // Get article information
  async getArticleInfo(articleId: number): Promise<Record<string, unknown>> {
    return this.fetch(`/articles/${articleId}`);
  }

  // Get popular articles
  async getPopularArticles(limit: number = 10): Promise<PopularArticle[]> {
    return this.fetch<PopularArticle[]>(`/articles/popular?limit=${limit}`);
  }

  // Get recent articles
  async getRecentArticles(
    hours?: number,
    categoryId?: number,
    limit: number = 10
  ): Promise<RecentArticle[]> {
    const params = new URLSearchParams({ limit: limit.toString() });
    if (hours) params.append('hours', hours.toString());
    if (categoryId) params.append('category_id', categoryId.toString());

    return this.fetch<RecentArticle[]>(`/articles/recent?${params}`);
  }

  // Get clusters characteristics
  async getClustersInfo(): Promise<Record<string, unknown>> {
    return this.fetch('/clusters');
  }

  // Debug endpoints
  async getConfig(): Promise<Record<string, unknown>> {
    return this.fetch('/debug/config');
  }

  async getDataStats(): Promise<Record<string, unknown>> {
    return this.fetch('/debug/data-stats');
  }
}

export const apiClient = new ApiClient();
