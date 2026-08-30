import { Progress } from "@/components/ui/progress";

export function AspectBars({ scores }: { scores: Record<string, number> }) {
  return (
    <div className="space-y-3">
      {Object.entries(scores).map(([aspect, score]) => (
        <div key={aspect} className="flex items-center justify-between gap-4">
          <span className="text-sm font-medium capitalize w-24 truncate">{aspect}</span>
          <div className="flex-1">
            <Progress value={(score / 5) * 100} className="h-2" />
          </div>
          <span className="text-xs text-muted-foreground font-mono">{score.toFixed(1)}/5</span>
        </div>
      ))}
    </div>
  );
}
