#!/usr/bin/env python

import logging
import os
import shutil
import subprocess
import datetime
import argparse
from threading import Thread
from datetime import datetime
from sys import exit
from time import sleep
from queue import Queue

logger = logging.getLogger("logger")

logger.setLevel(logging.INFO)


# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter(
    "%(asctime)s:%(levelname)s > %(message)s", "%Y-%m-%d %H:%M:%S"
)
# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class NetinstallAuditor:
    def __init__(self, log_name, search_term):

        self.search_term = None
        self.search_results = []

        if search_term is not None:
            self.search_term = search_term
            logger.info(f"Searching for package {self.search_term}")

        self.log_dir = f"/home/{os.getlogin()}/arcolinux-netinstall-explorer"

        logger.info(f"Creating log directory {self.log_dir}")
        os.makedirs(self.log_dir, exist_ok=True)

        self.filename = (
            f"{self.log_dir}/{datetime.now().strftime('%Y%m%d%H%M%S')}-{log_name}.txt"
        )

        self.log_file = open(
            self.filename,
            "w",
            encoding="utf-8",
        )
        self.log_file.write(f"####### {log_name} package log #######\n")

    def clone_repo(self, repo, dest):
        logger.info(f"Git clone = {repo}")
        logger.info(f"Destination = {dest}")
        clone_cmd = ["git", "clone", repo, dest]
        try:
            if os.path.exists(dest):
                logger.info(f"Removing previous directory {dest}")

                shutil.rmtree(dest, ignore_errors=True)

            process = subprocess.run(
                clone_cmd,
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=60,
                universal_newlines=True,
            )

            if process.returncode == 0:
                logger.info("Git clone successful")
                return 0
            else:
                logger.error("Failed to git clone repo")
                return 1
        except Exception as e:
            logger.error(f"Failed to git clone repo: {e}")

            return 1

    def process_files(self, path):
        category = None
        total = 0

        for file in os.listdir(path):
            if "netinstall-" in file and file.endswith(".yaml"):
                filename = os.path.join(path, file)
                # logger.info(f"Verifying file {file}")
                if len(filename) > 0:
                    packages = []
                    with open(filename, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    category = os.path.basename(filename.replace(".yaml", "").strip())

                    for line in lines:
                        if line.startswith("    - "):
                            name = line.split("    - ")[1].strip()
                            if name not in packages:
                                if self.search_term is not None:
                                    if self.search_term in name:
                                        self.search_results.append(
                                            Package(name, category)
                                        )
                                packages.append(name)

                    self.log_file.write(
                        f"####### {category.upper()} ({len(packages)}) #######\n"
                    )
                    logger.info(f"Category = {category} | Packages = {len(packages)}")
                    total += len(packages)

                    if total > 0:
                        for package in packages:
                            self.log_file.write(f" - {package}\n")

        print(
            "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        )
        logger.info(f"Packages total = {total}")
        logger.info(f"File = {self.filename}")


class Package:
    def __init__(self, name, category):
        self.name = name
        self.category = category


def main():
    parser = argparse.ArgumentParser(
        prog="Calamares Netinstall package explorer",
        description="Output a list of packages from Calamares netinstall YAML files",
    )

    parser.add_argument(
        "--config",
        help="Choose from: arcopro-calamares-config, arconet-calamares-config, arcoplasma-calamares-config",
    )

    parser.add_argument(
        "--find",
        help="Find package name",
    )

    args = parser.parse_args()

    if args.config is not None:

        # clone the calamares-config repo for netinstall files

        if args.find is not None:
            netinstall_auditor = NetinstallAuditor(args.config, args.find.lower())
        else:
            netinstall_auditor = NetinstallAuditor(args.config, None)
        arco_git = f"https://github.com/arconetpro/{args.config}.git"
        dest = "/tmp/arco-calamares-config"

        ret = netinstall_auditor.clone_repo(arco_git, dest)

        if ret == 0:
            netinstall_auditor.process_files(f"{dest}/calamares/modules")

            if (
                netinstall_auditor.search_term is not None
                and len(netinstall_auditor.search_results) > 0
            ):
                print(
                    f" ########################## Search results ({len(netinstall_auditor.search_results)}) ##########################"
                )

                for package in netinstall_auditor.search_results:
                    print(
                        f" - Package = {package.name} | Category = {package.category}"
                    )
                print(
                    " ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                )
            elif netinstall_auditor.search_term is not None:
                print(
                    f" ########################## Search results ({len(netinstall_auditor.search_results)}) ##########################"
                )
                print(f" - No results found for {netinstall_auditor.search_term}")

                print(
                    " ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                )
            else:
                print(
                    "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
                )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
