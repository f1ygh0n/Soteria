from flask import Blueprint, render_template, request
import os
import time
import uuid

from utils.image_rules import analyze_image

deepfake_bp = Blueprint("deepfake", __name__)

UPLOAD_FOLDER = "static/uploads"

MAX_FILE_AGE = 300  # 5 minutes

def cleanup_uploads(folder):

    if not os.path.exists(folder):
        return

    now = time.time()

    for filename in os.listdir(folder):

        filepath = os.path.join(folder, filename)

        if not os.path.isfile(filepath):
            continue

        try:

            age = now - os.path.getmtime(filepath)

            if age > MAX_FILE_AGE:

                os.remove(filepath)

        except OSError:

            pass


@deepfake_bp.route("/deepfake", methods=["GET", "POST"])
def deepfake():

    result = None
    image_path = None

    if request.method == "POST":

        image = request.files.get("image")

        if image and image.filename:

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            # Delete old uploads
            cleanup_uploads(UPLOAD_FOLDER)

            # Generate unique filename
            extension = os.path.splitext(image.filename)[1].lower()

            filename = f"{uuid.uuid4().hex}{extension}"

            filepath = os.path.join(
                UPLOAD_FOLDER,
                filename
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