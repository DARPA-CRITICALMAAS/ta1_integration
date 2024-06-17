import os
import json
import numpy as np

class ocr4CDR():
    def __init__(self, input_path):
        self.cog_id = os.path.basename(input_path)
        with open(input_path, 'r') as f:
            self.data = json.load(f)
            
    def process_data_to_cdr(self):
        cdr_ocr = []
        for item in self.data['features']:
            temp_dict = {}
            polygon = np.array(item["geometry"]["coordinates"])
            temp_dict["coordinates"] = np.array([polygon[0,:,0],-polygon[0,:,1]]).transpose()
            temp_dict["coordinates"] = np.expand_dims(temp_dict["coordinates"], 0)
            temp_dict["bbox"] = [np.min(polygon[0,:,0]), -np.max(polygon[0,:,1]),\
                                np.max(polygon[0,:,0]), -np.min(polygon[0,:,1])]
            temp_dict["category"] = "ocr"
            temp_dict["text"] = item["properties"]["text"]
            temp_dict["model"] = "umn-mapkurator"
            temp_dict["model_version"] = "0.0.1"
            temp_dict["confidence"] = item["properties"]["score"]
            cdr_ocr.append(temp_dict)
        return cdr_ocr
        