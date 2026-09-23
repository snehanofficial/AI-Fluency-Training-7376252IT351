"""Shared configuration for Day 02 assignment.
Apex Logistics & Customs Compliance Advisory scenario.
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()
MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

if PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
else:
    raise SystemExit(f"Unsupported PROVIDER '{PROVIDER}'. Use groq.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Private Customs Tariff Database & Real-Time Logistics Data (Unknown to LLM pre-training)
CUSTOMS_TARIFF_DATABASE = {
    ("BR", "8517.62"): {"description": "Industrial Telecom Switches", "duty_rate": 0.18, "vat_rate": 0.10}, # 18% import duty
    ("IN", "8471.50"): {"description": "Enterprise Server Units", "duty_rate": 0.12, "vat_rate": 0.18},     # 12% import duty
    ("DE", "8471.30"): {"description": "Portable Laptops", "duty_rate": 0.03, "vat_rate": 0.19},            # 3% import duty
    ("JP", "8504.40"): {"description": "Static Converters & Inverters", "duty_rate": 0.05, "vat_rate": 0.10}, # 5% import duty
}

PORT_CONGESTION_DATABASE = {
    "SSZ": {"port_name": "Port of Santos, Brazil", "delay_days": 6, "status": "Heavy Congestion"},
    "BOM": {"port_name": "Jawaharlal Nehru Port (Nhava Sheva), India", "delay_days": 2, "status": "Moderate Congestion"},
    "RTM": {"port_name": "Port of Rotterdam, Netherlands", "delay_days": 1, "status": "Normal Operations"},
    "LAX": {"port_name": "Port of Los Angeles, USA", "delay_days": 5, "status": "Heavy Congestion"},
}

QUESTIONS = [
    {
        "id": "Q1",
        "type": "Tool-Dependent Fact & Math",
        "text": "What is the total import duty payable for importing 150 units of Industrial Telecom Switches (HS Code 8517.62) valued at $1,200 per unit into Brazil (BR)?"
    },
    {
        "id": "Q2",
        "type": "Multi-Step Math & Capacity Reasoning",
        "text": "A cargo container carries 3 box types: Box Alpha (25 kg, $60 value), Box Beta (15 kg, $90 value), and Box Gamma (10 kg, $40 value). If loaded with 30 Alpha, 40 Beta, and 50 Gamma, and max container payload is 2,000 kg, is the cargo within payload limit, and what is the exact average value per kg of the loaded cargo?"
    },
    {
        "id": "Q3",
        "type": "Constraint Satisfaction & Deductive Logic",
        "text": "Shipping Route A takes 6 days with 95% reliability. Route B takes 3 days with 70% reliability. Route C takes 4 days with 85% reliability. If a shipper requires a minimum reliability threshold of 80% and prioritizes shortest shipping time as the tie-breaker, which route should be selected and why?"
    },
    {
        "id": "Q4",
        "type": "Direct Creative / General Knowledge",
        "text": "Draft a 2-sentence formal shipment dispatch notification for Container ID #APX-8849 bound for Rotterdam."
    },
    {
        "id": "Q5",
        "type": "Complex Multi-Tool + Multi-Step Reasoning",
        "text": "We plan to export 50 Enterprise Server Units (HS Code 8471.50, $3,000 each) to India (IN) via Port of Santos (SSZ). What is the total estimated transit delay including Santos port congestion, and total customs tariff duty?"
    }
]

def banner(title: str):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")
