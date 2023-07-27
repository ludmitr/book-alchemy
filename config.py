import os


def get_absolute_db_uri():
    data_base = "sqlite"
    # Get absolute path of the database directory
    database_dir = os.path.abspath(os.path.dirname(__file__))

    # Path to the SQLite file
    database_file_path = os.path.join(database_dir, 'data', 'library.sqlite')

    return data_base +":///" + database_file_path


def abs_path_templates_folder():
    return get_absolute_path_to_project_folder_folders('templates')

def abs_path_static_folder():
    return get_absolute_path_to_project_folder_folders('static')

def get_absolute_path_to_project_folder_folders(folder_name: str):
    project_folder_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(project_folder_path, folder_name)
