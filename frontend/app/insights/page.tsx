'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import { PopularArticle, RecentArticle } from '@/lib/types';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { TrendingUp, Clock, Sparkles, FileText, Tag, Calendar, MousePointerClick } from 'lucide-react';
import Link from 'next/link';
import { Footer } from '@/components/Footer';

export default function InsightsPage() {
  const [popularArticles, setPopularArticles] = useState<PopularArticle[]>([]);
  const [recentArticles, setRecentArticles] = useState<RecentArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [popular, recent] = await Promise.all([
        apiClient.getPopularArticles(10),
        apiClient.getRecentArticles(48, undefined, 10)
      ]);
      setPopularArticles(popular);
      setRecentArticles(recent);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Une erreur est survenue';
      console.error('Error fetching insights:', errorMessage);
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <header className="bg-white border-b sticky top-0 z-50 shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Insights & Analytics
              </h1>
              <p className="text-muted-foreground mt-1">
                Découvrez les articles tendances et nouveautés
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

      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="popular" className="space-y-6">
          <TabsList className="grid w-full max-w-md mx-auto grid-cols-2">
            <TabsTrigger value="popular" className="flex items-center gap-2">
              <TrendingUp className="h-4 w-4" />
              Articles populaires
            </TabsTrigger>
            <TabsTrigger value="recent" className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              Articles récents
            </TabsTrigger>
          </TabsList>

          <TabsContent value="popular" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-yellow-500" />
                  Top 10 articles populaires
                </CardTitle>
                <CardDescription>
                  Articles les plus consultés récemment (score de popularité normalisé)
                </CardDescription>
              </CardHeader>
              <CardContent>
                {error ? (
                  <div className="text-center py-8">
                    <p className="text-destructive mb-2">Erreur: {error}</p>
                    <p className="text-sm text-muted-foreground">
                      Assurez-vous que le backend est démarré sur http://localhost:8000
                    </p>
                  </div>
                ) : loading ? (
                  <div className="text-center py-8 text-muted-foreground">Chargement...</div>
                ) : (
                  <div className="space-y-3">
                    {popularArticles.map((article) => (
                      <Card key={article.article_id} className="hover:shadow-md transition-shadow">
                        <CardContent className="pt-6">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <Badge variant="secondary">#{article.rank}</Badge>
                                <h3 className="font-semibold">Article {article.article_id}</h3>
                              </div>
                              <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                                <div className="flex items-center gap-1">
                                  <Calendar className="h-4 w-4" />
                                  <span>{formatDate(article.metadata.created_date)}</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <Tag className="h-4 w-4" />
                                  <span>Cat. {article.metadata.category_id}</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <FileText className="h-4 w-4" />
                                  <span>{article.metadata.words_count} mots</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <TrendingUp className="h-4 w-4" />
                                  <span>{article.unique_users} utilisateurs</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <MousePointerClick className="h-4 w-4" />
                                  <span>{article.total_clicks} clics</span>
                                </div>
                              </div>
                            </div>
                            <Badge variant="info" className="ml-2">
                              Score: {article.popularity_score.toFixed(2)}
                            </Badge>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="recent" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5 text-blue-500" />
                  Articles récents (48h)
                </CardTitle>
                <CardDescription>
                  Nouveaux articles publiés dans les dernières 48 heures
                </CardDescription>
              </CardHeader>
              <CardContent>
                {error ? (
                  <div className="text-center py-8">
                    <p className="text-destructive mb-2">Erreur: {error}</p>
                    <p className="text-sm text-muted-foreground">
                      Assurez-vous que le backend est démarré sur http://localhost:8000
                    </p>
                  </div>
                ) : loading ? (
                  <div className="text-center py-8 text-muted-foreground">Chargement...</div>
                ) : recentArticles.length > 0 ? (
                  <div className="space-y-3">
                    {recentArticles.map((article) => (
                      <Card key={article.article_id} className="hover:shadow-md transition-shadow">
                        <CardContent className="pt-6">
                          <div className="flex items-start justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <Badge variant="secondary">#{article.rank}</Badge>
                                <h3 className="font-semibold">Article {article.article_id}</h3>
                                <Badge variant="success" className="text-xs">
                                  Nouveau
                                </Badge>
                              </div>
                              <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                                <div className="flex items-center gap-1">
                                  <Calendar className="h-4 w-4" />
                                  <span>{formatDate(article.created_date)}</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <Tag className="h-4 w-4" />
                                  <span>Cat. {article.category_id}</span>
                                </div>
                                <div className="flex items-center gap-1">
                                  <FileText className="h-4 w-4" />
                                  <span>{article.words_count} mots</span>
                                </div>
                              </div>
                            </div>
                            <Badge variant="outline" className="ml-2">
                              Il y a {article.age_hours}h
                            </Badge>
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    Aucun article récent trouvé dans les dernières 48h
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
      {/* Footer */}
      <Footer />
    </div>
  );
}
