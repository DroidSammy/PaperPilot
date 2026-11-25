import re
from typing import Literal

from langchain_core.documents import Document

from docuagent.core.logger import logger

# Heuristic patterns. Extend them as you find real cases in your own documents.
PATTERNS = [
    r"ignore (all |any )?(the )?(previous|prior|above|earlier) (instructions|prompts?|rules)",
    r"disregard (all |any )?(the )?(previous|prior|above|system) (instructions|prompts?)",
    r"forget (everything|all|your) (instructions|rules|above)",
    r"you are now\b",
    r"act as (an? )?(?!expected)\w+",
    r"(reveal|print|show|repeat) (your |the )?(system )?(prompt|instructions)",
    r"new instructions?\s*:",
    r"\bsystem\s*:\s",
    r"</?(context|system|assistant|instructions?)>",   # tries to break your delimiters
    r"do not (tell|inform) the user",
]
_REGEX = re.compile("|".join(f"(?:{p})" for p in PATTERNS), re.IGNORECASE)

Mode = Literal["flag", "strip", "reject"]


class InjectionScanner:
    def __init__(self, mode: Mode = "strip"):
        self.mode = mode

    def scan_text(self, text: str) -> tuple[str, int]:
        """Return (possibly cleaned text, number of suspicious lines)."""
        lines, hits, out = text.split("\n"), 0, []
        for line in lines:
            if _REGEX.search(line):
                hits += 1
                if self.mode == "strip":
                    continue          # drop the whole line
            out.append(line)
        return "\n".join(out), hits

    def __call__(self, docs: list[Document]) -> list[Document]:
        result, flagged = [], 0
        for d in docs:
            text, hits = self.scan_text(d.page_content)
            if hits:
                flagged += 1
                logger.warning(
                    f"Possible prompt injection ({hits} line(s)) in "
                    f"{d.metadata.get('source')} p{d.metadata.get('page')}"
                )
                if self.mode == "reject":
                    continue
            result.append(Document(
                page_content=text if self.mode == "strip" else d.page_content,
                metadata={**d.metadata, "injection_suspected": hits > 0},
            ))
        logger.info(f"Injection scan: {flagged} suspicious page(s) of {len(docs)}")
        return result