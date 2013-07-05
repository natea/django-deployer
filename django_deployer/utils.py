import git
import uuid
import os

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

def get_template_filelist(repo_path):
    """
    input: local repo path
    output: path list of files which need to be rendered
    """
    ignoring_files = ['.gitignore']
    ignoring_folders = ['.git']

    filelist = []

    for root, folders, files in os.walk(repo_path):
        for ignoring_file in ignoring_files:
            if ignoring_file in files:
                files.remove(ignoring_file)

        for ignoring_folder in ignoring_folders:
            if ignoring_folder in folders:
                folders.remove(ignoring_folder)

        for file_name in files:
            filelist.append( '%s/%s' % (root, file_name))

    return filelist


def render_from_repo(repo_path, to_path, template_params):
    """
    rendering all files into the target directory
    """
    repo_path = repo_path.rstrip('/')
    to_path = to_path.rstrip('/')
    files_to_render = get_template_filelist(repo_path)

    for single_file_path in files_to_render:
        source_file_path = single_file_path
        dest_file_path = source_file_path.replace(repo_path, to_path)

        render_from_single_file(source_file_path, dest_file_path, template_params)

def render_from_single_file(file_path, dest_file_path, template_params):
    from jinja2 import Template
    import os
    dest_dirname = os.path.dirname(dest_file_path)
    if not os.path.exists(dest_dirname):
        os.makedirs(dest_dirname)

    with open(file_path) as source_file_p:
        template = Template(source_file_p.read())
        rendered_content = template.render(**template_params)

    with open(dest_file_path, 'w') as dest_file_p:
        dest_file_p.write(rendered_content)


