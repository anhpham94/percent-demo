from PIL import Image
import base64
from io import BytesIO

def image_to_base64(image_path):
    with Image.open(image_path) as image:
        image.thumbnail((512, 512)) # Resize to avoid huge output
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

print("DATA:image/jpeg;base64," + image_to_base64("ui_screenshot_default.png"))
