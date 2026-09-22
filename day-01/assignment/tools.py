"""Tools available to the AI Agent, including AST-safe evaluation and JSON Schema definitions."""
import ast
import operator
import json
from config import IT_ASSET_PRICING

def get_asset_price(asset_name: str) -> str:
    """Look up the private cost/pricing for a TechCorp IT asset or license."""
    clean_key = asset_name.strip().upper().replace(" ", "_")
    price = IT_ASSET_PRICING.get(clean_key)
    if price is not None:
        return json.dumps({"asset": clean_key, "price_usd": price})
    return json.dumps({"error": f"Unknown asset '{asset_name}'. Available assets: {list(IT_ASSET_PRICING.keys())}"})

def list_all_assets() -> str:
    """List all available TechCorp IT assets and their pricing."""
    return json.dumps(IT_ASSET_PRICING)

# Safe AST-based calculator: only numbers and + - * / ( ) are allowed.
_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.USub: operator.neg
}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression or operation")

def calculator(expression: str) -> str:
    """Evaluate a mathematical expression safely (e.g. '(5 * 540 + 3 * 1200) * 0.85')."""
    try:
        val = _evaluate(ast.parse(expression, mode="eval").body)
        return str(val)
    except Exception as err:
        return f"Calculator Error: {err}"

TOOL_FUNCTIONS = {
    "get_asset_price": get_asset_price,
    "list_all_assets": list_all_assets,
    "calculator": calculator,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_asset_price",
            "description": "Look up private corporate pricing for a specific TechCorp IT hardware asset or software license.",
            "parameters": {
                "type": "object",
                "properties": {
                    "asset_name": {
                        "type": "string",
                        "description": "Name or key of the asset (e.g. FIGMA_ENTERPRISE, MACBOOK_PRO_M3)"
                    }
                },
                "required": ["asset_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_all_assets",
            "description": "List all TechCorp IT assets and software licenses along with their pricing.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Safely calculate mathematical or financial expressions using standard operators (+, -, *, /).",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression string, e.g. '(5 * 540 + 3 * 1200) * 0.85'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

if __name__ == "__main__":
    print("get_asset_price('FIGMA_ENTERPRISE') ->", get_asset_price("FIGMA_ENTERPRISE"))
    print("list_all_assets() ->", list_all_assets())
    print("calculator('(5 * 540 + 3 * 1200) * 0.85') ->", calculator("(5 * 540 + 3 * 1200) * 0.85"))
