#!/usr/bin/python
import os
import urllib.request
import re
from xml.dom import minidom


def versionRegex(_suffix):
    return rf"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)-{_suffix}([0-9]\d*)$"


def is_debug():
    return os.getenv("INPUT_DEBUG", False)


url = "https://dl.google.com/dl/android/maven2/com/android/tools/build/group-index.xml"
stable_regex = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
alpha_regex = re.compile(versionRegex("alpha"))
beta_regex = re.compile(versionRegex("beta"))
rc_regex = re.compile(versionRegex("rc"))

with urllib.request.urlopen(url) as response:
    xml = response.read()
    root_tag = minidom.parseString(xml)
    group_tag = root_tag.getElementsByTagName("com.android.tools.build")[0]
    module_tag = group_tag.getElementsByTagName("gradle")[0]
    versions = module_tag.attributes["versions"].value.split(",")

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

os.system(f"echo \"latest-stable={all_stable[-1]}\" >> $GITHUB_OUTPUT")
os.system(f"echo \"latest-alpha={all_alpha[-1]}\" >> $GITHUB_OUTPUT")
os.system(f"echo \"latest-beta={all_beta[-1]}\" >> $GITHUB_OUTPUT")
os.system(f"echo \"latest-rc={all_rc[-1]}\" >> $GITHUB_OUTPUT")
