import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.fixture
def mcp_instance():
    from vision_mcp.server import mcp
    return mcp


@pytest.fixture
def mock_encode_image():
    with patch("vision_mcp.server.encode_image") as mock:
        mock.return_value = "data:image/png;base64,mockencodeddata"
        yield mock


@pytest.fixture
def mock_call_vision_api():
    with patch("vision_mcp.server.call_vision_api") as mock:
        mock.return_value = "Mock vision API response"
        yield mock


@pytest.fixture
def mock_encode_image_error():
    with patch("vision_mcp.server.encode_image") as mock:
        mock.side_effect = FileNotFoundError("Mock file not found")
        yield mock


@pytest.fixture
def mock_call_vision_api_error():
    from vision_mcp.client import VisionAPIError

    with patch("vision_mcp.server.call_vision_api") as mock:
        mock.side_effect = VisionAPIError("Mock API error")
        yield mock
