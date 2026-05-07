import json
import os

# Load your Roboflow COCO JSON file
with open("_annotations.coco.json") as f:
    coco = json.load(f)

# Build category lookup
categories = {cat["id"]: cat["name"] for cat in coco["categories"]}

# Build image lookup
images = {img["id"]: img for img in coco["images"]}

# Optional: define your image path prefix for Label Studio to locate the images
IMAGE_PATH_PREFIX = "/data/local-files/?d=train/"

# Collect annotations per image
annotations_by_image = {}
for ann in coco.get("annotations", []):
    img_id = ann["image_id"]
    bbox = ann["bbox"]  # [x, y, width, height]
    category_id = ann["category_id"]

    image = images[img_id]
    width = image["width"]
    height = image["height"]

    # Normalize coordinates for Label Studio
    x = bbox[0] / width * 100
    y = bbox[1] / height * 100
    w = bbox[2] / width * 100
    h = bbox[3] / height * 100

    result = {
        "from_name": "label",
        "to_name": "image",
        "type": "rectanglelabels",
        "value": {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "rectanglelabels": [categories[category_id]],
        },
    }

    if img_id not in annotations_by_image:
        annotations_by_image[img_id] = []

    annotations_by_image[img_id].append(result)

# Convert to Label Studio format
label_studio_data = []
for img_id, image in images.items():
    entry = {
        "data": {"image": IMAGE_PATH_PREFIX + image["file_name"]},
        "annotations": [{"result": annotations_by_image.get(img_id, [])}],
    }
    label_studio_data.append(entry)

# Save to file
with open("label_studio_format.json", "w") as f:
    json.dump(label_studio_data, f, indent=2)

print("Conversion complete. Output saved to label_studio_format.json.")
print("Categories:")
for cat_id, cat_name in categories.items():
    print(f"{cat_id}: {cat_name}")
