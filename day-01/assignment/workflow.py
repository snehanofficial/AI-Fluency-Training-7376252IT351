"""System 2: A rule-based workflow. Predefined if/else rules & regex, no LLM at all."""
import re
from config import IT_ASSET_PRICING, QUESTIONS

def workflow(question: str) -> str:
    text = question.upper()
    
    # 1. Match asset keys in text
    found_assets = [key for key in IT_ASSET_PRICING.keys() if key in text]
    
    # Simple single asset price query rule
    if "ANNUAL COST" in text or "PRICE" in text or "COST OF" in text:
        if len(found_assets) == 1:
            asset = found_assets[0]
            price = IT_ASSET_PRICING[asset]
            return f"The annual cost of {asset} is ${price:,}."
    
    # Total calculation rule with discount support
    if "TOTAL" in text and "COST" in text:
        # Extract quantities and assets using regex, e.g. "5 FIGMA_ENTERPRISE"
        matches = re.findall(r"(\d+)\s+([A-Z0-9_]+)", text)
        total = 0.0
        details = []
        for qty_str, asset in matches:
            if asset in IT_ASSET_PRICING:
                qty = int(qty_str)
                price = IT_ASSET_PRICING[asset]
                subtotal = qty * price
                total += subtotal
                details.append(f"{qty}x {asset} (${subtotal})")
        
        if details:
            # Check for discount percentage
            discount_match = re.search(r"(\d+)\%\s*(?:CORPORATE\s*)?DISCOUNT", text)
            if discount_match:
                discount_pct = float(discount_match.group(1))
                total = total * (1.0 - discount_pct / 100.0)
                return f"Total annual IT licensing cost ({', '.join(details)}) after {discount_pct:.0f}% discount: ${total:,.2f}"
            return f"Total annual IT licensing cost ({', '.join(details)}): ${total:,.2f}"

    # Price comparison rule
    if "MORE EXPENSIVE" in text or "PRICE DIFFERENCE" in text:
        if len(found_assets) == 2:
            a1, a2 = found_assets[0], found_assets[1]
            p1, p2 = IT_ASSET_PRICING[a1], IT_ASSET_PRICING[a2]
            diff = abs(p1 - p2)
            higher = a1 if p1 > p2 else a2
            return f"{higher} is more expensive by ${diff:,}. ({a1}: ${p1:,}, {a2}: ${p2:,})"

    # Static fallback for unsupported rules
    return "Error: Request does not match any predefined rule pattern in the workflow engine."

if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (No LLM) ===\n")
    for idx, question in enumerate(QUESTIONS, 1):
        print(f"Q{idx}: {question}")
        print("A:", workflow(question))
        print("-" * 75)
