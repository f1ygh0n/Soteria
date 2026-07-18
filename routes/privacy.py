import fitz
import os
import tempfile

from docx import Document
from flask import Blueprint, render_template, request

from utils.privacy_rules import analyze_text
from ai.privacy_ai import analyze_privacy
from database.database import save_history

privacy_bp = Blueprint("privacy", __name__)

SUPPORTED_EXTENSIONS = {

    ".txt",
    ".py",
    ".js",
    ".json",
    ".csv",
    ".html",
    ".css",
    ".md",
    ".env",
    ".xml",
    ".yaml",
    ".yml",
    ".ini",
    ".pdf",
    ".docx"

}

def extract_pdf_text(filepath):

    document = fitz.open(filepath)

    text = ""

    for page in document:

        text += page.get_text()

    document.close()

    return text

def extract_docx_text(filepath):

    document = Document(filepath)

    text = ""

    for paragraph in document.paragraphs:

        text += paragraph.text + "\n"

    return text

@privacy_bp.route("/privacy", methods=["GET", "POST"])
def privacy():

    result = None

    if request.method == "POST":

        text = request.form.get("text", "").strip()

        uploaded_file = request.files.get("file")   

        if uploaded_file and uploaded_file.filename:

            filename = uploaded_file.filename.lower()

            extension = "." + filename.rsplit(".", 1)[-1]

            if extension in SUPPORTED_EXTENSIONS:

                try:

                    if extension == ".pdf":

                        with tempfile.NamedTemporaryFile(
                            suffix=".pdf",
                            delete=False
                        ) as temp:

                            uploaded_file.save(temp.name)

                            text = extract_pdf_text(temp.name)

                        os.remove(temp.name)

                    elif extension == ".docx":

                        with tempfile.NamedTemporaryFile(
                            suffix=".docx",
                            delete=False
                        ) as temp:

                            uploaded_file.save(temp.name)

                            text = extract_docx_text(temp.name)

                        os.remove(temp.name)

                    else:

                        text = uploaded_file.read().decode(
                            "utf-8",
                            errors="ignore"
                        )

                except Exception:

                    text = ""

            else:

                result = {

                    "score": 0,

                    "verdict": "Unsupported File",

                    "summary": (
                        "This file type is not currently supported."
                    ),

                    "findings": []

                }

        if result is None:

            if text:

                result = analyze_text(text)

                result["ai"] = analyze_privacy(result["ai_input"])

            else:

                result = {

                    "score": 100,

                    "verdict": "No Input",

                    "summary": (
                        "Please upload a supported file or paste some text."
                    ),

                    "findings": []

                }

    if result:

        save_history(

            module="Privacy Scanner",

            score=result["score"],

            verdict=result["verdict"],

            summary=result["summary"]

        )

    return render_template(

        "privacy.html",

        page_title="Privacy Scanner",

        page_subtitle="Scan uploaded files or pasted text for sensitive information and exposed secrets.",

        result=result

    )