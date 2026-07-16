import cv2
import os 
import tempfile
import numpy as np

from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance

from ai.deepfake_ai import detect_ai_image

FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40,40))
    return len(faces)

def calculate_blur(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def calculate_noise(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).std()

def edge_density(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,100,200)
    return edges.mean()

def brightness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray.mean()

def metadata_info(path):
    try:
        exif = Image.open(path).getexif()
        if exif and len(exif)>0:
            return True,len(exif)
    except Exception:
        pass
    return False,0

def error_level_analysis(path):

    original = Image.open(path).convert("RGB")

    temp = tempfile.NamedTemporaryFile(

        suffix=".jpg",

        delete=False

    )

    original.save(

        temp.name,

        "JPEG",

        quality=90

    )

    compressed = Image.open(temp.name)

    diff = ImageChops.difference(

        original,

        compressed

    )

    extrema = diff.getextrema()

    maximum = max(

        channel[1]

        for channel in extrema

    )

    scale = 1 if maximum == 0 else 255 / maximum

    ela = ImageEnhance.Brightness(diff).enhance(scale)

    ela_path = (

        os.path.splitext(path)[0]

        + "_ela.png"

    )

    ela.save(ela_path)

    temp.close()

    os.remove(temp.name)

    return maximum, ela_path

def texture_uniformity(image):

    gray = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )

    block = 32

    variances = []

    for y in range(

        0,

        gray.shape[0],

        block

    ):

        for x in range(

            0,

            gray.shape[1],

            block

        ):

            region = gray[

                y:y+block,

                x:x+block

            ]

            if region.size:

                variances.append(

                    region.var()

                )

    return float(

        np.std(variances)

    )

def frequency_energy(image):

    gray = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )

    fft = np.fft.fft2(gray)

    fft = np.fft.fftshift(fft)

    magnitude = np.log(

        np.abs(fft) + 1

    )

    return magnitude.mean()

def saturation(image):

    hsv = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2HSV

    )

    return hsv[:, :, 1].mean()

def contrast(image):

    gray = cv2.cvtColor(

        image,

        cv2.COLOR_BGR2GRAY

    )

    return gray.std()

def analyze_image(path):

    image = cv2.imread(path)

    if image is None:

        return {

            "score": 0,

            "verdict": "Invalid Image",

            "summary": "The uploaded image could not be read.",

            "checks": []

        }

    height, width = image.shape[:2]

    score = 100

    checks = []

    # Resolution

    pixels = width * height

    if pixels >= 1920 * 1080:

        checks.append({

            "name": "Resolution",

            "status": "Excellent"

        })

    elif pixels >= 1280 * 720:

        score -= 3

        checks.append({

            "name": "Resolution",

            "status": "Good"

        })

    else:

        score -= 8

        checks.append({

            "name": "Resolution",

            "status": "Low"

        })

    # Face Detection

    faces = detect_faces(image)

    checks.append({

        "name": "Face Detection",

        "status": "No faces detected"

        if faces == 0

        else f"{faces} face(s) detected"

    })

    # Blur

    blur = calculate_blur(image)

    if blur > 200:

        blur_status = "Sharp"

    elif blur > 100:

        blur_status = "Moderately Sharp"

        score -= 5

    else:

        blur_status = "Blurry"

        score -= 12

    checks.append({

        "name": "Sharpness",

        "status": blur_status

    })

    # Noise

    noise = calculate_noise(image)

    if noise < 8:

        noise_status = "Very Smooth"

        score -= 8

    elif noise < 18:

        noise_status = "Normal"

    else:

        noise_status = "Natural"

    checks.append({

        "name": "Noise Consistency",

        "status": noise_status

    })

    # Edge Density

    edge = edge_density(image)

    if edge < 8:

        edge_status = "Low Detail"

        score -= 5

    elif edge < 20:

        edge_status = "Normal"

    else:

        edge_status = "High Detail"

    checks.append({

        "name": "Edge Analysis",

        "status": edge_status

    })

    # Brightness

    bright = brightness(image)

    if bright < 40:

        bright_status = "Very Dark"

        score -= 3

    elif bright > 220:

        bright_status = "Very Bright"

        score -= 3

    else:

        bright_status = "Normal"

    checks.append({

        "name": "Brightness",

        "status": bright_status

    })

    # Metadata

    has_metadata, count = metadata_info(path)

    checks.append({

        "name": "Metadata",

        "status":

            f"{count} EXIF fields"

            if has_metadata

            else "Unavailable"

    })

    # Error Level Analysis

    ela_score, ela_path = error_level_analysis(path)

    if ela_score > 20:

        score -= 12

    elif ela_score > 10:

        score -= 6

    checks.append({

        "name": "Error Level Analysis",

        "status": f"{ela_score:.1f}"

    })

    # Texture

    texture = texture_uniformity(image)

    if texture < 15:

        score -= 8

    checks.append({

        "name": "Texture Uniformity",

        "status": f"{texture:.1f}"

    })

    # Frequency Spectrum

    fft = frequency_energy(image)

    if fft < 6:

        score -= 6

    checks.append({

        "name": "Frequency Spectrum",

        "status": f"{fft:.1f}"

    })

    # Saturation

    sat = saturation(image)

    if sat > 180:

        score -= 5

    checks.append({

        "name": "Color Saturation",

        "status": f"{sat:.1f}"

    })

    # Contrast

    cont = contrast(image)

    if cont < 25:

        score -= 5

    checks.append({

        "name": "Local Contrast",

        "status": f"{cont:.1f}"

    })



    score = max(0, min(score, 100))



    if score >= 85:

        verdict = "Likely Authentic"

    elif score >= 70:

        verdict = "Probably Authentic"

    elif score >= 50:

        verdict = "Needs Manual Review"

    else:

        verdict = "Potential Manipulation"



    summary = (

        f"Analyzed a {width}×{height} image using "

        "resolution, sharpness, noise consistency, "

        "edge density, brightness, metadata, "

        "Error Level Analysis (ELA), texture, "

        "frequency spectrum, saturation and contrast. "

        "This forensic assessment is heuristic and "

        "should not be considered definitive proof "

        "of authenticity."

    )

    ai = detect_ai_image(path)

    return {

        "score": score,

        "verdict": verdict,

        "summary": summary,

        "checks": checks,

        "ai": ai

    }
