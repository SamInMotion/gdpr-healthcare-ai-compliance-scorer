import streamlit as st
import json
import os
from datetime import datetime
from pipeline.pdf_extraction.extract_pdf import extract_text_from_pdf
from pipeline.scoring.article9_scorer import Article9Scorer
from report_writer import ReportWriter
import logging

logging.basicConfig(level=logging.INFO)


def display_results(results):
    """Display scoring results in Streamlit"""

    # --- Score Overview ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Compliance Score",
            f"{results.get('score', 0)}/{results.get('max_score', 0)}",
            f"{results.get('percentage', 0)}%",
        )
    with col2:
        st.metric("Requirements Met", len(results.get("passed", [])))
    with col3:
        st.metric("Requirements Failed", len(results.get("failed", [])))

    # --- Compliance Level Badge ---
    compliance_level = results.get("compliance_level", "Unknown")
    st.markdown(f"### Compliance Level: **{compliance_level}**")

    # --- Progress Bar ---
    st.progress(results.get("percentage", 0) / 100)

    # --- Critical Warnings ---
    warnings = results.get("warnings", [])
    if warnings:
        st.error("### ⚠️ Critical Issues Found")
        for warning in warnings:
            st.warning(warning)

    # --- Detailed Breakdown ---
    with st.expander("Detailed Compliance Breakdown", expanded=False):
        details = results.get("details", {})
        if not details:
            st.info("No detailed results available.")
        else:
            for category, requirements in details.items():
                st.subheader(f"{category.replace('_', ' ').title()}")
                for req in requirements:
                    if req.get("found"):
                        st.success(f"✅ {req['category']}: {req['requirement']}")
                        if req.get("evidence"):
                            st.text("Evidence found:")
                            for evidence in req["evidence"]:
                                st.code(evidence, language="text")
                    else:
                        st.error(f"❌ {req['category']}: {req['requirement']}")

    # --- Actionable Recommendations ---
    st.markdown("### Priority Actions")
    priority_actions = []
    for req_id in results.get("failed", []):
        req = next(
            (r for cat in results.get("details", {}).values() for r in cat if r["id"] == req_id),
            None,
        )
        if req and req.get("weight", 1) >= 2:
            priority_actions.append(req)

    if not priority_actions:
        st.success("No high-priority issues found!")
    else:
        for i, action in enumerate(priority_actions[:5], 1):
            st.info(f"{i}. Add explicit mention of: **{action['category']}**")
            st.caption(f"Requirement: {action['requirement']}")

    # --- Export Results ---
    st.markdown("### Export Results")
    if st.button("Generate Compliance Report"):
        report = {
            "summary": {
                "score": results.get("score", 0),
                "max_score": results.get("max_score", 0),
                "percentage": results.get("percentage", 0),
                "compliance_level": results.get("compliance_level", "Unknown"),
            },
            "warnings": results.get("warnings", []),
            "details": results.get("details", {}),
            "priority_actions": [r["requirement"] for r in priority_actions],
        }

        json_data = json.dumps(report, indent=2)
        md_data = (
            f"# Compliance Report\n\n"
            f"**Score:** {report['summary']['score']}/{report['summary']['max_score']} "
            f"({report['summary']['percentage']}%)\n\n"
            f"**Compliance Level:** {report['summary']['compliance_level']}\n\n"
            f"## Priority Actions\n"
            + "".join([f"- {a}\n" for a in report["priority_actions"]])
        )

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="⬇️ Download JSON",
                data=json_data,
                file_name=f"article9_compliance_{datetime.now():%Y%m%d}.json",
                mime="application/json",
            )
        with col2:
            st.download_button(
                label="⬇️ Download Markdown",
                data=md_data,
                file_name=f"article9_compliance_{datetime.now():%Y%m%d}.md",
                mime="text/markdown",
            )


def score_document(path):
    """Extract text from document and run scoring"""
    text = extract_text_from_pdf(path)
    scorer = Article9Scorer("rules/article9.yaml")
    return scorer.score_document(text)


# --- Streamlit UI ---
st.title("GDPR Article 9 Compliance Scorer")

files = [f for f in os.listdir("test_docs") if f.endswith((".txt", ".pdf"))]
if not files:
    st.error("No test documents found in test_docs/. Please add some .txt or .pdf files.")
else:
    selected_file = st.selectbox("Choose a test document", files, key="test_doc_select")


# Option 1: Upload your own file
uploaded_file = st.file_uploader("Upload a PDF or TXT document", type=["pdf", "txt"])
if uploaded_file is not None:
    # Save uploaded file temporarily
    temp_path = os.path.join("test_docs", uploaded_file.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded file saved as: {uploaded_file.name}")
    path = temp_path
    st.info(f"Scoring uploaded file: {uploaded_file.name}")
    results = score_document(path)
    display_results(results)
else:
    # Option 2: Use existing test documents
    files = [f for f in os.listdir("test_docs") if f.endswith((".txt", ".pdf"))]
    if not files:
        st.error("No test documents found in test_docs/. Please add some .txt or .pdf files.")
    else:
        selected_file = st.selectbox("Choose a test document", files)
        if selected_file:
            st.info(f"Scoring: {selected_file}")
            path = os.path.join("test_docs", selected_file)
            results = score_document(path)
            display_results(results)

            # Generate reports using ReportWriter
            writer = ReportWriter()
            report_md_path = writer.to_markdown(results)
            report_json_path = writer.to_json(results)

            with open(report_md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
            with open(report_json_path, "r", encoding="utf-8") as f:
                json_content = f.read()

            st.download_button(
                label="⬇️ Download Markdown Report",
                data=md_content,
                file_name=os.path.basename(report_md_path),
                mime="text/markdown",
            )
            st.download_button(
                label="⬇️ Download JSON Report",
                data=json_content,
                file_name=os.path.basename(report_json_path),
                mime="application/json",
            )

