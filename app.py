from flask import (
    Flask,
    render_template,
    request,
    send_file
)

import os

from services.fipe_service import process_spreadsheet

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    """
    Render home page.
    """

    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    """
    Upload spreadsheet,
    process FIPE data,
    and return generated file.
    """

    if "file" not in request.files:

        return {
            "error": "No file uploaded"
        }, 400

    uploaded_file = request.files["file"]

    if uploaded_file.filename == "":

        return {
            "error": "Invalid file"
        }, 400

    input_file_path = os.path.join(
        UPLOAD_FOLDER,
        uploaded_file.filename
    )

    uploaded_file.save(input_file_path)

    output_file_path = os.path.join(
        OUTPUT_FOLDER,
        "fipe_result.xlsx"
    )

    process_spreadsheet(
        input_file_path,
        output_file_path
    )

    return send_file(
        output_file_path,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(debug=True)
