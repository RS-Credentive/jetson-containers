#---
# name: comfyui
# group: diffusion
# depends: [pytorch, torchvision, torchaudio, opencv, bitsandbytes, transformers, xformers, torchao, diffusers, vhacdx, manifold, huggingface_hub]
# requires: '>=35.0.0'
# docs: docs.md
#---
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

WORKDIR /opt

# Generate a persistent .venv under /data/comfyui so that modules installed by nodes persist across reboots
COPY comfy_venv.py /opt/
RUN python3 /opt/comfy_venv.py 

# Clone the repository:
RUN git clone https://github.com/comfyanonymous/ComfyUI.git && \
    cd ComfyUI && \
    source /data/models/comfyui/venv/bin/activate &&\
    python -m pip install --no-cache-dir -r requirements.txt

RUN cd /opt/ComfyUI/custom_nodes && \
    git clone --recursive https://github.com/ltdrdata/ComfyUI-Manager.git && \
    git clone --recursive https://github.com/discus0434/comfyui-flux-accelerator.git && \
    git clone --recursive https://github.com/pydn/ComfyUI-to-Python-Extension.git

RUN cd /opt/ComfyUI/custom_nodes/comfyui-flux-accelerator/scripts && \
    if [ -f download_taef1.sh ]; then \
        chmod +x download_taef1.sh && bash download_taef1.sh; \
    else \
        echo "download_taef1.sh not found"; \
    fi && \
    cd /opt/ComfyUI/

WORKDIR /opt/ComfyUI/

RUN source /data/models/comfyui/venv/bin/activate &&\ 
    python -m pip install --no-cache-dir -U xformers onnxruntime-gpu triton lm_eval

RUN source /data/models/comfyui/venv/bin/activate &&\ 
    python -m pip install --no-cache-dir -U diffusers flash-attn sageattention  torchao

COPY workflow /opt/ComfyUI/workflow
COPY extra_model_paths.yaml /opt/ComfyUI/extra_model_paths.yaml
COPY extra /opt/ComfyUI/extra
EXPOSE 8188

RUN source /data/models/comfyui/venv/bin/activate &&\ 
    /opt/ComfyUI/extra/init.sh
CMD source /data/models/comfyui/venv/bin/activate &&\ 
    python main.py --listen 0.0.0.0 --port ${PORT:-8188}