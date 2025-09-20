import json
from datetime import datetime

class ReportWriter:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir

    def to_markdown(self, results, filename=None):
        """Generate a Markdown compliance report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename or f"report_{timestamp}.md"
        path = f"{self.output_dir}/{filename}"

        lines = []
        lines.append(f"# GDPR Article 9 Compliance Report\n")
        lines.append(f"**Generated:** {datetime.now().isoformat()}\n")
        lines.append(f"**Compliance Score:** {results['score']} / {results['max_score']} "
                     f"({results['percentage']}%)\n")
        lines.append(f"**Compliance Level:** {results['compliance_level']}\n")

        # Category overview
        lines.append("\n## Category Scores\n")
        for category, score_data in results.get("category_scores", {}).items():
            lines.append(f"- **{category}**: {score_data['score']} / {score_data['max']}")

        # Critical Warnings
        if results['warnings']:
            lines.append("\n## ⚠️ Critical Issues\n")
            for warning in results['warnings']:
                lines.append(f"- {warning}")

        # Detailed breakdown
        lines.append("\n## Detailed Breakdown\n")
        for category, requirements in results['details'].items():
            lines.append(f"### {category.replace('_', ' ').title()}")
            for req in requirements:
                status = "✅ PASSED" if req['found'] else "❌ FAILED"
                lines.append(f"- **[{req['id']}] {req['requirement']}** ({req['weight']} pts) → {status}")
                if req['evidence']:
                    for ev in req['evidence']:
                        lines.append(f"    - Evidence: {ev}")

        report_md = "\n".join(lines)

        # Save file
        with open(path, "w", encoding="utf-8") as f:
            f.write(report_md)

        return path

    def to_json(self, results, filename=None):
        """Save results as JSON report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = filename or f"report_{timestamp}.json"
        path = f"{self.output_dir}/{filename}"

        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        return path
