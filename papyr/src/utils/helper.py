import os


def clean_path(path: str) -> str:
    """
    Cleans a Unix-like file path string by normalizing it.

    Parameters:
    path (str): The Unix-like file path to be cleaned.

    Returns:
    str: The cleaned and normalized file path.
    """
    if not isinstance(path, str):
        raise ValueError("Path must be a string")

    return os.path.normpath(path)
