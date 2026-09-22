"""Orchestrates running all 3 systems and generating terminal output PNG images."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont
from config import QUESTIONS
from chatbot import chatbot
from workflow import workflow
from agent import agent

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "Output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_terminal_image(title: str, lines: list[str], output_filename: str):
    """Render a modern dark-mode terminal window image with rounded corners and window controls."""
    # Measure dimensions
    padding = 25
    header_height = 45
    font_size = 14
    line_spacing = 6

    # Load monospace font or fallback
    font = None
    possible_fonts = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeMono.ttf"
    ]
    for font_path in possible_fonts:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, font_size)
                title_font = ImageFont.truetype(font_path, 15)
                break
            except Exception:
                pass
    if font is None:
        font = ImageFont.load_default()
        title_font = font

    # Calculate text width & height
    max_line_len = max([len(line) for line in lines] + [len(title)]) if lines else 40
    char_width = 8.5
    img_width = max(850, int(max_line_len * char_width + padding * 2))
    img_height = header_height + padding * 2 + len(lines) * (font_size + line_spacing) + 20

    img = Image.new("RGBA", (img_width, img_height), (15, 17, 23, 255))
    draw = ImageDraw.Draw(img)

    # Window Header (Mac / Linux Dark Terminal Bar)
    draw.rectangle([(0, 0), (img_width, header_height)], fill=(30, 34, 45, 255))
    
    # Terminal Window Buttons (Red, Yellow, Green)
    draw.ellipse([(15, 15), (27, 27)], fill=(255, 95, 86, 255))
    draw.ellipse([(35, 15), (47, 27)], fill=(255, 189, 46, 255))
    draw.ellipse([(55, 15), (67, 27)], fill=(255, 40, 34, 255))

    # Header Title
    draw.text((80, 14), title, font=title_font, fill=(180, 190, 210, 255))

    # Output lines rendering
    y = header_height + padding
    for line in lines:
        if line.startswith("==="):
            fill_color = (0, 210, 255, 255)  # Cyan for headers
        elif line.startswith("Q"):
            fill_color = (255, 200, 80, 255)  # Amber for questions
        elif line.startswith("A:") or line.startswith("Final Answer:"):
            fill_color = (120, 225, 140, 255)  # Green for answers
        elif line.startswith("   [Step"):
            fill_color = (180, 150, 255, 255)  # Purple for agent steps
        elif "Error" in line:
            fill_color = (255, 100, 100, 255)  # Red for errors
        elif line.startswith("---"):
            fill_color = (70, 80, 100, 255)  # Dim for separators
        else:
            fill_color = (220, 225, 235, 255)  # Soft white/grey for text

        draw.text((padding, y), line, font=font, fill=fill_color)
        y += font_size + line_spacing

    img_path = os.path.join(OUTPUT_DIR, output_filename)
    img.save(img_path)
    print(f"Saved terminal visual: {img_path}")

def run_and_record():
    print("Executing System 1: Plain Chatbot...")
    chatbot_lines = [
        "=== SYSTEM 1: PLAIN LLM CHATBOT (No Tools / No Private Data) ===",
        ""
    ]
    for idx, q in enumerate(QUESTIONS, 1):
        ans = chatbot(q)
        chatbot_lines.append(f"Q{idx}: {q}")
        for line in ans.split("\n"):
            chatbot_lines.append(f"A: {line}" if line == ans.split("\n")[0] else f"   {line}")
        chatbot_lines.append("-" * 70)
    
    render_terminal_image("System 1 - Plain LLM Chatbot Execution Output", chatbot_lines, "chatbot_output.png")

    print("Executing System 2: Rule-Based Workflow...")
    workflow_lines = [
        "=== SYSTEM 2: RULE-BASED WORKFLOW (Regex & Predefined Rules, No LLM) ===",
        ""
    ]
    for idx, q in enumerate(QUESTIONS, 1):
        ans = workflow(q)
        workflow_lines.append(f"Q{idx}: {q}")
        workflow_lines.append(f"A: {ans}")
        workflow_lines.append("-" * 70)
    
    render_terminal_image("System 2 - Rule-Based Workflow Execution Output", workflow_lines, "workflow_output.png")

    print("Executing System 3: AI Agent...")
    agent_lines = [
        "=== SYSTEM 3: AI AGENT (LLM + Tools + ReAct Loop) ===",
        ""
    ]
    for idx, q in enumerate(QUESTIONS, 1):
        agent_lines.append(f"Q{idx}: {q}")
        # Capture step trace by running agent with verbose output
        ans = agent(q, verbose=True)
        agent_lines.append(f"Final Answer: {ans}")
        agent_lines.append("-" * 70)
    
    render_terminal_image("System 3 - AI Agent Execution Output", agent_lines, "agent_output.png")

    # Render Comparison Summary Dashboard
    summary_lines = [
        "==========================================================================================",
        "                       DAY 1 PRACTICE TASK: COMPARISON SUMMARY                            ",
        "==========================================================================================",
        "Basis for Comparison  | Plain Chatbot         | Rule-Based Workflow  | AI Agent           ",
        "----------------------+-----------------------+----------------------+--------------------",
        "Flexibility           | High (Free text)      | Zero (Fixed rules)   | High (Adaptive)    ",
        "Decision-making       | Probabilistic (LLM)   | Deterministic        | LLM + Loop Reasoning",
        "Tool usage            | None                  | Static DB scripts    | Dynamic Tool Loop  ",
        "Private-data access   | None (Hallucinates)   | Hardcoded DB Lookup  | Dynamic via Tools  ",
        "Multi-step handling   | Poor (Prompt length)  | Hardcoded sequence   | Loop + Refinement  ",
        "Automation            | Conversational only   | Rigid execution      | Autonomous Tool Use",
        "Reliability           | Low on facts/math     | High on matched rules| High (Fact+Reason) ",
        "------------------------------------------------------------------------------------------",
        "SUITABILITY VERDICT: AI Agent is the clear winner for TechCorp's IT Asset Management",
        "scenario due to its ability to reason over multi-step queries, query private pricing,",
        "execute precise math via calculator tool, and adapt gracefully to creative prompts."
    ]
    render_terminal_image("Day 1 - Comparative Summary Matrix", summary_lines, "comparison_summary.png")

if __name__ == "__main__":
    run_and_record()
