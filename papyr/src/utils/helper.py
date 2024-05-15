import os


def create_file_path(username: str, file_path: str, filename: str) -> str:
    username = username.strip(" /\\")
    file_path = file_path.strip(" /\\")
    filename = filename.strip(" /\\")

    combined_path = os.path.join(username, file_path)

    # Check if the combined path ends in a typical file extension; if not, append the filename
    if not os.path.splitext(combined_path)[1]:
        combined_path = os.path.join(combined_path, filename)

    final_path = os.path.normpath(combined_path)
    return final_path
