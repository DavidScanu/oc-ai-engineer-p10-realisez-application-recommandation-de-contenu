'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { User, Loader2, Search } from 'lucide-react';
import type { ActiveUser } from '@/lib/types';

interface UserSelectorProps {
  onUserSelect: (userId: number) => void;
  selectedUserId?: number;
}

export function UserSelector({ onUserSelect, selectedUserId }: UserSelectorProps) {
  const [activeUsers, setActiveUsers] = useState<ActiveUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [manualUserId, setManualUserId] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const userList = await apiClient.getMostActiveUsers(20);
        setActiveUsers(userList);

        // Auto-select first user if none selected
        if (!selectedUserId && userList.length > 0) {
          onUserSelect(userList[0].user_id);
        }
      } catch (error) {
        console.error('Error fetching users:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const userId = parseInt(manualUserId);
    if (!isNaN(userId) && userId > 0) {
      onUserSelect(userId);
      setManualUserId('');
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <User className="h-5 w-5" />
          Sélection de l&apos;utilisateur
        </CardTitle>
        <CardDescription>
          Choisissez un utilisateur actif ou entrez un ID utilisateur
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {loading ? (
          <div className="flex items-center justify-center py-4">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : (
          <>
            <div className="space-y-2">
              <label className="text-sm font-medium">Top 20 utilisateurs actifs</label>
              <Select
                value={selectedUserId?.toString()}
                onValueChange={(value) => onUserSelect(parseInt(value))}
              >
                <SelectTrigger className="w-full bg-white">
                  <SelectValue placeholder="Sélectionnez un utilisateur" />
                </SelectTrigger>
                <SelectContent className="bg-white">
                  {activeUsers.map((user) => (
                    <SelectItem key={user.user_id} value={user.user_id.toString()}>
                      Utilisateur {user.user_id} ({user.total_clicks} clics, {user.unique_articles} articles)
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">Ou</span>
              </div>
            </div>

            <form onSubmit={handleManualSubmit} className="space-y-2">
              <label className="text-sm font-medium">Rechercher un utilisateur par ID</label>
              <div className="flex gap-2">
                <Input
                  type="number"
                  placeholder="ID utilisateur"
                  value={manualUserId}
                  onChange={(e) => setManualUserId(e.target.value)}
                  min="1"
                  className="flex-1"
                />
                <Button type="submit" size="icon">
                  <Search className="h-4 w-4" />
                </Button>
              </div>
            </form>
          </>
        )}
      </CardContent>
    </Card>
  );
}
