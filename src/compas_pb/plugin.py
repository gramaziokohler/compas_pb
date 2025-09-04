import warnings
from importlib import import_module
from importlib.metadata import entry_points

DEBUG = True


def _create_logger():
    # I want to include sufficient debug printing because plugin discovery can be tricky.
    # I don't want to use logging module with NullHandler becuase this is a library and it shouldn't configure logging.
    # I don't want to use print directly because I don't want to clutter the code with if DEBUG checks.
    # I really don't want to shadow built-in print, because I'm not god

    def noop(*args, **kwargs):
        pass

    if DEBUG:
        return print
    else:
        return noop


def set_debug_mode(enabled: bool) -> None:
    """
    Enable or disable DEBUG mode and update the logger.

    Parameters
    ----------
    enabled : bool
        Whether to enable DEBUG mode
    """
    global DEBUG, LOG
    DEBUG = enabled
    LOG = _create_logger()
    if enabled:
        LOG("DEBUG mode enabled")


LOG = _create_logger()


def _import_core_serializers():
    # side-effect import: serializers get registered by the decorators
    import_module("compas_pb.conversions")


class _PluginManager:
    __INSTANCE = None

    def __init__(self):
        if _PluginManager.__INSTANCE:
            raise RuntimeError("PluginManager is a singleton!")
        _PluginManager.__INSTANCE = self

        self._auto_discovery_done = False
        self._loaded_modules = set()
        self.warn_on_missing = True

        LOG("PluginManager initialized")

    def discover_plugins(self, group: str = "compas_pb.plugins") -> None:
        if self._auto_discovery_done:
            LOG("Plugin discovery already done, skipping")
            return

        LOG("Importing core serializers")
        _import_core_serializers()

        discovered_plugins = entry_points(group=group)

        LOG(f"Found {len(discovered_plugins)} plugins in group '{group}'")
        for plugin in discovered_plugins:
            try:
                LOG(f"Loading plugin: {plugin.name}")

                plugin.load()
                self._loaded_modules.add(plugin.name)
            except Exception as e:
                LOG.error(f"Failed to load plugin {plugin.name}: {e}")

                if self.warn_on_missing:
                    warnings.warn(f"Failed to load plugin {plugin.name}: {e}", RuntimeWarning)

        self._auto_discovery_done = True
        LOG("Plugin discovery complete.")


PLUGIN_MANAGER = _PluginManager()
