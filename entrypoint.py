#!/usr/bin/python
import os
import urllib.request
import re
from xml.dom import minidom


def version_regex(_suffix):
    return rf"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)-{_suffix}([0-9]\d*)$"


def is_debug():
    return os.getenv("INPUT_DEBUG", "false").casefold() == "true".casefold()


def github_output(key, value):
    with open(os.environ['GITHUB_OUTPUT'], mode='a', encoding='UTF-8') as fh:
        print(f'{key}={value}', file=fh)


url = "https://dl.google.com/android/maven2/com/android/tools/build/gradle/maven-metadata.xml"
stable_regex = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
alpha_regex = re.compile(version_regex("alpha"))
beta_regex = re.compile(version_regex("beta"))
rc_regex = re.compile(version_regex("rc"))

with urllib.request.urlopen(url) as response:
    xml = response.read()
    root_tag = minidom.parseString(xml)
    versions = [elem.firstChild.data for elem in root_tag.getElementsByTagName("version")]

all_stable = [s for s in versions if stable_regex.match(s)]
all_alpha = [s for s in versions if alpha_regex.match(s)]
all_beta = [s for s in versions if beta_regex.match(s)]
all_rc = [s for s in versions if rc_regex.match(s)]

if is_debug():
    print(f"""
        Found:
            all_count={len(versions)}, 
            stable_count={len(all_stable)}, 
            alpha_count={len(all_alpha)}, 
            beta_count={len(all_beta)},
            rc_count={len(all_rc)}
        """)

latest_stable = all_stable[-1]
latest_alpha = all_alpha[-1]
latest_beta = all_beta[-1]
latest_rc = all_rc[-1]

version_to_resolve = os.getenv("INPUT_VERSION_TO_RESOLVE", "")
if version_to_resolve in ["stable", "current"]:
    resolved_version = latest_stable
elif version_to_resolve == "alpha":
    resolved_version = latest_alpha
elif version_to_resolve == "beta":
    resolved_version = latest_beta
elif version_to_resolve in ["release-candidate", "rc"]:
    resolved_version = latest_rc
else:
    resolved_version = ""

github_output(key="latest-stable", value=latest_stable)
github_output(key="latest-alpha", value=latest_alpha)
github_output(key="latest-beta", value=latest_beta)
github_output(key="latest-rc", value=latest_rc)
github_output(key="resolved-version", value=resolved_version)
