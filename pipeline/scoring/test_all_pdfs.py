import os
from pipeline.pdf_extraction.extract_pdf import extract_text_from_pdf
from pipeline.scoring.article9_scorer import Article9Scorer

# Initialize the scorer
scorer = Article9Scorer(rules_path="rules/article9.yaml")

# Directory containing PDFs
pdf_dir = "test_docs/"

# Loop through all PDFs in the folder
for filename in os.listdir(pdf_dir):
    if filename.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        print(f"\n--- Scoring PDF: {filename} ---")

        # Extract text
        text = extract_text_from_pdf(pdf_path)

        # Score document
        results = scorer.score_document(text)

        # Print summary
        print(f"Score: {results['score']} / {results['max_score']}")
        print(f"Percentage: {results['percentage']}%")
        print(f"Compliance Level: {results['compliance_level']}")
        print(f"Passed requirements: {results['passed']}")
        print(f"Failed requirements: {results['failed']}")
        if results['warnings']:
            print("Warnings:")
            for warning in results['warnings']:
                print("  -", warning)
