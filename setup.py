import platform
from setuptools import setup, find_packages
from sys import argv


import setuptools
TORCH_MAJOR = 1
TORCH_MINOR = 3
import pprint
extra_compile_args = []
if platform.system() != 'Windows':
	extra_compile_args += ['-Wno-unused-variable']

if (TORCH_MAJOR > 1) or (TORCH_MAJOR == 1 and TORCH_MINOR > 2):
	extra_compile_args += ['-DVERSION_GE_1_3']


ext_modules = [
	setuptools.Extension('torch_scatter.scatter_cpu', ['cpu/scatter.cpp'],
				 extra_compile_args=extra_compile_args)
]

def my_build_ext(pars):
	# import delayed:
	from setuptools.command.build_ext import build_ext as _build_ext#
	# include_dirs adjusted: 
	class build_ext(_build_ext):
		def __init__(self, *args, **kwargs):
			print(args, kwargs)
			self.ARGS = args
			self.KWARGS = kwargs
			super().__init__(*args, **kwargs)
		def finalize_options(self):
			_build_ext.finalize_options(self)
			pprint.pprint(self.__dict__)
			# Prevent numpy from thinking it is still in its setup process:
			# print(__builtins__.__dict__)
			__builtins__.__TORCH_SETUP__ = False

			import torch.utils.cpp_extension
			import importlib
			importlib.reload(torch)
			# print(torch.utils.cpp_extension)
			# print(dir(torch.utils))
			extensions = self.extensions
			a = torch.utils.cpp_extension.BuildExtension(*self.ARGS, **self.KWARGS)
			# self.__dict__.update(a.__dict__)
			# self.extensions = extensions
			pprint.pprint(a.__dict__)
			from torch.utils.cpp_extension import CppExtension
			b = CppExtension('torch_scatter.scatter_cpu', ['cpu/scatter.cpp'],
				extra_compile_args=extra_compile_args)
			self.include_dirs += b.include_dirs
			self.language = b.language
			pprint.pprint(self.__dict__)

	return build_ext(pars)

cmdclass = {'build_ext': my_build_ext}

GPU = False
for arg in argv:
	if arg == '--cpu':
		GPU = False
		argv.remove(arg)

# if CUDA_HOME is not None and GPU:
# 	ext_modules += [
# 		CUDAExtension('torch_scatter.scatter_cuda',
# 					  ['cuda/scatter.cpp', 'cuda/scatter_kernel.cu'])
# 	]

__version__ = '1.4.0'
url = 'https://github.com/rusty1s/pytorch_scatter'

install_requires = ['torch']
setup_requires = ['torch==1.3.1', 'pytest-runner']
tests_require = ['pytest', 'pytest-cov']
print(ext_modules)
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
	ext_modules=ext_modules,
	cmdclass=cmdclass,
	packages=find_packages(),
)
