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

ext_modules = [
	MyExtension('torch_scatter.scatter_cpu', ['cpu/scatter.cpp'],
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
			# Prevent numpy from thinking it is still in its setup process:
			__builtins__.__TORCH_SETUP__ = False
			import torch
			a = torch.utils.cpp_extension.BuildExtension(*self.ARGS, **self.KWARGS)
			self.__dict__.update(a.__dict__)
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
setup_requires = ['torch', 'pytest-runner']
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
	ext_modules=ext_modules,
	cmdclass=cmdclass,
	packages=find_packages(),
)
