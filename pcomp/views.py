from django.views.generic import TemplateView
import boto3
from api.models import Prompts
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from datetime import datetime, timedelta

class PromptInputView(TemplateView):
    template_name = 'pcomp/prompt_input.html'

class PromptListView(TemplateView):
    template_name = 'pcomp/prompt_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the day and hour filter values from request GET parameters
        day_filter = self.request.GET.get('day', None)
        hour_filter = self.request.GET.get('hour', None)

        # Get all prompts from the database
        all_prompts = Prompts.objects.all().order_by('-date')  # Order by date descending

        # Extract unique days from prompts
        unique_days = {}
        for prompt in all_prompts:
            # Convert UTC time to local time for display
            local_date = timezone.localtime(prompt.date)
            day_str = local_date.strftime('%Y-%m-%d')
            day_display = local_date.strftime('%B %d, %Y')  # Format: January 01, 2023
            unique_days[day_str] = day_display

        # Filter prompts by day if a day filter is provided
        if day_filter:
            # Filter prompts for the selected day
            from datetime import datetime, timedelta

            # Parse the local date from the filter
            local_date = datetime.strptime(day_filter, '%Y-%m-%d')

            # Get the current timezone
            current_tz = timezone.get_current_timezone()

            # Create a timezone-aware datetime for the start of the local day
            local_day_start = datetime(local_date.year, local_date.month, local_date.day, 0, 0, 0, tzinfo=current_tz)
            # Create a timezone-aware datetime for the end of the local day
            local_day_end = datetime(local_date.year, local_date.month, local_date.day, 23, 59, 59, tzinfo=current_tz)

            # Convert local datetimes to UTC for filtering
            from datetime import timezone as py_timezone
            utc_day_start = local_day_start.astimezone(py_timezone.utc)
            utc_day_end = local_day_end.astimezone(py_timezone.utc)

            # Filter prompts between UTC start and end times
            from django.db.models import Q
            day_filtered_prompts = all_prompts.filter(
                date__gte=utc_day_start,
                date__lte=utc_day_end
            )

            # Extract unique hours for the selected day
            unique_hours = {}
            for prompt in day_filtered_prompts:
                # Convert UTC time to local time for display
                local_date = timezone.localtime(prompt.date)
                hour_str = local_date.strftime('%H')
                hour_display = local_date.strftime('%I %p').lstrip('0')  # Format: 1 PM (12-hour format)
                unique_hours[hour_str] = hour_display

            # Filter by hour if hour filter is provided
            if hour_filter:
                # Convert local hour to UTC hour for filtering
                local_hour = int(hour_filter)
                # Get the UTC offset in hours
                utc_offset = timezone.get_current_timezone().utcoffset(datetime.now()).total_seconds() / 3600
                # Calculate the UTC hour
                utc_hour = (local_hour - int(utc_offset)) % 24

                prompts = day_filtered_prompts.filter(
                    Q(date__hour=utc_hour)
                ).order_by('-date')
            else:
                prompts = day_filtered_prompts.order_by('-date')
        else:
            prompts = all_prompts
            unique_hours = {}

        # Create S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        # Include all necessary fields for the template
        prompts_data = []
        for prompt in prompts:
            # Generate a presigned URL for the S3 object
            try:
                presigned_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": settings.AWS_S3_BUCKET_NAME, "Key": prompt.img_path},
                    ExpiresIn=3600,  # URL valid for 1 hour
                )
                # Convert UTC time to local time for display
                local_date = timezone.localtime(prompt.date)
                prompts_data.append({
                    'id': prompt.id,
                    'prompt': prompt.prompt,
                    'model': prompt.model,
                    'resolution': prompt.resolution,
                    'quality': prompt.quality,
                    'note': prompt.note,
                    'date': local_date,  # Local time instead of UTC
                    'image_url': presigned_url  # Presigned URL for S3 object
                })
            except Exception as e:
                # If there's an error generating the presigned URL, log it and continue
                print(f"Error generating presigned URL for {prompt.img_path}: {str(e)}")
                continue

        # Pass the data to the template
        context['prompts'] = prompts_data
        context['unique_days'] = unique_days
        context['unique_hours'] = unique_hours
        context['current_day'] = day_filter
        context['current_hour'] = hour_filter

        # Add the selected day's display name if a day is selected
        if day_filter and day_filter in unique_days:
            context['selected_day_display'] = unique_days[day_filter]

        # Add the selected hour's display name if an hour is selected
        if hour_filter and hour_filter in unique_hours:
            context['selected_hour_display'] = unique_hours[hour_filter]

        return context

class FilteredPromptListView(TemplateView):
    template_name = 'pcomp/filtered_prompt_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the processed filter value from request GET parameters
        processed_filter = self.request.GET.get('processed', None)

        # Get prompts from the database
        if processed_filter is not None and processed_filter.isdigit():
            # Convert to integer and filter
            processed_value = int(processed_filter)
            prompts = Prompts.objects.filter(processed=processed_value).order_by('-date')
        else:
            # If no filter or invalid filter, show all prompts
            prompts = Prompts.objects.all().order_by('-date')
            processed_filter = None

        # Only include processed and prompt fields
        prompts_data = []
        for prompt in prompts:
            prompts_data.append({
                'id': prompt.id,
                'prompt': prompt.prompt,
                'processed': prompt.processed
            })

        # Pass the current filter to the template
        context['prompts'] = prompts_data
        context['current_filter'] = processed_filter
        return context
