"""Shared configuration: chooses the LLM provider and holds private IT asset data."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "ollama":
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
elif PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
elif PROVIDER == "huggingface":
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")
else:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use ollama, groq or huggingface.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Private TechCorp Corporate IT Asset & License Pricing Data (USD)
# Data unknown to public LLM pre-training
IT_ASSET_PRICING = {
    "FIGMA_ENTERPRISE": 540,          # $540 per user / year
    "VS_CODE_ENTERPRISE": 1200,       # $1,200 per user / year
    "MACBOOK_PRO_M3": 2400,           # $2,400 per laptop unit
    "DELL_XPS_15": 1800,              # $1,800 per laptop unit
    "JIRA_ENTERPRISE": 450,           # $450 per user / year
    "SLACK_ENTERPRISE": 240,          # $240 per user / year
}

QUESTIONS = [
    "What is the annual cost of a FIGMA_ENTERPRISE license?",
    "What is the total annual IT licensing cost for 5 FIGMA_ENTERPRISE licenses and 3 VS_CODE_ENTERPRISE licenses after a 15% corporate discount?",
    "Is MACBOOK_PRO_M3 more expensive than DELL_XPS_15, and what is the price difference?",
    "Write a two-line welcome message for a new Software Engineer joining TechCorp.",
    "Which software licenses can we purchase within a total budget of $1000?",
]

def banner(system_name):
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n")
