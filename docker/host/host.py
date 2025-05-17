"""
Host Network Module

This module manages the basic network configuration for a host container.
It retrieves the host's network information and maintains an active state.
"""

import time
import socket
from typing import Tuple

def get_host_info() -> Tuple[str, str]:
    """
    Retrieve the hostname and IP address of the current host.
    
    Returns:
        Tuple[str, str]: A tuple containing (hostname, ip_address)
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return hostname, ip_address

if __name__ == "__main__":
    HOST_NAME, HOST_IP = get_host_info()
    print(f"[{HOST_NAME}] Iniciado com IP {HOST_IP}.")

    # Keep container running
    while True:
        time.sleep(1)