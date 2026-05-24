import base64
import mimetypes
import os

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
EXT_TO_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}
MAX_FILE_SIZE = 20 * 1024 * 1024


def get_mime_type(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    mime = EXT_TO_MIME.get(ext)
    if mime is None:
        raise ValueError(
            f"Unsupported image format: {ext}. "
            f"Supported formats: PNG, JPEG, GIF, WebP"
        )
    return mime


def validate_image_path(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Image file not found: {file_path}")

    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Image file not readable: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported image format: {ext}. "
            f"Supported formats: PNG, JPEG, GIF, WebP"
        )

    size = os.path.getsize(file_path)
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"Image file too large: {size} bytes (max {MAX_FILE_SIZE} bytes)"
        )

    return get_mime_type(file_path)


def encode_image(file_path: str) -> str:
    mime_type = validate_image_path(file_path)
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"
