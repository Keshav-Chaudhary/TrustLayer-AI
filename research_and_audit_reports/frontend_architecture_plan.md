# Frontend Architecture Plan

## Frontend Stack
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **Data Fetching**: TanStack Query
- **State Management**: Zustand

## Constraints
- **NO** hardcoded hotel data.
- **NO** mock hotel objects or placeholder cards.
- **NO** fake metrics. All data API-driven.

## Page Architecture

### 1. Landing Page (`/`)
- **Purpose**: Brand introduction, trust establishment, and primary search gateway.
- **Data Sources**: Live metrics from `GET /metrics`.
- **Components**: `Hero`, `SearchBar`, `QuickActionChips`, `MetricCard`.
- **State**: Local form state for search input.
- **Loading/Error States**: Skeleton loaders for metrics; fallback static numbers on API failure.

### 2. Search Results Dashboard (`/search`)
- **Purpose**: Display filtered recommendations visually.
- **Data Sources**: `POST /recommend`.
- **Components**: `SidebarFilters`, `RecommendationCard`, `TrustBadge`, `AspectBars`.
- **State**: Zustand for global filter state (Budget, Area, Cleanliness).
- **Loading/Error States**: Grid of `CardSkeleton` during TanStack fetch. Toast notifications for API errors.

### 3. Hotel Analysis Page (`/hotel/[id]`)
- **Purpose**: Deep dive into trust scoring and specific evidence.
- **Data Sources**: `GET /hotel/{id}`.
- **Components**: `AspectScoreGrid`, `ReviewEvidenceSection`, `ProvenanceDrawer`.
- **State**: Zustand for expanded provenance UI state.
- **Loading/Error States**: Page-level skeleton. 404 page if ID is invalid.

### 4. Compare Hotels Page (`/compare`)
- **Purpose**: Side-by-side aspect score analysis.
- **Data Sources**: `POST /compare` (or combined client-side cache).
- **Components**: `ComparisonTable`.

### 5. Saved Hotels Page (`/saved`)
- **Purpose**: Bookmark management.
- **Data Sources**: LocalStorage + `POST /save`.
- **Components**: `SavedHotelList`.
