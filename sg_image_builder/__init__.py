from importlib.resources import files

# The `version` file holds the human / git-tag form, e.g. "v0.0.1".
# Read via importlib.resources so it works both on disk and inside a zipapp
# (principle P20). Strip the leading "v" for PEP 440, which setuptools'
# dynamic version expects.
version_raw = files(__name__).joinpath('version').read_text().strip()
version = version_raw  # human form, e.g. "v0.0.1"
__version__ = version_raw.lstrip('v')  # PEP 440 form, e.g. "0.0.1"
