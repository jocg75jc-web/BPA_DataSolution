from __future__ import annotations

from typing import Any

try:
    from .base import BaseExtractor
    from .onnet import ONNETExtractor
    from .titania import TitaniaExtractor
except ImportError:
    from extractors.base import BaseExtractor
    from extractors.onnet import ONNETExtractor
    from extractors.titania import TitaniaExtractor


class ExtractorRegistry:
    """Maps extractor ids to concrete extractor classes."""

    _registry: dict[str, type[BaseExtractor]] = {
        "titania": TitaniaExtractor,
        "onnet": ONNETExtractor,
    }

    @classmethod
    def register(cls, extractor_id: str, extractor_cls: type[BaseExtractor]) -> None:
        cls._registry[extractor_id.lower()] = extractor_cls

    @classmethod
    def create(cls, extractor_id: str, project_definition: dict[str, Any]) -> BaseExtractor:
        key = extractor_id.lower()
        extractor_cls = cls._registry.get(key)
        if extractor_cls is None:
            raise ValueError(f"Extractor not registered: {extractor_id}")
        return extractor_cls(project_definition)
