'use client';

import { UserStats } from '@/lib/types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { BarChart3, FileCheck, UserCheck } from 'lucide-react';

interface UserStatsCardProps {
  stats: UserStats;
}

export function UserStatsCard({ stats }: UserStatsCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5 text-blue-600" />
            Statistiques utilisateur
          </span>
          {stats.is_new_user && (
            <Badge variant="warning">Nouvel utilisateur</Badge>
          )}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <UserCheck className="h-4 w-4" />
              <span>ID Utilisateur</span>
            </div>
            <p className="text-2xl font-bold">{stats.user_id}</p>
          </div>

          <div className="space-y-2">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <FileCheck className="h-4 w-4" />
              <span>Articles uniques lus</span>
            </div>
            <p className="text-2xl font-bold">{stats.unique_articles}</p>
          </div>

          <div className="space-y-2 col-span-2">
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <BarChart3 className="h-4 w-4" />
              <span>Total d&apos;interactions</span>
            </div>
            <p className="text-2xl font-bold">{stats.total_interactions}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
