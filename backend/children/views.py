# backend/children/views.py
from rest_framework import generics
from rest_framework.response import Response
from .models import Child
from .serializers import ChildSerializer
from deepface import DeepFace
from notifications.utils import send_alert
import tempfile, traceback

class ChildCreateView(generics.CreateAPIView):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer

class ChildSearchView(generics.GenericAPIView):
    def post(self, request):
        if 'photo' not in request.FILES:
            return Response({"error": "No photo uploaded"}, status=400)

        uploaded_file = request.FILES['photo']
        location_text = request.data.get("location", "Unknown Location")
        lat = request.data.get("lat", None)
        lon = request.data.get("lon", None)

        # capture uploader IP (best-effort)
        uploader_ip = request.META.get("REMOTE_ADDR") or request.META.get("HTTP_X_FORWARDED_FOR", "")

        # save temp file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        for chunk in uploaded_file.chunks():
            temp_file.write(chunk)
        temp_file.close()

        for child in Child.objects.all():
            try:
                result = DeepFace.verify(temp_file.name, child.photo.path)
                print("DeepFace result:", result)
                if result.get("verified") or (result.get("distance") is not None and float(result.get("distance")) < 0.45):
                    print(f"✅ Match found for {child.name}. Sending alerts...")
                    # pass location & coordinates & uploader_ip to send_alert
                    send_alert(child.parent.id, location=location_text, lat=lat, lon=lon, uploader_ip=uploader_ip)

                    return Response({
                        "match": True,
                        "child_id": child.id,
                        "child_name": child.name,
                        "location": location_text,
                        "lat": lat,
                        "lon": lon,
                    })
            except Exception as e:
                print(f"Error comparing {child.name}: {e}")
                traceback.print_exc()
                continue

        return Response({"match": False})
