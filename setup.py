from setuptools import find_packages,setup
from typing import List


REQUIRMENTS_FILE_PATH:str='requirments.txt'
DASH_E_DOT='-e .'


def get_requirments()->List[str]:
    requirments=[]
    with open(REQUIRMENTS_FILE_PATH,'r') as file:
        text=file.readlines()
        for req in text:
            req=req.replace("\n",'')
            if req != DASH_E_DOT:
                requirments.append(req)
    return requirments

setup(
    name='fakeNewsDetection',
    version='0.0.1',
    author='Rikan Maji',
    author_email='example@gmail.com',
    packages=find_packages(),
    install_requires=get_requirments()
)
