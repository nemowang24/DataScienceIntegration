from django.views.generic import TemplateView
import boto3
from api.models import Prompts
from django.conf import settings
from django.db.models import Q

class PromptInputView(TemplateView):
    template_name = 'pcomp/prompt_input.html'

class PromptListView(TemplateView):
    template_name = 'pcomp/prompt_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get all prompts from the database
        prompts = Prompts.objects.all()

        # Create S3 client
        s3_client = boto3.client('s3')

        # Generate presigned URLs for each prompt's image
        prompts_with_images = []
        for prompt in prompts:
            # Generate a presigned URL for the image (valid for 1 hour)
            image_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_S3_BUCKET_NAME, 'Key': prompt.img_path},
                ExpiresIn=3600
            )

            prompts_with_images.append({
                'prompt': prompt.prompt,
                'image_url': image_url,
                'model': prompt.model,
                'resolution': prompt.resolution,
                'quality': prompt.quality,
                'note': prompt.note,
                'date': prompt.date
            })

        context['prompts'] = prompts_with_images
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
            prompts = Prompts.objects.filter(processed=processed_value)
        else:
            # If no filter or invalid filter, show all prompts
            prompts = Prompts.objects.all()
            processed_filter = None

        # Only include processed and prompt fields
        prompts_data = []
        for prompt in prompts:
            prompts_data.append({
                'prompt': prompt.prompt,
                'processed': prompt.processed
            })

        # Pass the current filter to the template
        context['prompts'] = prompts_data
        context['current_filter'] = processed_filter
        return context
