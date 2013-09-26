import git
import uuid
import os
from jinja2 import Template

def clone_git_repo(repo_url):
    """
    input: repo_url
    output: path of the cloned repository
    steps:
        1. clone the repo
        2. parse 'site' into for templating

    assumptions:
        repo_url = "git@github.com:littleq0903/django-deployer-template-openshift-experiment.git"
        repo_local_location = "/tmp/djangodeployer-cache-xxxx" # xxxx here will be some short uuid for identify different downloads
    """
    REPO_PREFIX = "djangodeployer-cache-"
    REPO_POSTFIX_UUID = str(uuid.uuid4()).split('-')[-1]
    REPO_CACHE_NAME = REPO_PREFIX + REPO_POSTFIX_UUID
    REPO_CACHE_LOCATION = '/tmp/%s' % REPO_CACHE_NAME

    repo = git.Repo.clone_from(repo_url, REPO_CACHE_LOCATION)
    return REPO_CACHE_LOCATION

def get_template_filelist(repo_path, ignore_files=[], ignore_folders=[]):
    """
    input: local repo path
    output: path list of files which need to be rendered
    """

    default_ignore_files = ['.gitignore']
    default_ignore_folders = ['.git']

    ignore_files += default_ignore_files
    ignore_folders += default_ignore_folders

    filelist = []

    for root, folders, files in os.walk(repo_path):
        for ignore_file in ignore_files:
            if ignore_file in files:
                files.remove(ignore_file)

        for ignore_folder in ignore_folders:
            if ignore_folder in folders:
                folders.remove(ignore_folder)

        for file_name in files:
            filelist.append( '%s/%s' % (root, file_name))

    return filelist


def render_from_repo(repo_path, to_path, template_params, settings_dir):
    """
    rendering all files into the target directory
    """
    TEMPLATE_PROJECT_FOLDER_PLACEHOLDER_NAME = 'deployer_project'

    repo_path = repo_path.rstrip('/')
    to_path = to_path.rstrip('/')
    files_to_render = get_template_filelist(repo_path, ignore_folders=[TEMPLATE_PROJECT_FOLDER_PLACEHOLDER_NAME])


    # rendering generic deploy files
    for single_file_path in files_to_render:
        source_file_path = single_file_path
        dest_file_path = source_file_path.replace(repo_path, to_path)

        render_from_single_file(source_file_path, dest_file_path, template_params)

    settings_template_dir = os.path.join(repo_path, TEMPLATE_PROJECT_FOLDER_PLACEHOLDER_NAME)
    settings_files = get_template_filelist(settings_template_dir)

    # rendering settings file
    for single_file_path in settings_files:
        source = single_file_path
        dest = single_file_path.replace(settings_template_dir, settings_dir)
        render_from_single_file(source, dest, template_params)



def render_from_single_file(file_path, dest_file_path, template_params):

    dest_dirname = os.path.dirname(dest_file_path)

    if not os.path.exists(dest_dirname):
        os.makedirs(dest_dirname)

    with open(file_path) as source_file_p:
        template = Template(source_file_p.read())
        rendered_content = template.render(**template_params)

    with open(dest_file_path, 'w') as dest_file_p:
        dest_file_p.write(rendered_content)


