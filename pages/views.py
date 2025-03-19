from django.views.generic import TemplateView
import boto3
from django.http import JsonResponse
from django.conf import settings
from django.views import View
from django.utils.timezone import now
from .models import AccessStatistic  # Import the model to log statistics


# Create your views here.
class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Get the existing context data
        context = super().get_context_data(**kwargs)

        # Get the session ID (cookie sessionid)
        session_id = self.request.session.session_key

        # Ensure the session is created
        if session_id is None:
            self.request.session.save()
            session_id = self.request.session.session_key

        # Pass the session ID to the context
        context['session_id'] = session_id
        return context

    def get(self, request, *args, **kwargs):
        # Log access statistics
        if request.method == "GET":  # Log only GET requests
            ip = self.get_client_ip(request)
            user = request.user if request.user.is_authenticated else "Unknown"
            AccessStatistic.objects.create(
                user=user,
                ip_address=ip,
                url_visited=request.build_absolute_uri(),
                access_time=now(),
            )
        return super().get(request, *args, **kwargs)


    def get_client_ip(self, request):
        """Retrieve the client's IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip



class PresignedUrlView(View):
    """
    A class-based view to generate presigned URLs for private S3 files.
    """

    def get(self, request, file_name):
        """
        Handles GET requests to generate a presigned URL for a given file.
        :param request: Django's request object.
        :param file_name: The name of the file in the private S3 bucket.
        """
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )

        try:
            # Generate the presigned URL
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.AWS_S3_BUCKET_NAME, "Key": file_name},
                ExpiresIn=3600,  # URL valid for 1 hour
            )
            return JsonResponse({"presigned_url": presigned_url})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class ChurnAnalysisView(TemplateView):
    template_name = "pages/ChurnAnalysis.html"