import logging
from django.utils.timezone import now
from user_agents import parse  # Install this with 'pip install pyyaml user-agents'
from pages.models import AccessStatistic  # Import the AccessStatistic model (adjust the path if needed)
from django.conf import settings
import requests
import json


logger = logging.getLogger(__name__)  # For debugging purposes


class AccessLogMiddleware:
    """
    Middleware to log access statistics for all page requests.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        self.log_access(request)  # Log access data
        response = self.get_response(request)
        return response

    def fetch_organization_by_ip(self, ip: str) -> str:
        """
        Fetches the organization name using the provided IP address via an external API.
        """
        if ip == "127.0.0.1":
            return "Local", "Local"

        if ip == '68.173.141.46':
            return "myPublicIP", "myPublicIP"

        try:
            api_url = f"http://ip-api.com/json/{ip}"
            response = requests.get(api_url)
            status_code = response.status_code

            if status_code != 200:
                return "Unknown", "Unknown"

            response_data = response.json()
            owner = response_data.get('org', "Unknown")
            return owner, json.dumps(response_data).replace('\n', ' ')
        except Exception:
            return "Lookup Failed", "Lookup Failed"

    def get_browser_info(self, user_agent_string):
        """
        Extract browser and robot information from the User-Agent string.
        :param user_agent_string: The User-Agent string from the request header.
        :return: (browser_info, is_robot) tuple containing browser details and whether it's a bot.
        """
        user_agent = parse(user_agent_string)  # Parse the User-Agent string

        # Gather browser and operating system information
        browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string} on {user_agent.os.family} {user_agent.os.version_string}"

        # Determine if the User-Agent belongs to a bot
        is_robot = user_agent.is_bot  # Returns True if it's a bot/crawler, False otherwise

        return browser_info, is_robot

    def log_access(self, request):
        """
        Logs access details including IP, browser info, and whether it is a bot.
        """
        # Exclude static and admin URLs if you don't want to log them
        # if request.path.startswith('/static') or request.path.startswith('/admin'):
        #     return

        try:
            # Gather IP address
            ip_address = self.get_client_ip(request)

            # Get User-Agent details
            user_agent_string = request.META.get("HTTP_USER_AGENT", "Unknown")
            browser_info, is_robot = self.get_browser_info(user_agent_string)
            # user_agent = parse(user_agent_string)
            # browser_info = f"{user_agent.browser.family} {user_agent.browser.version_string} on {user_agent.os.family} {user_agent.os.version_string}"
            # is_robot = user_agent.is_bot  # Check if it's a bot or human
            # Identify the user
            user = request.user if request.user.is_authenticated else "Anonymous"

            # Look up the organization for each IP address
            owner, detail_info = self.fetch_organization_by_ip(ip_address)

            # Store the statistics into the database
            AccessStatistic.objects.create(
                user=user,
                ip_address=ip_address,
                url_visited=request.build_absolute_uri(),
                access_time=now(),
                browser_info=browser_info,
                is_robot=is_robot,
                owner = owner,
                detail_ipinfo = detail_info
            )

        except Exception as e:
            # Log any errors without breaking the site
            logger.error(f"Error logging access: {e}")

    def get_client_ip(self,request):
        """
        Retrieve the client's IP address.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
