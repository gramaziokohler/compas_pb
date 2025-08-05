from contextlib import contextmanager


@contextmanager
def open_file(file_or_filename, mode="rb"):
    """Context-manager to open a file, path or URL and return a corresponding file object.

    Parameters
    ----------
    file_or_filename : path-like, file-like object or URL string
        A path-like, a file-like object or a URL pointing to a file.
    mode : str, optional
        Specifies the mode in which the file is opened. It defaults to ``'rb'`` which means
        open for reading in binary mode.

    Yields
    -------
    file-like object
        File object already opened.
    """

    close_file = False

    if isinstance(file_or_filename, str):
        # If the file is a string, assume it's a file path
        file = open(file_or_filename, mode)
        close_file = True
    elif hasattr(file_or_filename, "read"):
        # If it's already a file-like object, use it directly
        file = file_or_filename
    else:
        # If the file is not a file-like object or string, raise an error
        raise ValueError("file_or_filename must be a path-like or file-like object")

    try:
        yield file
        print("File Path read/write:", file_or_filename)
    finally:
        if close_file:
            file.close()
            print("File closed")
