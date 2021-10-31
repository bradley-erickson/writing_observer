import os.path

import yaml

creds = yaml.safe_load(open("settings/CREDS.YAML"))


def config_filename(machine_name, file_suffix, create=False):
    '''
    Search for the name of a config file, checking
    * Per-machine config
    * System-wide defaults
    * Defaults for this for the Learning Observer (defined in this repo)

    Absolute paths (e.g. beginning with '/') are returned as-is.
    '''
    if file_suffix.startswith("/"):
        return file_suffix

    paths = [
        # First, we try per-machine configuration
        os.path.join(
            creds["flock-config"], "config", machine_name, file_suffix
        ),
        # Next, we try the per-machine override
        os.path.join(
            creds["flock-config"], "config", machine_name, file_suffix+".base"
        ),
        # Then, system-wide configuration
        os.path.join(
            creds["flock-config"], "config", file_suffix
        ),
        # And finally, as a fallback, default files
        os.path.join(
            "config", file_suffix
        )
    ]

    # For making new versions, always return the per-machine git repo
    # directory
    if create == True:
        return paths[0]

    for fn in paths:
        print(fn)
        if os.path.exists(fn):
            return fn


def config_lines(machine_name, file_suffix):
    '''
    Kind of like a smart `open().readlines()` for reading config files.

    Handle paths, prefixes, missing files (return nothing),
    `strip()`ing lines, comments, etc.
    '''
    fn = config_filename(machine_name, file_suffix)
    # No config file
    if fn is None:
        print("Skipping; no file for: ", file_suffix)
        return
    print("Config file: ", fn)
    for line in open(fn).readlines():
        line = line.strip()
        if len(line) > 0:
            yield line
