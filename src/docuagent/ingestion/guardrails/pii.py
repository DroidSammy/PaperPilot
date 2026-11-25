from langchain_core.documents import Document
from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer.nlp_engine import NlpEngineProvider 


from docuagent.core.logger import logger

ENTITIES = ["EMAIL_ADDRESS", "PHONE_NUMBER", "IN_PHONE", "IN_AADHAAR",
            "IN_PAN", "CREDIT_CARD", "IBAN_CODE", "IP_ADDRESS"]


class PIIRedactor:
    def __init__(self, min_score: float = 0.5, entities: list[str] | None = None):
        self.min_score = min_score
        self.entities = entities or ENTITIES
        provider = NlpEngineProvider(nlp_configuration={
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
        })
        self.analyzer = AnalyzerEngine(
            nlp_engine=provider.create_engine(),
            supported_languages=["en"],
        )   # replaces: self.analyzer = AnalyzerEngine()

        self._add_indian_recognizers()
        self.anonymizer = AnonymizerEngine()
        self.operators = {
            e: OperatorConfig("replace", {"new_value": f"<{e}>"}) for e in self.entities
        }

    def _add_indian_recognizers(self):
        for name, regex, score in [
            ("IN_AADHAAR", r"\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b", 0.6),
            ("IN_PAN", r"\b[A-Z]{5}\d{4}[A-Z]\b", 0.8),
            ("IN_PHONE", r"\b(?:\+91[\s-]?)?[6-9]\d{9}\b", 0.5),
        ]:
            self.analyzer.registry.add_recognizer(
                PatternRecognizer(supported_entity=name,
                                  patterns=[Pattern(name.lower(), regex, score)])
            )

    def redact_text(self, text: str) -> tuple[str, dict[str, int]]:
        findings = [
            f for f in self.analyzer.analyze(text=text, entities=self.entities, language="en")
            if f.score >= self.min_score
        ]
        if not findings:
            return text, {}
        out = self.anonymizer.anonymize(
            text=text, analyzer_results=findings, operators=self.operators
        )
        counts: dict[str, int] = {}
        for f in findings:
            counts[f.entity_type] = counts.get(f.entity_type, 0) + 1
        return out.text, counts

    def __call__(self, docs: list[Document]) -> list[Document]:
        cleaned, total = [], {}
        for d in docs:
            text, counts = self.redact_text(d.page_content)
            for k, v in counts.items():
                total[k] = total.get(k, 0) + v
            # copy, don't mutate the originals
            cleaned.append(Document(
                page_content=text,
                metadata={**d.metadata, "pii_redacted": bool(counts)},
            ))
        logger.info(f"PII redaction complete: {total or 'nothing found'}")  # counts only
        return cleaned