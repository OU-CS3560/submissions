# submissions

An abstraction of the root directory of the student submissions and a set of common operations on students' submission.

## Specification

This package must solve the following problems

- TA want to see the content of certain file in the submission. The file may be in a nested archive file.
- No standard method to perform action over each submission.

### End-user scenarios

```python
from submissions import Submissions

s = Submissions.from_archive("~/Downloads/blackboard-gradebook.zip", "~/cs3560/submissions/hw2")
```

```python
from submissions import Submissions, find_makefiles

s = Submissions("~/cs3560/submissions/hw2")
makefiles = s.map(find_makefiles)
```

```python
from pathlib import Path
from submissions import Submissions

def get_bb_text_submission(submission_root: Path) -> str:
    pass

s = Submissions("~/cs3560/submissions/hw2")
results = s.map(get_bb_text_submission)
```

```python
from submissions import Submissions

s = Submissions("~/cs3560/submissions/hw2")
s.map_shell_command("cookiecutter --no-input ~/cs3560/cookiecutters/hw2-grading-workspace")
```

```python
from pathlib import Path
from shutil import copyfile
import subprocess
from submissions import Submissions, find_makefiles

def create_grading_workspace(path: Path) -> None:
    handle = Submissions.get_handle(path)
    subprocess.run("cookiecutter --no-input ~/cs3560/cookiecutters/hw2-grading-workspace", shell=True, cwd=str(path))

    makefiles = find_makefiles(path)
    for f in makefiles:
        copyfile(str(f), Path("grading-workspace") / f.name)

s = Submissions("~/cs3560/submissions/hw2")
s.map(create_grading_workspace)
```

## Development Note

Install flit. Then the package can be built with the following command.

```console
flit build
```

### Development Installation

```console
flit install -s
```
