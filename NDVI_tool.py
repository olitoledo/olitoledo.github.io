"""
My section of a collaborative .arcpy script that calculated slope, aspect,
NDVI, proximity to roads, areas of historic burn, and used these layers
as inputs for a suitability analysis to determine wildfire risk.

Part of a final group project for Geog 181C - Programming for ArcGIS Pro.

Software Versions:
ArcGIS Pro 3.2.2
Python 3.9.18
IDLE 3.9.18

"""

import arcpy
from arcpy.sa import *

StudyArea_input = arcpy.GetParameterAsText(1)

NIR_input = arcpy.GetParameterAsText(4)
Red_input = arcpy.GetParameterAsText(5)
NDVI_TIF = r"memory/NDVI_TIF"


def NDVI(NIR_input, Red_input, StudyArea_input, NDVI_TIF):
    """
    Calculates the Normalized Difference Vegetation Index (NDVI) for
    any input data. Scores NDVI values 0-5 in preparation for suitability
    analysis: higher NDVI values indicate healthier vegetation that is
    less likely to burn, and lower NDVI values indicate dry and dead
    vegetation, which is usually more likely to be fuel for fire.

    Parameters:

        NIR_input: geotiff
            Near infrared band.
        Red_input: geotiff
            Red band.
        StudyArea_input: shapefile
            Outline of study area.

    Returns:
        NDVI_TIF: geotiff
            Output NDVI image.
    """
    # Load rasters
    NIRBand = arcpy.Raster(NIR_input)
    RedBand = arcpy.Raster(Red_input)

    # Calculate NDVI
    output_ndvi = (NIRBand - RedBand) / (NIRBand + RedBand)

    # Remap NDVI values
    ndvi_remap = RemapRange([[-1, 0.15, 0], [0.6, 1, 1], [0.5, 0.6, 2], [0.4, 0.5, 3], [0.2, 0.4, 4], [0.15, 0.2, 5]])
    ndvi_class = Reclassify(output_ndvi, "Value", ndvi_remap)

    # Apply mask
    out_raster = arcpy.sa.ExtractByMask(
        in_raster=ndvi_class,
        in_mask_data=StudyArea_input,
        extraction_area="INSIDE")

    # Save output
    out_raster.save(NDVI_TIF)

# Run function
arcpy.CheckOutExtension("Spatial")

NDVI(NIR_input, Red_input, StudyArea_input, NDVI_TIF)

arcpy.CheckInExtension("Spatial")