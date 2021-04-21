from setuptools import setup, find_namespace_packages

test_deps = ["pytest"]

setup(name="psutils",
      package_dir={"": "src"},
      packages=find_namespace_packages(where="src"),
      python_requires='>=3.7',
      extras_require={
        "test": test_deps,
      }
)