import cloudinary
import cloudinary.uploader
import cloudinary.api
import base64
import tempfile
import os

# Configuración de Cloudinary
cloudinary.config(
    cloud_name="doe5urc8k",
    api_key="744776625568778",
    api_secret="budMRbCvM9LwdCGY1jCgspCg5NU",
)
_folder = "students"


class CloudinaryHelper:

    @staticmethod
    def upload_image(photo_data, folder=_folder):
        # Decode the Base64 string
        decoded_image = base64.b64decode(photo_data)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(decoded_image)
            temp_file_path = temp_file.name

        try:
            # Upload the image to Cloudinary
            result = cloudinary.uploader.upload(temp_file_path, folder=folder)
            return result.get("secure_url")
        finally:
            # Delete the temporary file
            os.remove(temp_file_path)
            

    @staticmethod
    def delete_image(photo_url, folder=_folder):
        # Extract the public_id from the Cloudinary URL
        public_id = photo_url.split("/")[-1].split(".")[0]
        # Delete the image from Cloudinary
        cloudinary.uploader.destroy(f"{folder}/{public_id}")

    
    

