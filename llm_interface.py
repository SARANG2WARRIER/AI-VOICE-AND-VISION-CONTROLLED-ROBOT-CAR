"""
LLMInterface – converts natural language into structured robot command JSON
using Groq (LLaMA 3.1 8B Instant).
"""

import json
import re

from groq import Groq

from config.settings import GROQ_API_KEY, GROQ_MODEL, GROQ_MAX_TOKENS, GROQ_TEMPERATURE

SYSTEM_PROMPT = """You are a robot command parser.
Convert the user's voice command into a JSON object with this exact structure:
{"action": "<ACTION>", "target": "<TARGET>"}

Allowed actions: LED_ON, LED_OFF, MOVE_FORWARD, MOVE_BACKWARD, TURN_LEFT, TURN_RIGHT, STOP, MOVE_TOWARDS, FOLLOW
- target is only required for MOVE_TOWARDS and FOLLOW (e.g. "person", "bottle", "chair")
- For all other actions, omit the target field entirely.
- Respond with JSON only. No explanation. No markdown.
"""


class LLMInterface:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

    # ── Public API ────────────────────────────────────────────────────────────

    def parse(self, text: str) -> dict:
        """
        Convert natural language text to a command dict.
        Returns e.g. {"action": "LED_ON"} or {"action": "FOLLOW", "target": "person"}
        Returns {} on failure.
        """
        if not text:
            return {}

        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=GROQ_MAX_TOKENS,
            temperature=GROQ_TEMPERATURE,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": text},
            ],
        )

        raw = response.choices[0].message.content.strip()
        return self._safe_parse(raw)

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _safe_parse(raw: str) -> dict:
        """Strip markdown fences and parse JSON safely."""
        clean = re.sub(r"```(?:json)?|```", "", raw).strip()
        try:
            return json.loads(clean)
        except json.JSONDecodeError:
            print(f"[LLM] Failed to parse: {raw}")
            return {}
