'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { ActiveUser } from '@/lib/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, Users, TrendingUp, Activity, Database, Calendar, FileText, BarChart3 } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import Link from 'next/link';

interface DataStats {
  categories_count?: number;
  avg_words_per_article?: number;
  interactions_per_user?: number;
  date_range?: {
    min_article_date?: string;
    max_article_date?: string;
  };
  reference_date?: string;
  unique_users?: number;
  total_articles?: number;
  total_interactions?: number;
}

export default function StatisticsPage() {
  const [activeUsers, setActiveUsers] = useState<ActiveUser[]>([]);
  const [dataStats, setDataStats] = useState<DataStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const [usersData, statsData] = await Promise.all([
          apiClient.getMostActiveUsers(10),
          apiClient.getDataStats(),
        ]);
        setActiveUsers(usersData);
        setDataStats(statsData as DataStats);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Une erreur est survenue';
        console.error('Error fetching statistics:', errorMessage);
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const formatDate = (dateStr?: string) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Statistiques
              </h1>
              <p className="text-muted-foreground mt-1">
                Vue d&apos;ensemble des données et utilisateurs actifs
              </p>
            </div>
            <Link href="/">
              <Badge variant="outline" className="text-sm cursor-pointer hover:bg-accent">
                ← Retour aux recommandations
              </Badge>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          </div>
        ) : error ? (
          <Card className="border-destructive">
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-destructive mb-2 font-semibold">Erreur: {error}</p>
                <p className="text-sm text-muted-foreground">
                  Assurez-vous que le backend est démarré sur http://localhost:8000
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-6">
            {/* Overview Stats */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Utilisateurs</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dataStats?.unique_users?.toLocaleString() || 'N/A'}</div>
                  <p className="text-xs text-muted-foreground mt-1">
                    Utilisateurs totaux
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Articles</CardTitle>
                  <FileText className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dataStats?.total_articles?.toLocaleString() || 'N/A'}</div>
                  <p className="text-xs text-muted-foreground mt-1">
                    Articles disponibles
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Interactions</CardTitle>
                  <Activity className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dataStats?.total_interactions?.toLocaleString() || 'N/A'}</div>
                  <p className="text-xs text-muted-foreground mt-1">
                    Interactions totales
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Catégories</CardTitle>
                  <Database className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{dataStats?.categories_count?.toLocaleString() || 'N/A'}</div>
                  <p className="text-xs text-muted-foreground mt-1">
                    Catégories d&apos;articles
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Additional Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <FileText className="h-4 w-4" />
                    Mots par article
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">
                    {dataStats?.avg_words_per_article?.toFixed(0) || 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Moyenne</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <BarChart3 className="h-4 w-4" />
                    Interactions par utilisateur
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-3xl font-bold">
                    {dataStats?.interactions_per_user?.toFixed(1) || 'N/A'}
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Moyenne</p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Période des données
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm space-y-1">
                    <div>
                      <span className="font-semibold">Du:</span> {formatDate(dataStats?.date_range?.min_article_date)}
                    </div>
                    <div>
                      <span className="font-semibold">Au:</span> {formatDate(dataStats?.date_range?.max_article_date)}
                    </div>
                    <div className="pt-2 border-t mt-2">
                      <span className="font-semibold">Référence:</span> {formatDate(dataStats?.reference_date)}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Top 10 Active Users */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5" />
                  Top 10 Utilisateurs Actifs
                </CardTitle>
                <CardDescription>
                  Les utilisateurs avec le plus d&apos;interactions
                </CardDescription>
              </CardHeader>
              <CardContent>
                {activeUsers.length > 0 ? (
                  <div className="space-y-3">
                    {activeUsers.map((user, index) => (
                      <div
                        key={user.user_id}
                        className="flex items-center justify-between p-4 rounded-lg border bg-card hover:bg-accent transition-colors"
                      >
                        <div className="flex items-center gap-4">
                          <div className="flex items-center justify-center w-10 h-10 rounded-full bg-primary/10 text-primary font-bold">
                            {index + 1}
                          </div>
                          <div>
                            <p className="font-semibold text-lg">Utilisateur #{user.user_id}</p>
                            <p className="text-sm text-muted-foreground">
                              {user.unique_articles} articles uniques consultés
                            </p>
                          </div>
                        </div>
                        <div className="text-right">
                          <Badge variant="secondary" className="text-base px-3 py-1">
                            {user.total_clicks.toLocaleString()} clics
                          </Badge>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    Aucune donnée disponible
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
}
