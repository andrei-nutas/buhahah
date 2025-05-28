import subprocess
import sys

def run_all_api_tests():
    sys.exit(subprocess.call(["pytest"]))

def run_workflow_tests():
    sys.exit(subprocess.call(["pytest", "-m", "workflow"]))

def run_non_workflow_tests():
    sys.exit(subprocess.call(["pytest", "-m", "not workflow"]))
