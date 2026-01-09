import os
import sys

libs_path = os.path.join(os.path.dirname(__file__))
sys.path.insert(0, libs_path)
base_path = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, base_path)
