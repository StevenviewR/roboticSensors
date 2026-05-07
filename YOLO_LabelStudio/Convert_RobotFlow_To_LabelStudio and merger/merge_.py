import json

# Load both datasets
with open("label_studio_format.json", "r") as f1:
    data1 = json.load(f1)

with open("label_studio_format_2.json", "r") as f2:
    data2 = json.load(f2)

# Merge the lists
merged_data = data1 + data2

# Extract all unique labels
all_labels = set()
for task in merged_data:
    for annotation in task.get("annotations", []):
        for result in annotation.get("result", []):
            labels = result.get("value", {}).get("rectanglelabels", [])
            all_labels.update(labels)

# Save merged data
with open("merged_label_studio.json", "w") as f:
    json.dump(merged_data, f, indent=2)

# Save the distinct categories
sorted_labels = sorted(all_labels)
with open("categories.json", "w") as f:
    json.dump(sorted_labels, f, indent=2)

# Create Label Studio Interface XML
color_palette = [
    "orange",
    "blue",
    "red",
    "green",
    "purple",
    "pink",
    "gray",
    "brown",
    "cyan",
    "yellow",
]

xml_lines = [
    "<View>",
    '  <Image name="image" value="$image" zoom="true"/>',
    '  <RectangleLabels name="label" toName="image">',
]

for i, label in enumerate(sorted_labels):
    color = color_palette[i % len(color_palette)]
    xml_lines.append(f'    <Label value="{label}" background="{color}"/>')

xml_lines += ["  </RectangleLabels>", "</View>"]

# Save the XML
interface_xml = "\n".join(xml_lines)
with open("label_studio_interface.xml", "w") as f:
    f.write(interface_xml)

print("✅ Merged file saved as 'merged_label_studio.json'")
print("✅ Categories saved as 'categories.json'")
print("✅ Label Studio interface XML saved as 'label_studio_interface.xml'")
