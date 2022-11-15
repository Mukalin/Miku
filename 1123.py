import os,sys,time
from IPython.utils import capture
from IPython.display import clear_output
from IPython.display import HTML
from subprocess import getoutput


Fast_Install_Dependencies=True #@param {type:"boolean"}

%cd /content/
if Fast_Install_Dependencies and '3.7' in sys.version:
  with capture.capture_output() as cap:
    !wget -O Dependencies_AUT.7z.001 https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dependencies/Dependencies_AUT.1
    !wget -O Dependencies_AUT.7z.002 https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dependencies/Dependencies_AUT.2
    !7z x Dependencies_AUT.7z.001
    !cp -r /content/usr/local/lib/python3.7/dist-packages /usr/local/lib/python3.7/
    !rm -r /content/usr
    !rm Dependencies_AUT.7z.001 Dependencies_AUT.7z.002
else:
  # Install triton
  !pip install -q -U --pre triton

if not os.path.exists('/tools/node/bin/lt'):
  !npm install -g localtunnel
!pip install -q gradio==3.5

gpuinfo = getoutput('nvidia-smi --query-gpu=name --format=csv,noheader')
!echo install tensorflow-cpu...
with capture.capture_output() as cap:
  !pip uninstall -y tensorflow-cpu tensorflow
  !pip install -q tensorflow-cpu tensorflow-io
!pip install -q git+https://github.com/KichangKim/DeepDanbooru.git@edf73df4cdaeea2cf00e9ac08bd8a9026b7a7b26#egg=deepdanbooru
!pip install -q scikit-image --upgrade

# Install xformers for python version < 3.10
if int(sys.version.split(' ')[0].split('.')[1])<10:
  !echo "$gpuinfo"
  if 'T4' in gpuinfo:
    if '3.7' in sys.version:
      %pip install -q https://github.com/daswer123/xformers_prebuild_wheels/raw/main/Google%20Collab/T4/python37/xformers-0.0.14.dev0-cp37-cp37m-linux_x86_64.whl
    elif '3.8' in sys.version:
      %pip install -q https://github.com/daswer123/xformers_prebuild_wheels/raw/main/Google%20Collab/T4/python38/xformers-0.0.14.dev0-cp38-cp38-linux_x86_64.whl
    elif '3.9' in sys.version:
      %pip install -q https://github.com/daswer123/xformers_prebuild_wheels/raw/main/Google%20Collab/T4/python39/xformers-0.0.14.dev0-cp39-cp39-linux_x86_64.whl
    else:
      !echo "install xformers failed: unsupported python version."
  elif 'P100' in gpuinfo:
    %pip install -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/P100/xformers-0.0.13.dev0-py3-none-any.whl
  elif 'V100' in gpuinfo:
    %pip install -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/V100/xformers-0.0.13.dev0-py3-none-any.whl
  elif 'A100' in gpuinfo:
    %pip install -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/A100/xformers-0.0.13.dev0-py3-none-any.whl
  else:
    print('it seems that your GPU is not supported at the moment, install xformers failed.')

!echo done
