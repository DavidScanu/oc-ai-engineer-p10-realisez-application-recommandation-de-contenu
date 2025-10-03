'use client';

import { RecommendationMethod } from '@/lib/types';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Sparkles, Users, FileText, Layers } from 'lucide-react';

interface MethodSelectorProps {
  method: RecommendationMethod;
  onMethodChange: (method: RecommendationMethod) => void;
}

const methods: { value: RecommendationMethod; label: string; icon: React.ElementType; description: string; color: string }[] = [
  {
    value: 'hybrid',
    label: 'Hybride',
    icon: Layers,
    description: 'Combinaison intelligente de toutes les méthodes',
    color: 'text-purple-600'
  },
  {
    value: 'popularity',
    label: 'Popularité',
    icon: Sparkles,
    description: 'Articles tendances normalisés par âge',
    color: 'text-amber-600'
  },
  {
    value: 'content',
    label: 'Contenu',
    icon: FileText,
    description: 'Similarité basée sur les embeddings',
    color: 'text-blue-600'
  },
  {
    value: 'clustering',
    label: 'Clustering',
    icon: Users,
    description: 'Filtrage collaboratif par segments',
    color: 'text-green-600'
  },
];

export function MethodSelector({ method, onMethodChange }: MethodSelectorProps) {
  const currentMethod = methods.find((m) => m.value === method);

  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <h3 className="text-sm font-medium">Méthode de recommandation</h3>
        <Tabs value={method} onValueChange={(value) => onMethodChange(value as RecommendationMethod)}>
          <TabsList className="grid w-full grid-cols-4">
            {methods.map((m) => {
              const Icon = m.icon;
              return (
                <TabsTrigger key={m.value} value={m.value} className="flex items-center gap-1">
                  <Icon className={`h-4 w-4 ${m.color}`} />
                  <span className="hidden sm:inline">{m.label}</span>
                </TabsTrigger>
              );
            })}
          </TabsList>
        </Tabs>
      </div>

      {currentMethod && (
        <div className="rounded-lg bg-muted p-3">
          <p className="text-sm text-muted-foreground">
            <strong>{currentMethod.label}:</strong> {currentMethod.description}
          </p>
        </div>
      )}
    </div>
  );
}
