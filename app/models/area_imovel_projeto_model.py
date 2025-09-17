# feature_model.py
from bson import ObjectId

class FeatureModel:
    def __init__(self, id: str, geometry: dict, properties: dict, _id=None):
        from bson import ObjectId
        self._id = _id or ObjectId()
        self.id = id
        self.type = "Feature"
        self.geometry = geometry
        self.properties = properties

    def to_dict(self):
        return {
            "_id": self._id,
            "id": self.id,
            "type": self.type,
            "geometry": self.geometry,
            "properties": self.properties
        }
