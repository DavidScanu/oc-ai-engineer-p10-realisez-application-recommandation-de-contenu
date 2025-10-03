'use client';

import { useState, useEffect, useCallback } from 'react';
import { apiClient } from '@/lib/api';
import { RecommendationMethod, RecommendationResponse } from '@/lib/types';
import { UserSelector } from '@/components/UserSelector';
import { Footer } from '@/components/Footer';
import { MethodSelector } from '@/components/MethodSelector';
import { RecommendationCard } from '@/components/RecommendationCard';
import { UserStatsCard } from '@/components/UserStatsCard';
import { FallbackAlert } from '@/components/FallbackAlert';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, TrendingUp, Clock, BarChart3 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';

export default function HomePage() {
  const [selectedUserId, setSelectedUserId] = useState<number | undefined>();
  const [method, setMethod] = useState<RecommendationMethod>('hybrid');
  const [recommendations, setRecommendations] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecommendations = useCallback(async () => {
    if (!selectedUserId) return;

    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.getRecommendations(selectedUserId, method, 5, true);
      setRecommendations(response);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Une erreur est survenue';
      console.error('Error fetching recommendations:', errorMessage);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [selectedUserId, method]);

  useEffect(() => {
    if (selectedUserId) {
      fetchRecommendations();
    }
  }, [selectedUserId, method, fetchRecommendations]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                My Content
              </h1>
              <p className="text-muted-foreground mt-1">
                Système de recommandation de contenu personnalisé
              </p>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/statistics">
                <Badge variant="outline" className="text-sm cursor-pointer hover:bg-accent flex items-center gap-1">
                  <BarChart3 className="h-3 w-3" />
                  Statistiques
                </Badge>
              </Link>
              <Link href="/insights">
                <Badge variant="outline" className="text-sm cursor-pointer hover:bg-accent flex items-center gap-1">
                  <BarChart3 className="h-3 w-3" />
                  Insights
                </Badge>
              </Link>
              <Badge variant="outline" className="text-sm">
                v1.0.0
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Sidebar - User Selection & Stats */}
          <div className="space-y-6">
            <UserSelector
              selectedUserId={selectedUserId}
              onUserSelect={setSelectedUserId}
            />

            {recommendations?.metadata.user_stats && (
              <UserStatsCard stats={recommendations.metadata.user_stats} />
            )}
          </div>

          {/* Main Content - Recommendations */}
          <div className="lg:col-span-2 space-y-6">
            {/* Method Selector */}
            <Card>
              <CardHeader>
                <CardTitle>Paramètres de recommandation</CardTitle>
                <CardDescription>
                  Sélectionnez la méthode de recommandation à utiliser
                </CardDescription>
              </CardHeader>
              <CardContent>
                <MethodSelector method={method} onMethodChange={setMethod} />
              </CardContent>
            </Card>

            {/* Fallback Alert */}
            {recommendations && (
              <FallbackAlert
                fallbackApplied={recommendations.fallback_applied}
                fallbackReason={recommendations.metadata.fallback_reason}
                requestedMethod={recommendations.method}
                actualMethod={recommendations.actual_method}
              />
            )}

            {/* Recommendations List */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Recommandations
                  {recommendations && (
                    <Badge variant="secondary" className="ml-2">
                      {recommendations.recommendations.length} articles
                    </Badge>
                  )}
                </CardTitle>
                <CardDescription>
                  Articles recommandés pour l&apos;utilisateur sélectionné
                  {recommendations && (
                    <span className="flex items-center gap-1 mt-1">
                      <Clock className="h-3 w-3" />
                      Généré le {new Date(recommendations.generated_at).toLocaleString('fr-FR')}
                    </span>
                  )}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {error ? (
                  <div className="text-center py-12">
                    <p className="text-destructive mb-2 font-semibold">Erreur: {error}</p>
                    <p className="text-sm text-muted-foreground">
                      Assurez-vous que le backend est démarré sur http://localhost:8000
                    </p>
                  </div>
                ) : loading ? (
                  <div className="flex items-center justify-center py-12">
                    <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
                  </div>
                ) : recommendations && recommendations.recommendations.length > 0 ? (
                  <div className="space-y-4">
                    {recommendations.recommendations.map((rec, index) => (
                      <RecommendationCard
                        key={rec.article_id}
                        recommendation={rec}
                        rank={index + 1}
                      />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-12 text-muted-foreground">
                    <p>Sélectionnez un utilisateur pour voir les recommandations</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}
