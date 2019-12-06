import platform
from setuptools import setup, find_packages
from sys import argv
import setuptools

TORCH_MAJOR = 1
TORCH_MINOR = 3

extra_compile_args = []
if platform.system() != 'Windows':
    extra_compile_args += ['-Wno-unused-variable']

if (TORCH_MAJOR > 1) or (TORCH_MAJOR == 1 and TORCH_MINOR > 2):
    extra_compile_args += ['-DVERSION_GE_1_3']


def ext_modules_lazy():
    # from torch.utils.cpp_extension import CppExtension
    yield MyExtension('torch_scatter.scatter_cpu', ['cpu/scatter.cpp'],
        extra_compile_args=extra_compile_args)
    #'torch_scatter.scatter_cpu', ['cpu/scatter.cpp'],
    #        


class MyExtension(setuptools.extension.Extension):
    def __init__(self, *args, **kwargs):
        super(MyExtension, self).__init__(*args, **kwargs)
        self.ARGS = args
        self.KWARGS = kwargs
    def __getattribute__(self, x):
        print(x)
        if x in ("ARGS", "KWARGS", "_convert_pyx_sources_to_lang"):
            return super(MyExtension, self).__getattribute__(x)
        try:
            from torch.utils.cpp_extension import CppExtension
        except:
            return ""
        try:
            return CppExtension(*self.ARGS, **self.KWARGS).__getattribute__(x)
        except:
            return ""
from setuptools.command.build_ext import build_ext
class MyExtension2(build_ext):
    def __init__(self, *args, **kwargs):
        super(MyExtension2, self).__init__(*args, **kwargs)
        self.ARGS = args
        self.KWARGS = kwargs
    def __getattribute__(self, x):
        print(x)
        if x in ("ARGS", "KWARGS", "initialize_options", "ensure_finalized", "__dict__"):
            return super(MyExtension2, self).__getattribute__(x)
        try:
            from torch.utils.cpp_extension import BuildExtension
        except:
            return ""
        try:
            return BuildExtension(*self.ARGS, **self.KWARGS).__getattribute__(x)
        except:
            return ""

def cmd_class_lazy():
    yield 'build_ext', MyExtension2



GPU = False

__version__ = '1.4.0'
url = 'https://github.com/rusty1s/pytorch_scatter'

install_requires = ['torch']
setup_requires = ['pytest-runner']
tests_require = ['pytest', 'pytest-cov']

setup(
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
)
