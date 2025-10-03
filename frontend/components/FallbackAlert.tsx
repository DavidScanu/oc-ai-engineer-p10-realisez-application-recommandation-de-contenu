'use client';

import { AlertTriangle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';

interface FallbackAlertProps {
  fallbackApplied: boolean;
  fallbackReason?: string | null;
  requestedMethod: string;
  actualMethod: string;
}

export function FallbackAlert({
  fallbackApplied,
  fallbackReason,
  requestedMethod,
  actualMethod
}: FallbackAlertProps) {
  if (!fallbackApplied) {
    return (
      <Card className="border-green-200 bg-green-50">
        <CardContent className="pt-6">
          <div className="flex items-center gap-2">
            <Badge variant="success">✓ Recommandation normale</Badge>
            <span className="text-sm text-green-700">
              Méthode <strong>{requestedMethod}</strong> utilisée avec succès
            </span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="border-yellow-200 bg-yellow-50">
      <CardContent className="pt-6">
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 text-yellow-600 mt-0.5" />
            <div className="flex-1 space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="warning">Fallback appliqué</Badge>
                <span className="text-sm text-yellow-700">
                  <strong>{requestedMethod}</strong> → <strong>{actualMethod}</strong>
                </span>
              </div>
              {fallbackReason && (
                <p className="text-sm text-yellow-700 bg-yellow-100 p-2 rounded">
                  {fallbackReason}
                </p>
              )}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
