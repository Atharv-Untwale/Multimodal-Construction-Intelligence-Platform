"""Gemini wrapper with graceful demo-mode fallback."""
from __future__ import annotations
import logging
from typing import Callable, Optional, Tuple

from PIL import Image, ImageOps

from core.config import MAX_IMAGE_EDGE
from core.demo_data import CHAT_DEFAULT, CHAT_KEYWORDS
from core.schemas import parse_json_text

log = logging.getLogger(__name__)


def prepare_image(file) -> Image.Image:
    """Open an uploaded file, fix orientation, convert to RGB and downscale."""
    img = Image.open(file)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((MAX_IMAGE_EDGE, MAX_IMAGE_EDGE))
    return img


class GeminiService:
    def __init__(self, api_key: Optional[str], model: str):
        self.api_key = (api_key or "").strip()
        self.model = model
        self._client = None
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as exc:  # SDK missing or bad key format
                log.warning("Gemini client init failed: %s", exc)
                self._client = None

    @property
    def demo_mode(self) -> bool:
        return self._client is None

    def analyze_image(self, prompt: str, image: Image.Image, normalizer: Callable[[dict], dict],
                      demo_payload: dict) -> Tuple[dict, str, Optional[str]]:
        """Returns (report, source, error). source is 'live' or 'demo'."""
        if self.demo_mode:
            return normalizer(demo_payload), "demo", None
        try:
            from google.genai import types
            resp = self._client.models.generate_content(
                model=self.model,
                contents=[prompt, image],
                config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2),
            )
            return normalizer(parse_json_text(resp.text)), "live", None
        except Exception as exc:
            log.exception("Gemini analysis failed")
            return normalizer(demo_payload), "demo", f"{type(exc).__name__}: {exc}"

    def chat(self, history: list, user_msg: str, system: str) -> Tuple[str, Optional[str]]:
        if self.demo_mode:
            return self._demo_reply(user_msg), None
        try:
            from google.genai import types
            contents = [
                types.Content(role="user" if m["role"] == "user" else "model",
                              parts=[types.Part.from_text(text=m["content"])])
                for m in history + [{"role": "user", "content": user_msg}]
            ]
            resp = self._client.models.generate_content(
                model=self.model, contents=contents,
                config=types.GenerateContentConfig(system_instruction=system, temperature=0.4),
            )
            return resp.text or "I couldn't generate a response.", None
        except Exception as exc:
            log.exception("Gemini chat failed")
            return self._demo_reply(user_msg), f"{type(exc).__name__}: {exc}"

    @staticmethod
    def _demo_reply(msg: str) -> str:
        low = msg.lower()
        for keys, reply in CHAT_KEYWORDS:
            if any(k in low for k in keys):
                return reply
        return CHAT_DEFAULT
