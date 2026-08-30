import asyncio
from typing import List, Dict, Any
from scripts.rag.query_parser import QueryParser
from scripts.rag.retriever import HybridRetriever
from scripts.rag.context_builder import ContextBuilder
from app.services.context_compressor import ContextCompressor
from app.services.prompt_orchestrator import PromptOrchestrator
from app.services.llm_service import LLMService
from app.services.citation_injector import CitationInjector
from app.services.grounding_validator import GroundingValidator
import os

async def verify_pipeline():
    print("Initializing components...")
    parser = QueryParser()
    vector_dir = os.environ.get("VECTOR_STORE_PATH", "data/vector_store")
    retriever = HybridRetriever(vector_dir)
    compressor = ContextCompressor(max_tokens=1500)
    prompt_orchestrator = PromptOrchestrator()
    llm = LLMService()
    citation_injector = CitationInjector()
    validator = GroundingValidator()
    
    query = "family hotels in Delhi with good cleanliness"
    print(f"\n[1] Parsing query: '{query}'")
    constraints = parser.parse(query)
    print("Constraints:", constraints)
    
    print("\n[2] Retrieving...")
    chunks, fallback_level = retriever.retrieve(
        constraints.get("hard", {}).get("area", ""), 
        constraints.get("hard", {}), 
        constraints.get("soft", {}), 
        top_k=5
    )
    print(f"Retrieved {len(chunks)} chunks at fallback level {fallback_level}.")
    
    if not chunks:
        print("No chunks retrieved. Verification stopped.")
        return
        
    print("\n[3] Compressing context...")
    compressed = compressor.compress(chunks)
    print(f"Compressed down to {len(compressed)} chunks.")
    
    formatted_context = compressor.format_for_prompt(compressed)
    
    print("\n[4] Orchestrating Prompt...")
    prompt = prompt_orchestrator.get_prompt("search_summary", formatted_context, query)
    print("Prompt length:", len(prompt))
    
    print("\n[5] Generating from LLM...")
    try:
        raw_summary = llm.generate(prompt)
        print("Raw Summary:", raw_summary)
    except Exception as e:
        print(f"LLM Error: {e}")
        return
        
    print("\n[6] Injecting Citations...")
    text_w_citations, valid_citations = citation_injector.extract_and_verify_citations(raw_summary, chunks)
    print("Citations Found:", [c["chunk_id"] for c in valid_citations])
    
    print("\n[7] Validating Grounding...")
    hotel_name = chunks[0].get("metadata", {}).get("hotel_name", "Unknown Hotel")
    val_result = validator.validate_response(text_w_citations, chunks, hotel_name)
    
    print("\n=== FINAL RESULTS ===")
    print("Hotel Name:", hotel_name)
    print("Final Grounded Response:", val_result["remediated_text"])
    print("Passed Hallucination Check:", val_result["is_valid"])
    if not val_result["is_valid"]:
        print("Unsupported Claims:", val_result["unsupported_claims"])
        
if __name__ == "__main__":
    asyncio.run(verify_pipeline())
