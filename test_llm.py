"""Test LLM command parsing."""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.llm.llm_interface import LLMInterface

COMMANDS = [
    "turn on the LED",
    "turn off the light",
    "move forward",
    "follow the person",
    "move towards the bottle",
    "stop",
]

if __name__ == "__main__":
    llm = LLMInterface()
    for cmd in COMMANDS:
        result = llm.parse(cmd)
        print(f"  '{cmd}' → {result}")
