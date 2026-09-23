"""Tool functions and OpenAI function calling definitions for Apex Logistics."""
from config import CUSTOMS_TARIFF_DATABASE, PORT_CONGESTION_DATABASE

def get_customs_tariff_rate(country_code: str, hs_code: str) -> dict:
    """Retrieves private customs duty tariff rate for a given country and HS Code."""
    key = (country_code.upper().strip(), hs_code.strip())
    if key in CUSTOMS_TARIFF_DATABASE:
        data = CUSTOMS_TARIFF_DATABASE[key]
        return {
            "status": "success",
            "country_code": key[0],
            "hs_code": key[1],
            "description": data["description"],
            "duty_rate_percent": data["duty_rate"] * 100,
            "vat_rate_percent": data["vat_rate"] * 100
        }
    return {
        "status": "error",
        "message": f"No tariff data found for country '{country_code}' and HS code '{hs_code}'."
    }

def get_port_congestion_delay(port_code: str) -> dict:
    """Retrieves real-time port congestion status and delay in days for a given port code."""
    code = port_code.upper().strip()
    if code in PORT_CONGESTION_DATABASE:
        data = PORT_CONGESTION_DATABASE[code]
        return {
            "status": "success",
            "port_code": code,
            "port_name": data["port_name"],
            "delay_days": data["delay_days"],
            "congestion_status": data["status"]
        }
    return {
        "status": "error",
        "message": f"Port code '{port_code}' not found in global logistics database."
    }

def calculate_duty_and_total(item_count: int, unit_price: float, duty_rate_percent: float) -> dict:
    """Calculates customs duty payable and total cost including duty."""
    total_declared_value = item_count * unit_price
    duty_amount = total_declared_value * (duty_rate_percent / 100.0)
    total_landed_cost = total_declared_value + duty_amount
    return {
        "status": "success",
        "item_count": item_count,
        "unit_price": unit_price,
        "total_declared_value": total_declared_value,
        "duty_rate_percent": duty_rate_percent,
        "duty_amount_payable": round(duty_amount, 2),
        "total_landed_cost": round(total_landed_cost, 2)
    }

TOOL_FUNCTIONS = {
    "get_customs_tariff_rate": get_customs_tariff_rate,
    "get_port_congestion_delay": get_port_congestion_delay,
    "calculate_duty_and_total": calculate_duty_and_total,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_customs_tariff_rate",
            "description": "Lookup official customs import duty tariff rate for a target country (e.g. BR, IN) and Harmonized System (HS) commodity code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "country_code": {"type": "string", "description": "2-letter ISO country code, e.g. 'BR', 'IN'"},
                    "hs_code": {"type": "string", "description": "HS commodity tariff code, e.g. '8517.62', '8471.50'"}
                },
                "required": ["country_code", "hs_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_port_congestion_delay",
            "description": "Get real-time port congestion level and estimated vessel delay in days by 3-letter UN/LOCODE port code (e.g. 'SSZ', 'BOM', 'RTM').",
            "parameters": {
                "type": "object",
                "properties": {
                    "port_code": {"type": "string", "description": "3-letter port code, e.g. 'SSZ', 'BOM'"}
                },
                "required": ["port_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_duty_and_total",
            "description": "Calculate duty payable amount and landed total cost based on quantity, unit price, and duty percentage.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_count": {"type": "integer", "description": "Number of items"},
                    "unit_price": {"type": "number", "description": "Price per item in USD"},
                    "duty_rate_percent": {"type": "number", "description": "Customs duty percentage (e.g. 18 for 18%)"}
                },
                "required": ["item_count", "unit_price", "duty_rate_percent"]
            }
        }
    }
]
