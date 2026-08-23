from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import Parent
from .serializers import ParentSerializer
from django.core.mail import send_mail

class SignupView(generics.CreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        parent = self.queryset.last()  # last created parent

        # ✅ Send parent ID in response
        res_data = {
            "message": "Signup successful!",
            "parent_id": parent.id,
            "username": parent.username,
            "email": parent.email
        }

        # ✅ Optional: Send email with Parent ID
        try:
            send_mail(
                subject="Your Parent ID for Missing Child Portal",
                message=f"Hello {parent.username},\n\nYour Parent ID is: {parent.id}\nPlease use this ID when registering your child.",
                from_email="missingchild613@gmail.com",
                recipient_list=[parent.email],
                fail_silently=False,
            )
        except Exception as e:
            print("⚠️ Email sending failed:", e)

        return Response(res_data)
# Create your views here.
