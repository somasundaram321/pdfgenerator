from flask import Flask, request, send_file
from pdfrw import PdfReader, PdfWriter, PdfDict
import tempfile
import os

app = Flask(__name__)

@app.post("/make-fillable")
def make_fillable():
    # Read incoming PDF
    file = request.files['pdf']
    temp_input = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_input.name)

    # Read PDF
    pdf = PdfReader(temp_input.name)
    page = pdf.pages[0]

    # Add editable fields
    def add_field(name, rect):
        field = PdfDict(
            FT="/Tx",
            T=name,
            V="",
            Subtype="/Widget",
            Rect=rect,
            DA="/Helv 12 Tf 0 g"
        )
        if not page.Annots:
            page.Annots = []
        page.Annots.append(field)

    # ADD FIELDS HERE (coordinates adjustable)
    add_field("NAME", [70, 700, 250, 725])
    add_field("AMOUNT", [300, 700, 500, 725])

    # Output PDF
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    PdfWriter().write(temp_output.name, pdf)

    return send_file(temp_output.name,
                     download_name="fillable.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
