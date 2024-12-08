import re

_SEM_VER_RE = re.compile(
    r'^v?(?P<major>0|[1-9]\d*)'           # major version
    r'\.(?P<minor>0|[1-9]\d*)'            # minor version
    r'\.(?P<patch>0|[1-9]\d*)'            # patch version
    r'(?:-(?P<prerelease>'                # pre-release version (optional)
    r'(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)'
    r'(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*'
    r'))?'
    r'(?:\+(?P<build>'                    # build metadata (optional)
    r'[0-9a-zA-Z-]+'
    r'(?:\.[0-9a-zA-Z-]+)*'
    r'))?$'
)

def _version_str_to_int(s):
    return int(s.lstrip('0')) if s != '0' else 0


def bump_version(current_version: str, incr: str) -> str:
    if not _SEM_VER_RE.match(current_version):
        raise ValueError

    major, minor, patch = map(_version_str_to_int, current_version.split('.'))
    if incr == 'main':
        return f'{major + 1}.0.0'
    elif incr == 'minor':
        return f'{major}.{minor + 1}.0'
    elif incr == 'patch':
        return f'{major}.{minor}.{patch + 1}'
    raise ValueError
