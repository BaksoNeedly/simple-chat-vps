from ..managers.asset_manager import AssetManager
from simple_framework.http.response import HTTPResponse
from config import app_config

class AssetController:

    _content_types: dict[str, str] = {
        "html": "text/html",
        "css": "text/css",
        "js": "application/javascript",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "ico": "image/x-icon",
        "svg": "image/svg+xml"
    }

    @staticmethod
    def serve_response(file_name: str, directory: str|None = None, content_type: str|None = None) -> HTTPResponse:
        asset = AssetManager.serve(file_name, directory)
        name, ext = file_name.split(".", 1)
        if not content_type:
            content_type = AssetController._content_types.get(ext)
        return HTTPResponse(
            headers={
                "Content-Length": len(asset) if isinstance(asset, bytes) else len(asset.encode(app_config.ENCODING)),
                "Content-Type": content_type
            },
            body=asset
        )
        
