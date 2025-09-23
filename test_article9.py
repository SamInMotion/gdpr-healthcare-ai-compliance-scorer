from pipeline.scoring.article9_scorer import Article9Scorer

# Initialize scorer with both rules + dictionary
scorer = Article9Scorer(
    rules_path="rules/article9.yaml",
    terms_path="rules/article9_terms.yaml"
)

# Example Norwegian text
text_no = """
Denne behandlingen gjelder særlige kategorier av personopplysninger,
og krever uttrykkelig samtykke fra pasienten.
"""

results = scorer.score_document(text_no)

print("Score:", results['score'], "/", results['max_score'])
print("Percentage:", results['percentage'], "%")
print("Compliance level:", results['compliance_level'])
print("Passed:", results['passed'])
print("Failed:", results['failed'])
print("Evidence:", results['details'])
