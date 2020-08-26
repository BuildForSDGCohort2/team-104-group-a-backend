from rest_framework import generics
from rest_framework.response import Response


class Underconstruction(generics.GenericAPIView):
    @classmethod
    def get(self, request, *args, **kwargs):
        return Response({"Patient_Care_App": "This is the official API of Team-104-Group-A.", "Availability": "Under Construction"})
