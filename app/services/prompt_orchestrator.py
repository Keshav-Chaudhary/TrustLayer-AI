from typing import Dict, Any

class PromptOrchestrator:
    """
    Manages task-specific prompts for different RAG requirements,
    ensuring consistent grounding instructions and citation format requirements.
    """
    
    def get_prompt(self, task: str, context: str, user_query: str = "") -> str:
        base_grounding_rules = (
            "CRITICAL RULES:\n"
            "1. You must ONLY use the provided context to answer the query.\n"
            "2. Do NOT hallucinate amenities, locations, or scores not found in the context.\n"
            "3. You MUST inject citations directly in your text using the exact [Chunk ID] provided in the context.\n"
        )
        
        professional_rules = (
            "PROFESSIONAL TONE RULES:\n"
            "- NEVER use phrases like: 'does not match the provided context', 'could potentially meet the criteria', 'likely offers', or 'not explicitly stated'.\n"
            "- If evidence is insufficient, output exactly: 'Limited review evidence is available to confidently assess this criterion.'\n"
        )
        
        prompts = {
            "search_summary": (
                f"{base_grounding_rules}\n"
                f"{professional_rules}\n"
                f"TASK: For each hotel provided in the context, write a brief (1-2 sentences) explanation of why it matches the query: '{user_query}'.\n"
                "OUTPUT FORMAT: You MUST return a single JSON object where keys are the hotel_ids and values are the explanations.\n"
                "Example:\n"
                '{"H123": {"match_reason": "This hotel is great for families [Chunk ID: X]."}, "H456": {"match_reason": "..."}}\n'
                "DO NOT return any text outside of the JSON object.\n"
                f"CONTEXT:\n{context}\n"
            ),
            "hotel_analysis": (
                f"{base_grounding_rules}\n"
                f"TASK: Provide a grounded deep analysis of this hotel. Focus on answering: '{user_query}' if provided, "
                "otherwise summarize its strengths and weaknesses.\n"
                f"CONTEXT:\n{context}\n"
            ),
            "comparison": (
                f"{base_grounding_rules}\n"
                f"TASK: Compare the provided hotels objectively based on the context. Ensure you explicitly compare EACH hotel provided in the context (do not merge or omit any). Write a very brief, concise comparison (under 3 sentences per hotel). Do NOT output headers for aspects, just write 2-3 short paragraphs comparing suitability, addressing every hotel by its exact name.\n"
                f"NEUTRALITY RULE: Do NOT declare any hotel as a 'winner', 'best', or 'champion', and do NOT use gaming-style comparison language. Focus objectively on the trade-offs and suitability for different traveler types.\n"
                f"CONTEXT:\n{context}\n"
            ),
            "chat": (
                f"{base_grounding_rules}\n"
                f"TASK: Answer the conversational query: '{user_query}'.\n"
                f"CONTEXT:\n{context}\n"
            )
        }
        
        return prompts.get(task, prompts["search_summary"])
