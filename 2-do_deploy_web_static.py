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


def do_pack():
    """
    Generates a .tgz archive from the web_static folder
    """
    if not exists("versions"):
        mkdir("versions")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"

    result = local(f"tar -cvzf {archive_path} web_static")

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
        # /tmp/versions/web_static_20170315003959.tgz
        put(archive_path, '/tmp/')

        # archive_filename=web_static_20170315003959.tgz
        archive_filename = archive_path.split("/")[-1]

        # archive_name=web_static_20170315003959
        archive_name = archive_filename.split(".")[0]

        # path=/data/web_static/releasses/web_static_20170315003959
        path = f"/data/web_static/releases/{archive_name}"

        # make this dir(and parent_dir)
        # /data/web_static/releasses/web_static_20170315003959
        run(f"mkdir -p {path}")

        # extract /tmp/versions/web_static_20170315003959.tgz
        # to /data/web_static/releasses/web_static_20170315003959
        run(f"tar -xzf /tmp/{archive_filename} -C {path}")

        # delete /data/web_static/releasses/web_static_20170315003959
        run(f"rm /tmp/{archive_filename}")

        # remove symlink
        run("rm -rf /data/web_static/current")

        # create sysnlink
        run(f"ln -s {path} /data/web_static/current")

        return True

    except Exception as e:
        return False
