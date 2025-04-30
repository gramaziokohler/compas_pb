
def install():
    """Install and set up the compas_timber_pb package."""
    from .plugin import plugin_setup
    plugin_setup()
    print("compas_timber_pb has been successfully installed and set up!")

if __name__ == "__main__":
    install()
