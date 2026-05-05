import re

def parse_llm_output(output: str) -> dict:
    """Utility to parse structured data from LLM if needed."""
    # Example logic to extract JSON blocks
    match = re.search(r'```json(.*?)```', output, re.DOTALL)
    if match:
        import json
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return {"text": output}
