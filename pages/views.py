from django.views.generic import TemplateView
import boto3
from django.http import JsonResponse
from django.conf import settings
from django.views import View
from django.utils.timezone import now
from .models import AccessStatistic  # Import the model to log statistics
from user_agents import parse


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

    # def get(self, request, *args, **kwargs):
    #     # Log access statistics
    #     if request.method == "GET":  # Only log GET requests
    #         ip = self.get_client_ip(request)
    #         user = request.user if request.user.is_authenticated else "Unknown"
    #         user_agent_string = request.META.get("HTTP_USER_AGENT", "Unknown")
    #         browser_info, is_robot = self.get_browser_info(user_agent_string)
    #
    #         AccessStatistic.objects.create(
    #             user=user,
    #             ip_address=ip,
    #             url_visited=request.build_absolute_uri(),
    #             access_time=now(),
    #             browser_info=browser_info,  # Store browser information
    #             is_robot=is_robot,  # Store bot information
    #         )
    #     return super().get(request, *args, **kwargs)
    #
    #
    #
    # def get_client_ip(self, request):
    #     """Retrieve the client's IP address"""
    #     x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    #     if x_forwarded_for:
    #         ip = x_forwarded_for.split(",")[0]
    #     else:
    #         ip = request.META.get("REMOTE_ADDR")
    #     return ip
    #
    # def get_browser_info(self, user_agent_string):
    #     """
    #     Extract browser and robot information from the User-Agent string.
    #     :param user_agent_string: The User-Agent string from the request header.
    #     :return: (browser_info, is_robot) tuple containing browser details and whether it's a bot.
    #     """
    #     user_agent = parse(user_agent_string)  # Parse the User-Agent string
    #
    #     # Gather browser and operating system information
    #     browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string} on {user_agent.os.family} {user_agent.os.version_string}"
    #
    #     # Determine if the User-Agent belongs to a bot
    #     is_robot = user_agent.is_bot  # Returns True if it's a bot/crawler, False otherwise
    #
    #     return browser_info, is_robot




class PresignedUrlView(View):
    """
    A class-based view to generate presigned URLs for private S3 files.
    """

    # def get_client_ip(self, request):
    #     """Retrieve the client's IP address"""
    #     x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    #     if x_forwarded_for:
    #         ip = x_forwarded_for.split(",")[0]
    #     else:
    #         ip = request.META.get("REMOTE_ADDR")
    #     return ip

    def get(self, request, file_name):
        """
        Handles GET requests to generate a presigned URL for a given file.
        :param request: Django's request object.
        :param file_name: The name of the file in the private S3 bucket.
        """

        # if request.method == "GET":  # Log only GET requests
        #     ip = self.get_client_ip(request)
        #     user = request.user if request.user.is_authenticated else "Unknown"
        #     AccessStatistic.objects.create(
        #         user=user,
        #         ip_address=ip,
        #         url_visited=request.build_absolute_uri(),
        #         access_time=now(),
        #     )

        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        try:
            # Generate the presigned URL
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.AWS_S3_PRIVATE_BUCKET_NAME, "Key": file_name},
                ExpiresIn=3600,  # URL valid for 1 hour
            )
            return JsonResponse({"presigned_url": presigned_url})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


class ChurnAnalysisView(TemplateView):
    template_name = "pages/ChurnAnalysis.html"