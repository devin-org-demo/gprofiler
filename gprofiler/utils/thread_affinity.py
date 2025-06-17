#
#
#
#
#

import errno
import os
from typing import Set

from gprofiler.log import get_logger_adapter

logger = get_logger_adapter(__name__)


def set_thread_affinity(pid: int, cpu_mask: Set[int]) -> bool:
    """
    Set CPU affinity for a thread/process and log permission errors.
    
    This function wraps the sched_setaffinity() system call and provides
    explicit logging for permission errors that might occur when setting
    thread affinity.
    
    Args:
        pid: Process/thread ID to set affinity for
        cpu_mask: Set of CPU IDs to restrict the process/thread to
        
    Returns:
        bool: True if affinity was set successfully, False if permission error occurred
        
    Raises:
        OSError: For non-permission related errors (e.g., invalid PID, invalid CPU mask)
    """
    try:
        os.sched_setaffinity(pid, cpu_mask)
        logger.debug("Successfully set thread affinity", pid=pid, cpu_mask=sorted(cpu_mask))
        return True
    except OSError as e:
        if e.errno == errno.EPERM:
            logger.warning(
                "Permission denied when setting thread affinity",
                pid=pid,
                thread_id=pid,  # In Linux, thread ID is the same as PID for the thread
                error_code=e.errno,
                error_message=e.strerror,
                cpu_mask=sorted(cpu_mask),
            )
            return False
        else:
            logger.error(
                "Unexpected error when setting thread affinity",
                pid=pid,
                error_code=e.errno,
                error_message=e.strerror,
                cpu_mask=sorted(cpu_mask),
                exc_info=True,
            )
            raise
