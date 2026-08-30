def test_grounding_validator():
    from app.services.grounding_validator import GroundingValidator
    validator = GroundingValidator()
    
    response_text = "Hotel Awesome has a great pool and free wifi."
    provenance = [{"snippet": "The pool is huge."}]
    
    result = validator.validate_response(response_text, provenance, "Hotel Awesome")
    assert result["is_valid"] is False
    assert len(result["unsupported_claims"]) > 0
