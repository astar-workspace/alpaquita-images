import requests
import json
import os
import argparse
from bs4 import BeautifulSoup

# Modify these if anything on the BellSoft release chain changes
CURRENT_LTS = "23"
CURRENT_EDGE = "stream"
ARCHITECTURES = ["x86_64", "aarch64"]
C_STANDARD_LIBRARIES = ["musl", "glibc"]

# Constants
LATEST_LTS = "latest_lts.json"
LATEST_STREAM = "latest_stream.json"
HISTORY_FILE = "release_history.json"

parser = argparse.ArgumentParser(
    prog="Alpaquita Linux Release Utils (ALRU)",
    description="Manages .json versioning files.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

release_type = parser.add_mutually_exclusive_group(
    required=True
)

release_type.add_argument(
    "-s",
    "--stream",
    action="store_true",
    help="Marks this version as a stream release."
)

release_type.add_argument(
    "-l",
    "--lts",
    action="store_true",
    help="Marks this version as a lts release."
)

args = parser.parse_args()


def get_stream_tag(*versions) -> str:
    numbers = [int(y) for y in versions]
    return str(max(numbers))


def get_lts_tag(ver) -> str:
    major, minor = map(int, ver.split('.'))

    if minor < 9:
        minor += 1
    else:
        minor = 0
        major += 1

    return f"{major}.{minor}"


def update_md(release):
    # Update VERSIONS.md
    versions_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'VERSIONS.md')

    with open(versions_file, "a") as v_handle:
        for stdlib in release["stdlibs"]:
            v_handle.write(
                f"- {release["version"]}-{stdlib}-{release["tag"]}:"
            )

            for arch in release["arches"]:
                v_handle.write(
                    f" {arch}={release["releases"][stdlib][arch]["tag"]}"
                )

            v_handle.write("\n")

    # Update README.md
    data = {
        "ltsv": "",
        "ltst": "",
        "edgev": "",
        "edget": "",
    }

    try:
        with open(LATEST_LTS, 'r') as file:
            content = json.load(file)

            data["ltsv"] = content["version"]
            data["ltst"] = content["tag"]
    except FileNotFoundError:
        print("LTS versioning file does not exist, skipping...")

    try:
        with open(LATEST_STREAM, 'r') as file:
            content = json.load(file)
            data["edgev"] = content["version"]
            data["edget"] = content["tag"]
    except FileNotFoundError:
        print("Edge (stream) versioning file does not exist, skipping...")

    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'README.md'), "w") as readme_f:
        with open("README.template.md", "r") as fy:
            readme_template = fy.read()

        readme_f.write(
            readme_template.format_map(
                data
            )
        )


def main():
    config: dict = vars(args)

    rel_type = "stream" if config["stream"] else "lts"
    print(f"Processing release type '{rel_type}'")

    upstream_type = CURRENT_EDGE if rel_type == "stream" else CURRENT_LTS
    latest_release_file = LATEST_STREAM if rel_type == "stream" else LATEST_LTS
    latest_hashes = {}

    history_data = None
    if os.path.isfile(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as h_handle:
            history_data = json.load(h_handle)

    # Get the latest SHA512 for both stdlibs, together with the tags
    for stdlib in C_STANDARD_LIBRARIES:
        for arch in ARCHITECTURES:
            response = requests.get(
                f"https://packages.bell-sw.com/alpaquita/{stdlib}/{upstream_type}/releases/{arch}/alpaquita-minirootfs-{upstream_type}-latest-{stdlib}-{arch}.tar.gz.sha512"
            )

            if not response.ok:
                raise ValueError(f"Failed to download latest SHA512 hash for arch {arch}, and stdlib {stdlib}")

            current_hash = response.text.split("  ")[0]
            latest_hashes.setdefault(stdlib, {}).setdefault(arch, {})["hash"] = current_hash

            if history_data is not None:
                for version in history_data:
                    if version["releases"][stdlib][arch]["hash"] == current_hash:
                        print(f"Latest tag {version["releases"][stdlib][arch]["tag"]} has already been released on {stdlib}-{arch}-{version["tag"]}")
                        return

            response = requests.get(
                f"https://packages.bell-sw.com/browse/alpaquita/{stdlib}/{upstream_type}/releases/{arch}/"
            )

            if not response.ok:
                raise ValueError(f"Failed to list releases for arch {arch}, and stdlib {stdlib}")

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a"):
                href = link.get("href")
                filename = href.split("/")[-1]
                if "latest" in filename:
                    continue

                if filename.startswith("alpaquita-minirootfs-") and href.endswith(".tar.gz.sha512"):
                    response = requests.get(href)

                    if not response.ok:
                        raise ValueError(f"Failed to download SHA512 hash for {href}")

                    potential_hash = response.text.split("  ")[0]

                    if current_hash != potential_hash:
                        continue

                    latest_hashes[stdlib][arch]["tag"] = filename.replace(
                        f"alpaquita-minirootfs-{upstream_type}-", ""
                    ).replace(
                        f"-{stdlib}-{arch}.tar.gz.sha512", ""
                    )

            if "tag" not in latest_hashes[stdlib][arch]:
                raise ValueError(f"Failed to find tag for SHA512 {current_hash}")

    release = {
        "releases": latest_hashes,
        "arches": ARCHITECTURES,
        "stdlibs": C_STANDARD_LIBRARIES
    }

    # Tag this release
    if os.path.isfile(latest_release_file):
        with open(latest_release_file, "r") as r_handle:
            release_data = json.load(r_handle)
            last_tag = release_data["tag"]

            # LTS
            if rel_type == "lts":
                release["tag"] = get_lts_tag(last_tag)
                release["version"] = CURRENT_LTS
            # Stream
            else:
                new_tag = get_stream_tag(
                    *[latest_hashes[stdlib][arch]["tag"] for stdlib in C_STANDARD_LIBRARIES for arch in ARCHITECTURES])

                # Duplicate release tag
                if last_tag[:6] == new_tag[:6]:
                    if len(last_tag) == 6:
                        new_tag = new_tag + "r1"
                    else:
                        new_tag = f"{new_tag}r{str(int(last_tag[7:]) + 1)}"

                release["tag"] = new_tag
                release["version"] = CURRENT_EDGE
    else:
        if rel_type == "lts":
            release["tag"] = "1.0"
            release["version"] = CURRENT_LTS
        else:
            release["tag"] = get_stream_tag(
                *[latest_hashes[stdlib][arch]["tag"] for stdlib in C_STANDARD_LIBRARIES for arch in ARCHITECTURES])
            release["version"] = CURRENT_EDGE

    with open(latest_release_file, "w") as f:
        json.dump(release, f)

    with open(HISTORY_FILE, "w") as x:
        if history_data is None:
            history_data = [release]
        else:
            history_data.append(release)
        json.dump(history_data, x)

    update_md(release)
    print(f"Released new tag {release["tag"]} for '{release["version"]}' image version")


if __name__ == "__main__":
    main()
