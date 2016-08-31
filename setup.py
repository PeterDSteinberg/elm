import os
import glob
from setuptools import setup

import versioneer

version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()

setup(name='elm',
      version=version,
      cmdclass=cmdclass,
      description='Ensemble Learning Models',
      install_requires=[],
      packages=['elm',
                'elm.acquire',
                'elm.config',
                'elm.example_data',
                'elm.model_selection',
                'elm.pipeline',
                'elm.readers',
                'elm.sample_util',
                'elm.scripts',
                'elm.writers',
                ],
      data_files=[('elm', glob.glob(os.path.join('elm', 'examples', '*.yaml'))),
                  ('elm.acquire',
                   glob.glob(os.path.join('elm', 'acquire', 'metadata', '*'))),
                  ('elm.config',
                   glob.glob(os.path.join('elm', 'config', 'defaults', '*.yaml'))),
                  ('elm.example_data',
                    glob.glob(os.path.join('elm', 'example_configs', '*.yaml'))),
                 ],
      entry_points={
        'console_scripts': [
            'elm-main = elm.scripts.main:main',
            'elm-run-all-tests = elm.scripts.run_all_tests:run_all_tests',
        ]},)
