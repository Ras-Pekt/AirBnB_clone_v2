#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder of the AirBnB Clone repo
using the function do_pack
"""


from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime
from os import mkdir

env.hosts = ["54.160.123.234", "54.161.236.101"]
env.user = "ubuntu"
env.key_filename = '/root/.ssh/id_rsa'


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

        run("rm /tmp/{}".format(temp_path))

        run("mv -f {}web_static/* {}".format(full_path, full_path))

        run("rm -rf {}web_static".format(full_path))

        run("rm -rf /data/web_static/current")

        run("ln -s {} /data/web_static/current".format(full_path))

        return True

    except Exception as e:
        return False
