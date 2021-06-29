from setuptools import setup, find_packages
from sys import path
from os import environ

path.insert(0, '.')

NAME = "fetch_rewards_assessment"

if __name__ == "__main__":

    setup(
        name=NAME,
        version='0.0.1',
        author="Jonathan Kelley",
        author_email="jonk@uberleet.org",
        url="https://github.com/jondkelley/fetch_rewards_assessment",
        license='None',
        packages=find_packages(),
        include_package_data=True,
        package_dir={NAME: NAME},
        description="fetch_rewards_assessment - Hiring Asssessment",
        install_requires=['boto3==1.17.98', 'PyYAML==5.4.1'],
        entry_points={
            'console_scripts': ['fetch_rewards_assessment = fetch_rewards_assessment.assess:main'],
        },
        zip_safe=False,
    )