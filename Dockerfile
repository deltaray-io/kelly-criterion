FROM python:3.7-slim-stretch

WORKDIR /app

COPY requirements.txt .
RUN build_deps='gcc libc6-dev make' && \
    apt-get update && \
    apt-get install -y --no-install-recommends git ${build_deps} && \
    pip install -r requirements.txt && \
    apt-get purge -y --auto-remove ${build_deps} && \
    rm -rf /var/lib/apt/lists/*

COPY . .
RUN python setup.py install

ENTRYPOINT ["kelly_criterion"]