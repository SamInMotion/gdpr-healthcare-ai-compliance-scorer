import yaml
import re
from collections import defaultdict


class Article9Scorer:
    def __init__(self, rules_path="rules/article9.yaml", terms_path="rules/article9_terms.yaml"):
        # Load Article 9 rules
        with open(rules_path, "r", encoding="utf-8") as f:
            self.rules = yaml.safe_load(f)

        # Load EN → NO translation terms
        with open(terms_path, "r", encoding="utf-8") as f:
            self.terms = yaml.safe_load(f)

        self.max_score = self._calculate_max_score()

    def _calculate_max_score(self):
        """Calculate maximum possible score (all requirements counted)."""
        total = 0
        for category in self.rules["article_9_requirements"].values():
            for requirement in category:
                total += requirement["weight"]
        return total

    def _expand_keywords(self, keyword):
        """
        Expand a keyword with Norwegian equivalents from article9_terms.yaml.
        Always include the original keyword as well.
        """
        expanded = [keyword]
        for en, no in self.terms.items():
            if keyword.lower() == en.lower():
                expanded.append(no)
        return expanded

    def score_document(self, text):
        """Score document compliance with Article 9 (EN + NO)."""
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

                # Expand keywords with NO equivalents
                expanded_keywords = []
                for keyword_group in req["keywords"]:
                    expanded_group = []
                    for kw in keyword_group:
                        expanded_group.extend(self._expand_keywords(kw))
                    expanded_keywords.append(expanded_group)

                # Check for keywords using regex (EN + NO)
                for keyword_group in expanded_keywords:
                    for kw in keyword_group:
                        if re.search(rf"\b{re.escape(kw)}\b", text_lower, flags=re.IGNORECASE):
                            found = True
                            evidence.extend(self._extract_all_contexts(text, kw))
                            break
                    if found:
                        break

                # Check for evidence phrases if provided (also expand with NO)
                if "evidence_phrases" in req and not found:
                    for phrase in req["evidence_phrases"]:
                        for variant in self._expand_keywords(phrase):
                            if variant.lower() in text_lower:
                                found = True
                                evidence.extend(self._extract_all_contexts(text, variant))
                                break
                        if found:
                            break

                requirement_result = {
                    "id": req["id"],
                    "requirement": req["requirement"],
                    "category": req["category"],
                    "found": found,
                    "weight": req["weight"],
                    "conditional": req.get("conditional", False),
                    "evidence": evidence[:5],  # keep up to 5 snippets
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

    def _extract_all_contexts(self, text, keyword, context_chars=100):
        """Extract multiple snippets around a keyword."""
        snippets = []
        for match in re.finditer(re.escape(keyword), text, flags=re.IGNORECASE):
            start = max(0, match.start() - context_chars)
            end = min(len(text), match.end() + context_chars)
            snippets.append(f"...{text[start:end]}...")
        return snippets

    def _get_compliance_level(self, percentage):
        """Determine compliance level based on score."""
        if percentage >= 80:
            return "✅ High Compliance"
        elif percentage >= 60:
            return "⚠️ Moderate Compliance - Review Needed"
        elif percentage >= 40:
            return "⚠️ Low Compliance - Significant Gaps"
        else:
            return "❌ Non-Compliant - Major Issues"

