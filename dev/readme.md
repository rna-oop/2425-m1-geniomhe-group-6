# development utilities

<!-- want to add bade for colab, library deployment, documentation, submission, version  -->
![badge](https://img.shields.io/badge/test-i-brightgreen.svg)

## library setup

required utils:
- [x] requirements.txt
- [ ] setup.py
- [ ] library directory in the root of the repo

after this, you can install the library using pip (dev installation, updates dynamically)
```bash
pip install -e .
```

### pythonpath - import issue

`set-pythonpath.sh` is a script that adds a directory to the python path for the current shell session, useful for developing libraries that are not installed in the system python path

_e.g. adds `lab2/src` to the python path for the current shell session_
```bash
source dev/set-pythonpath.sh lab2/src
```
### library name change

Chanin library name requires changing its name from all imports inside its modules, this script will do that for you
```bash
./dev/change-libname.sh #--will ask u to enter path to the library and name directly on terminal
```

### versioning

- [ ] `__VERSION__` file in root
- [ ] CHANGELOG.md

updating version using the script
```bash
./dev/update-version.sh #--will ask u to enter one of the following: major, minor, patch (x.y.z format where x is major, y is minor and z is patch)
```
