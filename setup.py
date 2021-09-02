# ~/usr/bin/env python

import setuptools
from pathlib import Path

requirements_file = Path("requirements.txt")
with requirements_file.open() as reqs:
    requirements = (reqs.readlines(),)

test_requirements_file = Path("test_requirements.txt")
with test_requirements_file.open() as test_reqs:
    test_requirements = (test_reqs.readlines(),)

if __name__ == "__main__":
    setuptools.setup(
        install_requires=requirements,
        entry_points={
            "console_scripts": [
                "sumple_api = sumple_api.app:app.run",
            ]
        },
        extras_require={"test": test_requirements},
    )
