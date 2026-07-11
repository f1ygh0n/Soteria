from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename

import os

deepfake_bp = Blueprint("deepfake", __name__)

UPLOAD_FOLDER = "static/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@deepfake_bp.route("/deepfake", methods=["GET", "POST"])
def deepfake():

    result = None
    image_path = None

    if request.method == "POST":

        image = request.files.get("image")

        if image and image.filename:

            filename = secure_filename(image.filename)

            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
            )

            image.save(filepath)

            image_path = "/" + filepath.replace("\\", "/")

            # Placeholder until detector is implemented
            result = {

                "score": 78,

                "verdict": "Likely Authentic",

                "summary": (
                    "Only minor visual inconsistencies were detected. "
                    "No strong indicators of AI manipulation were found."
                ),

                "checks": [

                    {
                        "name": "Face Detection",
                        "status": "Passed"
                    },

                    {
                        "name": "Lighting Consistency",
                        "status": "Passed"
                    },

                    {
                        "name": "Compression Analysis",
                        "status": "Moderate"
                    },

                    {
                        "name": "Metadata",
                        "status": "Missing"
                    },

                    {
                        "name": "Skin Texture",
                        "status": "Normal"
                    },

                    {
                        "name": "Sharpness",
                        "status": "Normal"
                    }

                ]

            }

    return render_template(

        "deepfake.html",

        page_title="Deepfake Detector",

        page_subtitle="Detect manipulated images and AI-generated media.",

        result=result,

        image_path=image_path

    )