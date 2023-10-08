#!/usr/bin/python3
"""
a Fabric script that creates and distributes an archive
to your web servers, using the function deploy
"""

from fabric.api import local, env, put, run
from datetime import datetime
from os import mkdir
from os.path import exists

env.hosts = ["54.160.123.234", "54.161.236.101"]
env.user = "ubuntu"
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    Generates a .tgz archive from the web_static folder
    """
    if not exists("versions"):
        mkdir("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(timestamp)

    result = local("tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """
    Deploys an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        archive_filename = archive_path.split("/")[-1]

        temp_path = "/tmp/{}".format(archive_filename)

        archive_name = archive_filename.split(".")[0]

        full_path = "/data/web_static/releases/{}/".format(archive_name)

        put(archive_path, temp_path)

        run("mkdir -p {}".format(full_path))

        run("tar -xzf {} -C {}".format(temp_path, full_path))

        run("rm {}".format(temp_path))

        run("mv -f {}web_static/* {}".format(full_path, full_path))

        run("rm -rf {}web_static".format(full_path))

        run("rm -rf /data/web_static/current")

        run("ln -s {} /data/web_static/current".format(full_path))

        return True

    except Exception as e:
        return False


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    else:
        return do_deploy(archive_path)


def do_clean(number=0):
    """
    deletes out-of-date archives
    """
    try:
        number = int(number)

        if number < 0:
            return

        if number == 0 or number == 1:
            number = 2
        else:
            number += 1
    except Exception as e:
        return

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
