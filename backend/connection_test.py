"""
backend/connection_test.py  -  Role 1: AI Lead

Quick connection test for Foundry / LLM provider.
Run this FIRST after setting up .env to confirm the API works.

Usage:
  cd backend
  python connection_test.py
"""
import os, json

try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ .env loaded")
except ImportError:
    print("  (dotenv not installed, reading from environment)")

provider = os.getenv("LLM_PROVIDER", "azure").lower()
print(f"  Provider  : {provider}")

if provider == "azure":
    endpoint   = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
    key        = os.getenv("AZURE_OPENAI_KEY", "")
    print(f"  Endpoint  : {endpoint or '(not set)'}")
    print(f"  Deployment: {deployment or '(not set)'}")
    print(f"  Key       : {'(set)' if key else '(not set – will use keyless auth)'}")
    if not endpoint:
        print("\n✗ AZURE_OPENAI_ENDPOINT is missing in .env")
        exit(1)
    if not deployment:
        print("\n✗ AZURE_OPENAI_DEPLOYMENT is missing in .env")
        exit(1)

print("\nSending a test message to the LLM...")

try:
    import ai
    # Use a short, safe test message
    test_story = "I need a 5 day fee extension. I have my sanction letter."
    result = ai.call_llm(test_story, strict=False)
    print("✓ Got a response from the LLM")
    print(f"  Raw response (first 200 chars): {result[:200]!r}")

    import json
    try:
        parsed = json.loads(result)
        ok, reason = ai._validate(parsed)
        if ok:
            print("✓ Response is valid JSON matching our schema")
        else:
            print(f"  Response parsed but failed validation: {reason}")
    except json.JSONDecodeError:
        print("  Response is not JSON – the model may need json_object mode")

    print("\n✓ Connection test PASSED – your LLM provider is working")

except Exception as e:
    print(f"\n✗ Connection test FAILED: {e}")
    print("\nCommon fixes:")
    print("  - Wrong endpoint: copy from Foundry portal > project > Overview")
    print("  - Wrong deployment name: use the deployment name, not the model name")
    print("  - Key not set: add AZURE_OPENAI_KEY=... to .env, or run  az login")
    print("  - Package missing: pip install -r requirements.txt")
    exit(1)
