import os


def clean_path(path: str) -> str:
    """
    Cleans a Unix-like file path string by normalizing it.

    :param path: The Unix-like file path to be cleaned.
    :type path: str
    :return: The cleaned and normalized file path.
    :rtype: str
    """
    if not isinstance(path, str):
        raise ValueError("Path must be a string")
    return os.path.normpath(path)
