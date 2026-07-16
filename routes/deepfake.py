from flask import Blueprint, render_template, request
import os

from utils.image_rules import analyze_image

deepfake_bp = Blueprint("deepfake", __name__)

UPLOAD_FOLDER = "static/uploads"


@deepfake_bp.route("/deepfake", methods=["GET", "POST"])
def deepfake():

    result = None
    image_path = None

    if request.method == "POST":

        image = request.files.get("image")

        if image and image.filename:

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filepath = os.path.join(
                UPLOAD_FOLDER,
                image.filename
            )

            image.save(filepath)

            image_path = "/" + filepath.replace("\\", "/")

            result = analyze_image(filepath)

    return render_template(

        "deepfake.html",

        page_title="Deepfake Detector",

        page_subtitle="Analyze images for signs of manipulation using computer vision.",

        result=result,

        image_path=image_path

    )