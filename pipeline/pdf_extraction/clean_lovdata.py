from bs4 import BeautifulSoup

def clean_lovdata_html(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Remove nav, footer, scripts, etc.
    for tag in soup(["nav", "header", "footer", "script", "style"]):
        tag.decompose()

    # Grab the main content (Lovdata usually wraps articles in <main> or <div id="document">)
    main_content = soup.find("main") or soup.find("div", id="document")

    if not main_content:
        raise ValueError("Could not find main GDPR content in Lovdata HTML")

    # Save cleaned HTML
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(main_content))

if __name__ == "__main__":
    clean_lovdata_html("test_docs/Lov om behandling av personopplysninger (personopplysningsloven) - - Lovdata.html", "rules/gdpr_no_clean.html")
    print("✅ Cleaned GDPR saved to rules/gdpr_no_clean.html")
