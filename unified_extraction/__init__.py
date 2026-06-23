"""
BPA_DataSolution - Unified Extraction Engine

Ecosistema parametrizable para la extracción, transformación y distribución de datos.
"""

__version__ = "0.1.0-alpha"
__author__ = "Data Engineering Team"

from .core import (
    ConfigLoader,
    ExecutionEngine,
    ParameterValidator,
)
from .extractors import ExtractorRegistry

__all__ = [
    "ConfigLoader",
    "ExecutionEngine",
    "ParameterValidator",
    "ExtractorRegistry",
]
