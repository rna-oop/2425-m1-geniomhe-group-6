# development utilities

<!-- want to add bade for colab, library deployment, documentation, submission, version  -->

> [!CAUTION]
> `.gitignore` is hidden, make sure to have it as a file and hide the files u want to ignore in it

## library setup

required utils:
- [x] requirements.txt
- [x] setup.py
- [x] library directory in the root of the repo

after this, you can install the library using pip (dev installation, updates dynamically) _for development purposes_
```bash
pip install -e .
```


### pythonpath - import issue

`set-pythonpath.sh` is a script that adds a directory to the python path for the current shell session, useful for developing libraries that are not installed in the system python path

_e.g. adds `lab2/src` to the python path for the current shell session_
```bash
source dev/set-pythonpath.sh lab2/src
```

no need for this if pip installed successfully

### library documentation

To document it (it uses docstrings in python files), need to have sphinx installed:
```bash
pip install -U sphinx
sphinx-quickstart 
```

Then to build the documentation run:
```bash
./dev/create-library.sh #--will ask u to enter name of the lib terminal
#need to have this library in the root of the repo
```
for instance if library is called foo, need to have a `foo/` folder in the root, and enter the "foo" when prompted on terminal.

Everytime we want to update the doc, need to run it, it will move the old doc to a backup folder in backup.

### library name change

Changing library name requires changing its name from all imports inside its modules, this script will do that for you
```bash
./dev/change-libname.sh #--will ask u to enter path to the library and name directly on terminal
```

Need to run `./dev/create-library.sh` again to recreate the documentation in docs.

### versioning

- [x] `VERSION` file in root
- [x] CHANGELOG.md

updating version using the script
```bash
./dev/update-version.sh #--will ask u to enter one of the following: major, minor, patch (x.y.z format where x is major, y is minor and z is patch)
```
