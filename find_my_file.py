import os

print("--- SCANNING FOR UNZIPPED GEOJSON FILES ---")
folder_path = "D:\\maping\\"

# List all files inside your development directory
all_files = os.listdir(folder_path)
geojson_files = [f for f in all_files if f.endswith('.geojson')]

if not geojson_files:
    print("❌ No .geojson files found in the folder yet.")
    print("💡 Tip: Make sure you open the downloaded zip file and drag the file directly into D:\\maping\\")
else:
    print("✅ Found your file(s)! Here is the exact name to copy:")
    for f in geojson_files:
        print(f"👉   {f}")
