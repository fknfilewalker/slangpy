# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception

import sys
import pytest
import slangpy as spy
from slangpy import platform


def test_platform():
    assert platform.display_scale_factor() > 0


def test_paths():
    assert platform.executable_path().exists()
    assert platform.executable_directory() == platform.executable_path().parent
    assert platform.executable_name() == platform.executable_path().name
    assert platform.app_data_directory().parent.exists()
    assert platform.home_directory().exists()
    assert platform.project_directory().exists()
    assert platform.runtime_directory().exists()
    assert any(
        [
            (platform.runtime_directory() / x).exists()
            for x in ["sgl.dll", "libsgl.so", "libsgl.dylib"]
        ]
    )


def test_memory():
    assert platform.page_size >= 4096

    stats = platform.memory_stats()
    assert stats.rss > 0
    assert stats.peak_rss > 0


@pytest.mark.skipif(sys.platform != "linux", reason="Wayland handles are Linux only")
def test_window_handle_wayland():
    assert isinstance(spy.WindowHandle(wayland_display=1, wayland_surface=2), spy.WindowHandle)
    assert isinstance(spy.WindowHandle(xdisplay=1, xwindow=2), spy.WindowHandle)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
