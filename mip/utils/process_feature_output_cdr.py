import os
import json
from shapely.wkt import loads
from cdr_schemas.feature_results import FeatureResults

class feature4CDR():
    def __init__(self, file_path_list, mip_body):
        self.file_path_list = file_path_list
        self.mip_body = mip_body

    def replace_null_with_empty_string(self, obj):
        if isinstance(obj, dict):
            return {k: self.replace_null_with_empty_string(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.replace_null_with_empty_string(item) for item in obj]
        elif obj is None:
            return ""
        else:
            return obj

    def convert_float_to_int(self, obj):
        if isinstance(obj, dict):
            return {key: self.convert_float_to_int(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_float_to_int(item) for item in obj]
        elif isinstance(obj, float):
            return int(obj)
        else:
            return obj


    def process_line_features(self, feature_results):
        for feat in feature_results["line_features"]["features"]:
            feat["id"] = str(feat["id"])
            if feat["properties"]["dash_pattern"] == "dashed":
                feat["properties"]["dash_pattern"] = "dash"
        return feature_results

    def process_point_features(self, feature_results):
        new_feat_results = {}
        new_feat_results["legend_provenance"] = {
            "model": "umn-usc-inferlink",
            "model_version": "0.0.1",
            "confidence": 0
        }
        new_feat_results["legend_contour"] = []
        new_feat_results["abbreviation"] = ""
        new_feat_results["id"] = feature_results["id"]
        new_feat_results["name"] = feature_results["name"]
        new_feat_results["description"] = ""
        new_feat_results["legend_bbox"] = []
        new_feat_results["crs"] = feature_results["crs"]
        new_feat_results["cdr_projection_id"] = ""
        new_feat_results["point_features"] = {"features": []}
        
        for feat in feature_results['point_features']:
            for ffeat in feat['features']:
                ffeat["properties"]["dip"] = 0
                ffeat["properties"]["dip_direction"] = 0
            new_feat_results["point_features"]["features"].extend(feat['features'])
        return new_feat_results

    def process_polygon_features(self, all_feature_results):
        if isinstance(all_feature_results, list):
            if all_feature_results == []:
                return {}
            new_feat_results = all_feature_results[0]
            for feature_results in all_feature_results[:1]:
                new_feat_results["legend_contour"] = feature_results["legend_bbox"]
                new_feat_results["legend_bbox"] = []     
                new_feat_results["label"]  = ""
                new_feat_results["legend_provenance"] = {
                    "model": "umn-usc-inferlink",
                    "model_version": "0.0.1",
                    "confidence": 0
                }
                if feature_results["map_unit"]["b_age"] == 'null' or feature_results["map_unit"]["b_age"] is None:
                    new_feat_results["map_unit"]["b_age"] = 0 
                if feature_results["map_unit"]["t_age"] == 'null' or feature_results["map_unit"]["t_age"] is None:
                    new_feat_results["map_unit"]["t_age"] = 0
    
            for feature_results in all_feature_results[1:]:
                new_feat_results["polygon_features"]["features"].extend(feature_results["polygon_features"]["features"])
        elif isinstance(all_feature_results, dict):
            new_feat_results = all_feature_results
            new_feat_results["legend_contour"] = list(loads(all_feature_results["legend_bbox"]).exterior.coords)
            new_feat_results["legend_bbox"] = []     
            new_feat_results["label"]  = ""
            new_feat_results["legend_provenance"] = {
                "model": "umn-usc-inferlink",
                "model_version": "0.0.1",
                "confidence": 0
            }
            if all_feature_results["map_unit"]["b_age"] == 'null' or all_feature_results["map_unit"]["b_age"] is None:
                new_feat_results["map_unit"]["b_age"] = 0 
            if all_feature_results["map_unit"]["t_age"] == 'null' or all_feature_results["map_unit"]["t_age"] is None:
                new_feat_results["map_unit"]["t_age"] = 0
            print(type(all_feature_results["polygon_features"]["features"]))
        else:
            new_feat_results = {}
        return new_feat_results
    
    def get_feature_list(self):
        feature_list = []
        for file_path in self.file_path_list:
            with open(file_path, 'r') as f:
                feature_res = json.load(f)
            if self.mip_body["modules"] == ['line_extract']: 
                feature_res = self.process_line_features(feature_res)
                feature_res = self.replace_null_with_empty_string(feature_res)
                feature_list.append(feature_res)    
            elif self.mip_body["modules"] == ['point_extract']: 
                feature_res = self.process_point_features(feature_res)
                feature_res = self.replace_null_with_empty_string(feature_res)
                feature_list.append(feature_res)    
            elif self.mip_body["modules"] == ['polygon_extract']: 
                feature_res = self.process_polygon_features(feature_res)
                if feature_res != {}:
                    # feature_res["polygon_features"] = self.convert_float_to_int(feature_res["polygon_features"])
                    feature_res = self.replace_null_with_empty_string(feature_res)
                    feature_list.append(feature_res)         
        return feature_list
        
   