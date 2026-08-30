import { Badge } from "@/components/ui/badge";

export function TrustBadge({ score }: { score: number }) {
  const getVariant = () => {
    if (score >= 80) return "success";
    if (score >= 60) return "warning";
    return "destructive";
  };
  
  return (
    <div className="flex flex-col gap-1 items-end">
      <span className="text-xs text-muted-foreground">Trust Score</span>
      <Badge variant={getVariant()} className="text-sm px-3 py-1">
        {score.toFixed(1)}
      </Badge>
    </div>
  );
}

export function ConfidenceBadge({ level }: { level: string }) {
  const variantMap: Record<string, "success" | "warning" | "destructive"> = {
    High: "success",
    Medium: "warning",
    Low: "destructive"
  };
  
  return (
    <Badge variant={variantMap[level] || "default"}>
      {level} Confidence
    </Badge>
  );
}
