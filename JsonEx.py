# import json

class JsonEx():

    @staticmethod
    def vector2ToJson(vector):
        return [vector.x, vector.y]
    @staticmethod
    def vector2LoadFromJson(vector, vectorInJson):
        vector.x = vectorInJson[0]
        vector.y = vectorInJson[1]

    @staticmethod
    def vector3ToJson(vector):
        return [vector.x, vector.y, vector.z]
    @staticmethod
    def vector3LoadFromJson(vector, vectorInJson):
        vector.x = vectorInJson[0]
        vector.y = vectorInJson[1]
        vector.z = vectorInJson[2]

    @staticmethod
    def propArrayToJson(propArray):
        rez = []
        for prop in propArray:
            rez.append(prop)
        return rez
    @staticmethod
    def propArrayLoadFromJson(propArray, propArrayInJson):
        for i, prop in enumerate(propArrayInJson):
            propArray[i] = prop

    @staticmethod
    def colorToJson(color):
        return [color.r, color.g, color.b]
    @staticmethod
    def colorLoadFromJson(color, colorInJson):
        color.r = colorInJson[0]
        color.g = colorInJson[1]
        color.b = colorInJson[2]
