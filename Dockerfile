FROM python:3.10.2-buster

ENV DOCKER_BUILDKIT=0

WORKDIR /bin

# Install talib
RUN mkdir ./asset
RUN ls
COPY ta-lib-0.4.0-src.tar.gz ./asset
RUN cd ./asset; ls
RUN cd ./asset; tar -xvzf ta-lib-0.4.0-src.tar.gz
RUN cd ./asset; ls
RUN cd ./asset/ta-lib; ./configure --prefix=/usr; make; make install
RUN rm -rf ./asset

# Install python package
COPY requirements.txt ./
RUN python -m pip install --upgrade pip -r requirements.txt

COPY bin /bin

ENTRYPOINT [ "python", "main.py" ]
