import platform
from setuptools import setup, find_packages
from sys import argv


TORCH_MAJOR = 1
TORCH_MINOR = 3

extra_compile_args = []
if platform.system() != 'Windows':
    extra_compile_args += ['-Wno-unused-variable']

if (TORCH_MAJOR > 1) or (TORCH_MAJOR == 1 and TORCH_MINOR > 2):
    extra_compile_args += ['-DVERSION_GE_1_3']

def ext_modules_lazy():
    try:
        from torch.utils.cpp_extension import CppExtension
        yield CppExtension('torch_scatter.scatter_cpu', ['cpu/scatter.cpp'],
                 extra_compile_args=extra_compile_args)
    except:
        pass

def cmd_class_lazy():
    yield "dummy", ""
    try:
        import torch
        yield 'build_ext', torch.utils.cpp_extension.BuildExtension
    except:
        pass


GPU = False

__version__ = '1.4.0'
url = 'https://github.com/rusty1s/pytorch_scatter'

install_requires = ['torch']
setup_requires = ['pytest-runner']
tests_require = ['pytest', 'pytest-cov']

print(setup(
    name='torch_scatter',
    version=__version__,
    description='PyTorch Extension Library of Optimized Scatter Operations',
    author='Matthias Fey',
    author_email='matthias.fey@tu-dortmund.de',
    url=url,
    download_url='{}/archive/{}.tar.gz'.format(url, __version__),
    keywords=[
        'pytorch',
        'scatter',
    ],
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    ext_modules=list(ext_modules_lazy()),
    cmdclass={x:y for x, y in cmd_class_lazy()},
    packages=find_packages(),
))
