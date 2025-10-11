# GDPR Article 9 Compliance Checker

A tool for checking if healthcare AI documentation addresses GDPR Article 9 (special category data) requirements.

## What It Does

Scans your privacy policies, DPIAs, or compliance docs and shows:
- Which Article 9 requirements you've documented
- What's missing from your documentation  
- A compliance score to track improvements

Built this because manually checking 42 Article 9 requirements across multiple documents takes hours.

## Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run the web interface
streamlit run app.py

# Upload a PDF and get instant compliance analysis

```
Understanding Your Score
Article 9 has 10 different legal bases (exceptions) organizations can use. Most healthcare companies rely on 2-4 of these.
Typical scores:

Privacy policies: 10-25% (they mention special data but don't detail all legal bases)
DPIAs: 20-40% (more detailed, but focused on specific exceptions used)
Compliance docs: 30-50% (comprehensive coverage of relevant exceptions)

Low scores don't mean non-compliance. They mean your documentation focuses on the specific legal bases you actually use, rather than documenting all 10 possible exceptions.
What It Checks
Based on GDPR Article 9:

Prohibition: Are you processing special category data?
10 Legal Bases (a-j): Which exceptions apply to your processing?

Explicit consent
Employment law
Vital interests
Non-profit bodies
Public data
Legal claims
Public interest
Healthcare provision ← most common for medical AI
Public health
Research/archiving


Safeguards: Professional secrecy requirements
Member State Rules: Additional national restrictions

Limitations

Keyword-based detection: Doesn't understand context semantically
English only (for now): Norwegian support coming
Article 9 focus: Doesn't check other GDPR articles
Not legal advice: Use for gap analysis, not compliance certification

Example Output

```bash
Compliance Score: 7/42 (17%)

✅ Found: Healthcare provision exception (Article 9.2h)
✅ Found: Professional secrecy safeguards

⚠️ Missing: Explicit consent procedures
⚠️ Missing: Data retention policies
⚠️ Missing: International transfer mechanisms

```
Files
```bash
app.py                          # Streamlit web interface
pipeline/scoring/article9_scorer.py  # Core scoring logic
rules/article9.yaml             # Article 9 requirements
test_docs/                      # Sample documents to test
reports/                        # Generated compliance reports

```
Why I Built This
Every medical AI project I've worked on struggles with GDPR Article 9 compliance documentation. Manually checking requirements across multiple documents is both time-consuming and prone to errors. This tool automates the initial review, highlighting areas that require attention.
Contributing
Found a bug? Have suggestions for additional checks? Open an issue or PR.

License
MIT - Open Source.
