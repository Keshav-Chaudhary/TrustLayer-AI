# Frontend Requirements Audit

## Evaluation of Current Architecture Support
The frontend is NOT a chatbot. It must represent a fully-fledged AI-powered hotel recommendation platform emphasizing trust, evidence, and transparency.

### Supported Capabilities Needed:
- **Landing Page**: Needs live system metrics (must add `GET /metrics` backend route).
- **Search Experience**: Requires complex nested JSON payload for constraints (Area, Budget, etc.).
- **Recommendation Dashboard**: Needs robust list rendering, filtering, and sorting logic (requires frontend state management via Zustand and TanStack Query).
- **Hotel Analysis Page**: Requires a new `GET /hotel/{id}` route to fetch deep provenance and aspect data.
- **Compare Hotels**: Requires a `POST /compare` backend route or frontend client-side combination logic.
- **Saved Hotels**: Requires local storage or a backend `POST /save` route.
- **Trust Transparency & Evidence Exploration**: Requires rich UI components (progress bars, badges, collapsible drawers) populated dynamically from API provenance chunks.

## Conclusion
The deleted Streamlit app was insufficient for this complex, multi-page data exploration experience. The transition to Next.js 14 App Router with Tailwind and shadcn/ui is necessary to fulfill these architectural requirements natively without hacking a linear script format.
