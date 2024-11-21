#code\backend\batch\utilities\common\source_document.py

from typing import Optional, Type
from urllib.parse import urlparse, quote
import hashlib

class SourceDocument:
    def __init__(
        self,
        content: str,
        source: str,
        offset: Optional[int] = None,
        page_number: Optional[int] = None,
    ):
        self.content = content
        self.source = source
        self.offset = offset
        self.page_number = page_number

    @classmethod
    def from_metadata(
        cls: Type["SourceDocument"],
        content: str,
        metadata: dict,
        document_url: Optional[str],
        idx: Optional[int],
    ) -> "SourceDocument":
        parsed_url = urlparse(document_url)
        file_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
        filename = parsed_url.path
        hash_key = hashlib.sha1(f"{file_url}_{idx}".encode("utf-8")).hexdigest()
        hash_key = f"doc_{hash_key}"
        sas_placeholder = (
            "_SAS_TOKEN_PLACEHOLDER_"
            if parsed_url.netloc
            and parsed_url.netloc.endswith(".blob.core.windows.net")
            else ""
        )
        return cls(
            content=content,
            source=metadata.get("source", f"{file_url}{sas_placeholder}"),
            offset=metadata.get("offset"),
            page_number=metadata.get("page_number"),
        )