"""PC package for system control operations"""
from .system import (
    shutdown_pc,
    reboot_pc,
    abort_shutdown,
    lock_pc,
    sleep_pc,
    get_system_info,
    get_uptime
)
from .files import (
    list_directory,
    download_file,
    upload_file,
    create_directory,
    delete_path,
    get_directory_tree
)
from .screen import (
    take_screenshot,
    take_screenshot_area,
    take_screenshot_all_monitors
)
from .input import (
    type_text,
    press_keys,
    get_mouse_position,
    click_mouse,
    move_mouse,
    scroll_mouse,
    drag_mouse
)
from .processes import (
    get_process_list,
    kill_process
)
from .clipboard import (
    get_clipboard,
    set_clipboard
)
from .camera import (
    take_photo,
    list_cameras
)
from .audio import (
    get_volume,
    set_volume,
    mute,
    unmute
)
from .network import (
    get_network_info,
    ping,
    get_active_connections,
    get_wifi_networks
)

__all__ = [
    'shutdown_pc',
    'reboot_pc',
    'abort_shutdown',
    'lock_pc',
    'sleep_pc',
    'get_system_info',
    'get_uptime',
    'list_directory',
    'download_file',
    'upload_file',
    'create_directory',
    'delete_path',
    'get_directory_tree',
    'take_screenshot',
    'take_screenshot_area',
    'take_screenshot_all_monitors',
    'type_text',
    'press_keys',
    'get_mouse_position',
    'click_mouse',
    'move_mouse',
    'scroll_mouse',
    'drag_mouse',
    'get_process_list',
    'kill_process',
    'get_clipboard',
    'set_clipboard',
    'take_photo',
    'list_cameras',
    'get_volume',
    'set_volume',
    'mute',
    'unmute',
    'get_network_info',
    'ping',
    'get_active_connections',
    'get_wifi_networks'
]
