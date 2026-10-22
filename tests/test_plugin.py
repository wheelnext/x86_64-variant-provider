from __future__ import annotations

from argparse import Namespace

import pytest

from x86_64_variant_provider.plugin import VariantFeatureConfig
from x86_64_variant_provider.plugin import X8664Plugin
from x86_64_variant_provider.plugin import archspec_cpu
from variantlib.models.variant import VariantProperty


@pytest.fixture
def plugin() -> X8664Plugin:
    return X8664Plugin()


def test_bulldozer_configs(mocker, plugin):
    mocker.patch(
        "x86_64_variant_provider.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["bulldozer"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("level", ["v2", "v1"]),
    ]


def test_sandybridge_configs(mocker, plugin):
    mocker.patch(
        "x86_64_variant_provider.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["sandybridge"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("level", ["v2", "v1"]),
    ]


def test_generic_configs(mocker, plugin):
    mocker.patch(
        "x86_64_variant_provider.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["x86_64_v2"]
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("level", ["v2", "v1"]),
    ]


def test_non_x86_configs(mocker, plugin):
    mocker.patch(
        "x86_64_variant_provider.plugin.archspec_cpu.host"
    ).return_value = archspec_cpu.TARGETS["cortex_a72"]
    assert plugin.get_supported_configs() == []


def test_get_compiler_flags(plugin):
    assert plugin.get_compiler_flags(
        "c",
        "gcc",
        "14.3.0",
        [
            VariantProperty("x86_64", "level", "v2"),
        ],
    ) == ["-march=x86-64-v2"]


def test_get_compiler_flags_no_level(plugin):
    assert (
        plugin.get_compiler_flags(
            "c++",
            "clang",
            "20.1.8",
            [
            ],
        )
        == []
    )


def test_get_compiler_flags_no_properties(plugin):
    assert plugin.get_compiler_flags("c", "clang", "19.1.7", []) == []


def test_level_cap(mocker, plugin):
    """Test that we do not return level higher than declared supported"""

    mocker.patch(
        "x86_64_variant_provider.plugin.archspec_cpu.host"
    ).return_value = Namespace(generic=Namespace(name="x86_64_v6"))
    assert plugin.get_supported_configs() == [
        VariantFeatureConfig("level", ["v4", "v3", "v2", "v1"]),
    ]
