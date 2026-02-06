from weasyprint import HTML
import pathlib
from datetime import datetime

root_path = pathlib.Path(__file__).parent.parent.parent

def write_pdf(html: str):
    """
    Write HTML to a PDF file.
    All research must be saved as a PDF file.
    titles and section headers must be formatted with proper styling.
    and formatted professionally with proper citations and references.
    """
    print("writing pdf...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = root_path / "output"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"output_{timestamp}.pdf"
    HTML(string=html).write_pdf(output_path)
    print("pdf written successfully")
    