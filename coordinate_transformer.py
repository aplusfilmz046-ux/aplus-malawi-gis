from pyproj import Transformer

def convert_survey_to_wgs84(easting, northing, zone_number=36, southern_hemisphere=True):
    """
    Converts Malawi survey grid points (UTM Projection) into standard smartphone GPS degrees (WGS84).
    Most of Malawi, including Lilongwe and Blantyre, falls inside UTM Zone 36 South (36S).
    """
    # 1. Define the coordinate systems
    # epsg:32736 is the official universal tracking code for UTM Zone 36 South
    # epsg:4326 is the standard universal WGS84 Latitude/Longitude used by smartphones
    input_projection = f"epsg:32736" 
    output_projection = "epsg:4326"
    
    try:
        # 2. Initialize the mathematical transformer engine
        spatial_transformer = Transformer.from_crs(input_projection, output_projection, always_xy=True)
        
        # 3. Execute the coordinate calculation loop
        longitude, latitude = spatial_transformer.transform(easting, northing)
        
        return round(latitude, 6), round(longitude, 6)
        
    except Exception as error:
        print(f"❌ [TRANSFORM ERROR] Calculation failed due to: {error}")
        return None

if __name__ == "__main__":
    print("--- MALAWI SURVEY GRID MATHEMATICAL TRANSFORMER ---")
    
    # Let's test a real structural plot beacon point located in Lilongwe
    mock_surveyor_x = 582845.0  # Easting coordinate from layout plan
    mock_surveyor_y = 8460120.0 # Northing coordinate from layout plan
    
    print(f"📐 Input Legal Survey Plan Coordinates -> X: {mock_surveyor_x}, Y: {mock_surveyor_y}")
    print("[SYSTEM] Executing geospatial projection transformation math...")
    
    gps_coordinates = convert_survey_to_wgs84(mock_surveyor_x, mock_surveyor_y)
    
    if gps_coordinates:
        lat, lon = gps_coordinates
        print("=" * 65)
        print("✅ SUCCESS: Coordinates converted into standard smartphone format!")
        print(f"🌐 Latitude Degree  : {lat}")
        print(f"🌐 Longitude Degree : {lon}")
        print("=" * 65)
        print(f"💡 You can now safely pass these degrees directly into our SQLite database!")
