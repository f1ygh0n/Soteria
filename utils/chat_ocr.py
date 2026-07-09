from PIL import Image
import easyocr
import numpy as np

reader = easyocr.Reader(
    ["en"],
    gpu=False
)

IGNORE_LINES = {
    "type a message",
    "message",
    "typing...",
    "seen",
    "delivered",
    "sent",
    "online",
    "today",
    "yesterday",
    "active now",
    "write a message",
    "tap to chat",
    "search",
    "search messages",
    "camera",
    "calls",
    "status",
    "chats",
    "contacts",
    "new message",
    "reply",
    "forward",
    "copy",
    "delete",
    "edited"
}


def clean_chat_text(text):

    cleaned = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.lower() in IGNORE_LINES:
            continue

        cleaned.append(line)

    return "\n".join(cleaned)


def extract_chat_text(file):

    image = Image.open(file).convert("RGB")

    image = np.array(image)

    # OCR
    results = reader.readtext(
        image,
        detail=0,
        paragraph=True
    )

    text = "\n".join(results)

    return clean_chat_text(text)