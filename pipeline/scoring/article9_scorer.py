import yaml
import re
from collections import defaultdict

class Article9Scorer:
    def __init__(self, yaml_path="rules/article9_scorer.yaml"):
        with open(yaml_path, "r", encoding="utf-8") as f:
            self.rules = yaml.safe_load(f)
        self.max_score = self._calculate_max_score()

    def _calculate_max_score(self):
        """Calculate maximum possible score (all requirements counted)."""
        total = 0
        for category in self.rules["article_9_requirements"].values():
            for requirement in category:
                total += requirement["weight"]
        return total

    def _extract_all_contexts(self, text, keyword, window=50):
        """Extract all snippets around keyword matches."""
        contexts = []
        for match in re.finditer(rf"\b{re.escape(keyword)}\b", text, flags=re.IGNORECASE):
            start = max(match.start() - window, 0)
            end = min(match.end() + window, len(text))
            contexts.append(text[start:end].strip())
        return contexts

    def _get_compliance_level(self, percentage):
        """Return compliance level emoji + label."""
        if percentage == 100:
            return "✅ Fully Compliant"
        elif percentage >= 70:
            return "🟢 High Compliance - Minor Gaps"
        elif percentage >= 40:
            return "⚠️ Low Compliance - Significant Gaps"
        else:
            return "❌ Non-Compliant - Major Issues"

    def score_document(self, text):
        """Score document compliance with Article 9."""
        text_lower = text.lower()
        results = {
            "score": 0,
            "max_score": self.max_score,
            "percentage": 0,
            "passed": [],
            "failed": [],
            "warnings": [],
            "details": {},
            "category_scores": defaultdict(lambda: {"score": 0, "max": 0}),
        }

        for category_name, requirements in self.rules["article_9_requirements"].items():
            category_results = []

            for req in requirements:
                found = False
                evidence = []

                # Search keywords
                for keyword_group in req["keywords"]:
                    for kw in keyword_group:
                        if re.search(rf"\b{re.escape(kw)}\b", text_lower, flags=re.IGNORECASE):
                            found = True
                            evidence.extend(self._extract_all_contexts(text, kw))
                            break
                    if found:
                        break

                # Search evidence phrases
                if "evidence_phrases" in req and not found:
                    for phrase in req["evidence_phrases"]:
                        if phrase.lower() in text_lower:
                            found = True
                            evidence.extend(self._extract_all_contexts(text, phrase))
                            break

                requirement_result = {
                    "id": req["id"],
                    "requirement": req["requirement"],
                    "category": req["category"],
                    "found": found,
                    "weight": req["weight"],
                    "conditional": req.get("conditional", False),
                    "evidence": evidence[:5],  # limit to 5 snippets
                }

                # Update scoring
                results["category_scores"][category_name]["max"] += req["weight"]
                if found:
                    results["score"] += req["weight"]
                    results["passed"].append(req["id"])
                    results["category_scores"][category_name]["score"] += req["weight"]
                elif not req.get("conditional", False):
                    results["failed"].append(req["id"])
                    if req["weight"] >= 2:
                        results["warnings"].append(
                            f"⚠️ Critical: {req['category']} - {req['requirement']}"
                        )

                category_results.append(requirement_result)

            results["details"][category_name] = category_results

        results["percentage"] = round((results["score"] / self.max_score) * 100)
        results["compliance_level"] = self._get_compliance_level(results["percentage"])
        return results

