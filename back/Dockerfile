FROM python:3.9-slim
RUN python -m pip install --upgrade pip pip-tools
# RUN echo '#/bin/bash\npip install $1 && pip freeze | grep -i $1 >> requirements.in' > /usr/bin/pip-install && chmod +x /usr/bin/pip-install
# RUN echo '#/bin/bash\npip-compile\npip-sync' > /usr/bin/pip-compile-sync && chmod +x /usr/bin/pip-compile-sync
WORKDIR /opt/app
COPY requirements.* ./
RUN pip-compile && pip-sync
