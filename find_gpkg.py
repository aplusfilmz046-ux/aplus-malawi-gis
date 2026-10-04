import os

print("--- SCANNING FOR UNZIPPED GEOPACKAGE FILES ---")
folder_path = "D:\\maping\\"

all_files = os.listdir(folder_path)
gpkg_files = [f for f in all_files if f.endswith('.gpkg')]

if not gpkg_files:
    print("❌ No .gpkg files found in the folder yet.")
    print("💡 Tip: Open your downloaded zip file and drag the .gpkg file directly into D:\\maping\\")
else:
    print("✅ Found your file(s)! Here is the exact name to copy:")
    for f in gpkg_files:
        print(f"👉   {f}")
