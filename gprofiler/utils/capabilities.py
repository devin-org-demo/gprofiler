"""
Capability detection utilities for gProfiler.
"""

from gprofiler.platform import is_linux


def has_sys_ptrace_capability() -> bool:
    """Check if SYS_PTRACE capability is available for the current process."""
    if not is_linux():
        return False
    
    try:
        with open("/proc/self/status", "r") as f:
            for line in f:
                if line.startswith("CapEff:"):
                    cap_eff = int(line.split()[1], 16)
                    return bool(cap_eff & (1 << 19))
    except (OSError, IOError, ValueError, IndexError):
        return False
    
    return False
