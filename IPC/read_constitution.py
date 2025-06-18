import json

with open('indian_constitution_cleaned.json', encoding='utf-8') as f:
    data = json.load(f)

# Print top-level structure
print("Top-level keys:", list(data.keys()) if isinstance(data, dict) else "Not a dictionary")
print("\nFirst item sample:")
if isinstance(data, list):
    print(data[0])
elif isinstance(data, dict):
    for k, v in list(data.items())[:1]:
        print(f"{k}: {v}")