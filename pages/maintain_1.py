import os
import django
import requests
from django.apps import apps  # For dynamically accessing models
import json
from django.db import transaction
import time


def fetch_organization_by_ip(ip: str) -> str:
    """
    Fetches the organization name using the provided IP address via an external API.
    """
    if ip == "127.0.0.1":
        return "Local","Local"

    if ip == '68.173.141.46':
        return "myPublicIP","myPublicIP"


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
        return "Lookup Failed","Lookup Failed"


def lookup_organizations():
    """
    Lookups the organization for each IP in the AccessStatistic table
    and updates the `owner` field for each record.
    """
    print("Fetching IPs from the database...")

    # Access the AccessStatistic model dynamically using its full qualified name
    AccessStatistic = apps.get_model('pages', 'AccessStatistic')


    # Fetch all records from the AccessStatistic table
    access_statistics = AccessStatistic.objects.all()

    for record in access_statistics:
        ip_address = record.ip_address
        if not ip_address:
            continue  # Skip records with no IP address

        print(f"Looking up organization for IP: {ip_address}")

        # Look up the organization for each IP address
        owner, detail_info = fetch_organization_by_ip(ip_address)

        # Print the result for debugging purposes
        print(f"IP: {ip_address}, Owner:{owner}, detail_info: {detail_info}")

        # Update the record in the database
        record.owner = owner
        record.detail_ipinfo = detail_info
        record.save(force_update=True)
        time.sleep(5)
        pass


if __name__ == "__main__":
    # Set the DJANGO_SETTINGS_MODULE environment variable if not already set
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")

    # Initialize Django's setup
    django.setup()

    # Run the lookup
    lookup_organizations()
