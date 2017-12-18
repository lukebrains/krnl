# DownloadKernel is used to download the kernel that is
# requested to be installed. This is downloaded by default from kernel.org.
# A separate blob storage can be configured in ./storage_config.json.

import json, os, redis, gzip

import logging
from subprocess import run as run

def check_filesystem_for_kernel(version):
    if os.path.exists("./kernels/linux-" + version + ".tar.xz"):
        return True
    else:
        return False

def download_kernel(version):
    config_file = open("./config/storage_config.json", "r+").read()
    json_config = json.loads(config_file)
    cache_client = redis.StrictRedis(host=json_config.get("redis_server").get("host"),
                                     port= json_config.get("redis_server").get("port"),
                                     db= json_config.get("redis_server").get("database"),
                                     decode_responses=True,
                                     encoding="UTF-8")
    kernel_url = json_config.get("kernel_storage") + "linux-{}.tar.xz".format(version)
    if not check_filesystem_for_kernel(version):
        download = run(["curl", "-XGET", kernel_url, "-o", "./kernels/linux-" + version + ".tar.xz"])
        if download.returncode != 0:
            logging.error("There was an error downloading the kernel.")
            return
    else:
        print("Kernel version has already been downloaded.")
    if cache_client.get("current_kernel") != version:
        cache_client.set("current_kernel", version)
    else:
        print(cache_client.get("current_kernel"))
    return

def decompress_kernel(version):
    run(["tar", "xf", "./kernels/linux-" + version + ".tar.xz"])

if __name__ == "__main__":
    # download_kernel("4.9.68")
    download_kernel("4.9.68")