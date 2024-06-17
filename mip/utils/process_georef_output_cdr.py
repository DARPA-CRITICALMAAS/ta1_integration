import os
import json
import uuid
from cdr_schemas.georeference import (GeoreferenceResult, GeoreferenceResults, ProjectionResult)
import rasterio as rio
import rasterio.transform as riot
from pyproj import Transformer
from PIL import Image
from rasterio.warp import Resampling, calculate_default_transform, reproject

Image.MAX_IMAGE_PIXELS = None

class georef4CDR:
    def __init__(self, file_path):
        self.georef_file_path = file_path
        # Open the GeoJSON file
        with open(self.georef_file_path, 'r') as f:
            self.georef_res = json.load(f)
        
    def get_all_gcps(self):
        all_gcps = []
        for i, x in enumerate(self.georef_res['gcps']):
            all_gcps.append(
                {
                    "gcp_id": str(uuid.uuid4()),
                    "map_geom": {
                        "type": "Point",
                        "longitude":x['map_geom']["longitude"],
                        "latitude": x['map_geom']["latitude"]
                    },
                    "px_geom": {
                        "type": "Point",
                        "rows_from_top": x['px_geom']["rows_from_top"],
                        "columns_from_left": x['px_geom']["columns_from_left"]
                    },
                    "confidence": x['confidence'],
                    "model": x['model'],
                    "model_version": x['model_version'],
                    "crs": x['crs']
                }
            )
        return all_gcps


    # def georeference_result(self):
    #     cog_id = self.payload['cog_id']
    #     map_path = os.getenv("TA1_INPUTS_DIR") + '/maps' + f'/{cog_id}' + f'/{cog_id}.tif'
    #     img = Image.open(map_path)
    #     width, height = img.size
    #     proj_file_path = os.getenv("TA1_OUTPUTS_DIR") + f'/{cog_id}' + '/georeference'+ f'/{cog_id}.pro.cog.tif'

    #     gcps = self.get_all_gcps()
    #     geo_transform = self.cps_to_transform(gcps, height=height, to_crs="EPSG:4267")
    
    #     self.project_(map_path, proj_file_path,
    #              geo_transform, "EPSG:4267")
    
    #     gcp_ids = list(map(lambda x: x["gcp_id"], gcps))
    #     # pr = ProjectionResult(crs="EPSG:4267", gcp_ids=gcp_ids,
    #                           # file_name=proj_file_path)
    #     # pr = ProjectionResult(crs="EPSG:4267", gcp_ids=gcp_ids,
    #                           # file_name="")
    #     # gr = GeoreferenceResult(likely_CRSs=["EPSG:4267"], map_area= None, projections=[pr])
    #     gr = GeoreferenceResult(likely_CRSs=[], map_area= None, projections=[])
    #     # print(gr.projections)
    #     return gr
