from services.fingerprint import create_datadna
from services.watermark import embed_watermark
from services.extraction import extract_watermark
from services.matching import match_fingerprint


# Step 1: Generate fingerprint
data = create_datadna()

print("Original Fingerprint:", data["fingerprint"])

# Step 2: Embed into image
input_image = "backend/app/test.jpg"
output_image = "backend/app/output.png"

embed_watermark(input_image, data["binary"], output_image)

# Step 3: Extract from image
extracted = extract_watermark(output_image)

print("Extracted Fingerprint:", extracted)

match = match_fingerprint(data["fingerprint"], extracted)
print("Match:", match)
