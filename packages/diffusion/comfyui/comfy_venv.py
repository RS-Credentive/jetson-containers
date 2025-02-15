# docker images don't contain the 'venv' comand, even though the venv module is part of the standard library, so we had to make our own script *eyeroll*
import venv

comfy_venv_builder = venv.EnvBuilder(
    system_site_packages=True,
    clear=True,
    symlinks=False,
    with_pip=True,
    prompt="ComfyUI_venv",
)

comfy_venv_builder.create("/data/models/comfyui/venv/")
