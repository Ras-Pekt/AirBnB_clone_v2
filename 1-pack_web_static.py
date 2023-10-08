#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive
from the contents of the web_static folder of the AirBnB Clone repo
using the function do_pack
"""

from fabric.api import local
from datetime import datetime
from os import mkdir
from os.path import exists


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
