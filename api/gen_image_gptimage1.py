# gpt-image-1, low quality
# use word and definition
# remove transparent

import os
import openai
import base64
from openai import OpenAI
from collections import defaultdict
import re
import logger
import boto3
from django.conf import settings



OPENAI_API_KEY = settings.OPENAI_API_KEY
openai.api_key = OPENAI_API_KEY
openai_client = OpenAI()


def upload_file_to_public_s3(local_file_path: str, bucket_name: str, object_key: str):
    """
    Uploads a file to an S3 bucket with public read access.

    :param local_file_path: The path to the local file to upload
    :param bucket_name: The name of the S3 bucket to upload to
    :param object_key: The S3 object key (destination filename/key)

    Example usage:
        upload_file_to_public_s3("path/to/local_file.txt", "your-public-bucket", "folder/remote_file.txt")
    """
    # Create an S3 client (credentials can be handled by environment or IAM roles)
    s3_client = boto3.client("s3")

    # Upload the file with public-read ACL
    s3_client.upload_file(
        Filename=local_file_path,
        Bucket=bucket_name,
        Key=object_key,
        ExtraArgs={"ACL": "public-read"}
    )

    print(f"File '{local_file_path}' uploaded to 's3://{bucket_name}/{object_key}' with public read access.")


def gen_icon_hf(prompt: str, outpath: str):
    try:
        # Create a more specific prompt based on both word and sentence context
        response = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024",
            quality="low",  # Options: 'low','medium','high','auto'
            n=1
        )

        # image_url = response.data[0].url
        # print(f"Image {i + 1} URL: {image_url}")
        b64_image = response.data[0].b64_json

        with open(output_file, "wb") as f:
            f.write(base64.b64decode(b64_image))

        if not db.img_path_update(id, output_file):
            logger.error(f"update img_path failed for id:{id}")
            break
    except Exception as e:
        print(f"Error generating icon: {e}")


if __name__ == "__main__":
    s3_bucket_name = "generated-images-v1"
    project_root_directory = "projects"
    project_name = "unit3"
    icon_path = os.path.join(project_root_directory, project_name)
    file_key_name = os.path.join(icon_path, "generated_image.png")

    # prepare prompt for img generation
    prepare_prompt()

    # get genable list
    genable_list = get_gen_list()

    # generate icon
    gen_icon_hf(genable_list)
    print(f"icon generated")
