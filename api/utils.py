from PIL import Image
from colorthief import ColorThief
from io import BytesIO
import base64


def get_contrasting_color(hex_color):
    """Returns the contrasting color for the given hex color.

    Args:
        hex_color (tuple): RGB color tuple.

    Returns:
        string: Hex color code for the contrasting color.
    """
    luminance = 0.2126 * hex_color[0] + 0.7152 * hex_color[1] + 0.0722 * hex_color[2]
    return '#000000' if luminance > 128 else '#FFFFFF'


def get_file_ids(drive_service, folder_id):
    """Retrieve the IDs of all PNG files in the specified Google Drive folder.

    Args:
        drive_service (googleapiclient.discovery.Resource): An authorized Google Drive API service instance.
        folder_id (str): The ID of the Google Drive folder to search.

    Returns:
        list: A list of file IDs for all PNG files found in the specified folder.
    """
    query = f"'{folder_id}' in parents and mimeType='image/png' and trashed=false"
    response = drive_service.files().list(q=query, fields='nextPageToken, files(id)').execute()
    file_ids = [file.get('id') for file in response.get('files', [])]
    return file_ids


def get_file_content(drive_service, file_id):
    """
    Retrieve the content of a file with the given file ID from Google Drive.

    Args:
        drive_service (googleapiclient.discovery.Resource): A Google Drive API service instance.
        file_id (str): The ID of the file to retrieve.

    Returns:
        bytes: The file content as bytes.

    Raises:
        googleapiclient.errors.HttpError: If an error occurs while retrieving the file content.
    """
    response = drive_service.files().get_media(fileId=file_id).execute()
    return response


def resize_and_compress_image(file_content):
    """Resize and compress the given image file content.

    Args:
        file_content (bytes): The file content in bytes to resize and compress.

    Returns:
        Tuple[str, str]: A tuple containing the base64-encoded image data and the dominant color in the image as a hex code.
    """
    img = Image.open(BytesIO(file_content))
    img = img.resize((1920, 1080))
    output = BytesIO()
    img.save(output, format='PNG', quality=90)
    compressed_image = output.getvalue()
    image_data = base64.b64encode(compressed_image).decode('ascii')
    color_thief = ColorThief(BytesIO(compressed_image))
    hex_color = color_thief.get_color((5))
    return image_data, hex_color
