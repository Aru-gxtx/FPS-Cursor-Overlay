import os
import shutil
import subprocess
import sys
import tempfile


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RELEASE_DIR = os.path.join(ROOT_DIR, "release")
BUILD_DIR = os.path.join(RELEASE_DIR, "build")
LEGACY_WORK_DIR = os.path.join(RELEASE_DIR, ".pyinstaller-work")
EXCLUDED_MODULES = [
    "idlelib",
    "lib2to3",
    "doctest",
    "unittest",
    "pydoc_data",
    "turtledemo",
    "tkinter.test",
    "tkinter.tix",
    "numpy",
    "pandas",
    "scipy",
    "matplotlib",
    "IPython",
    "jupyter",
    "notebook",
    "torch",
    "tensorflow",
    "cv2",
    "skimage",
    "seaborn",
]


def run_pyinstaller(script_name, dist_path, work_path, exe_name):
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconsole",
        "--onefile",
        "--clean",
        "--name",
        exe_name,
        "--distpath",
        dist_path,
        "--workpath",
        work_path,
    ]
    for module_name in EXCLUDED_MODULES:
        command.extend(["--exclude-module", module_name])
    command.append(os.path.join(ROOT_DIR, script_name))
    subprocess.run(command, check=True)


def copy_tree(source, target):
    if os.path.exists(target):
        shutil.rmtree(target)
    shutil.copytree(source, target)


def main():
    os.makedirs(RELEASE_DIR, exist_ok=True)
    shutil.rmtree(LEGACY_WORK_DIR, ignore_errors=True)
    os.makedirs(BUILD_DIR, exist_ok=True)
    work_dir = tempfile.mkdtemp(prefix="cursorrg-pyinstaller-")

    try:
        run_pyinstaller("run.py", RELEASE_DIR, os.path.join(work_dir, "run"), "run")
        run_pyinstaller("cursorrg.py", BUILD_DIR, os.path.join(work_dir, "cursorrg"), "cursorrg")

        copy_tree(os.path.join(ROOT_DIR, "icons"), os.path.join(BUILD_DIR, "icons"))
        shutil.copy2(os.path.join(ROOT_DIR, "save.txt"), os.path.join(BUILD_DIR, "save.txt"))
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)


if __name__ == "__main__":
    main()