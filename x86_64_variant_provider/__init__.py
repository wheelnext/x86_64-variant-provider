"""A wheel variant provider with properties specific to x86-64 CPUs"""

from __future__ import annotations

from .plugin import X8664Plugin

__version__ = "0.2.1"

get_supported_configs = X8664Plugin.get_supported_configs
get_all_configs = X8664Plugin.get_all_configs
get_compiler_flags = X8664Plugin.get_compiler_flags
