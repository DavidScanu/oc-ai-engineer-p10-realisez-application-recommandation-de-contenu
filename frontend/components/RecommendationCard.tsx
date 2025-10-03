'use client';

import { Recommendation } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FileText, Calendar, Tag } from 'lucide-react';

interface RecommendationCardProps {
  recommendation: Recommendation;
  rank: number;
}

export function RecommendationCard({ recommendation, rank }: RecommendationCardProps) {
  const { article_id, score, reason, metadata } = recommendation;

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      });
    } catch {
      return dateString;
    }
  };

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <Badge variant="secondary" className="text-xs">
                #{rank}
              </Badge>
              <CardTitle className="text-lg">Article {article_id}</CardTitle>
            </div>
            <div className="flex items-center gap-4 text-sm text-muted-foreground mt-2">
              <div className="flex items-center gap-1">
                <Tag className="h-4 w-4" />
                <span>Catégorie {metadata.category_id}</span>
              </div>
              <div className="flex items-center gap-1">
                <FileText className="h-4 w-4" />
                <span>{metadata.words_count} mots</span>
              </div>
              <div className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                <span>{formatDate(metadata.created_date)}</span>
              </div>
            </div>
          </div>
          <Badge variant="info" className="ml-2">
            Score: {score.toFixed(3)}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="bg-muted rounded-md">
          <p className="text-sm text-muted-foreground italic">{reason}</p>
        </div>
      </CardContent>
    </Card>
  );
}
