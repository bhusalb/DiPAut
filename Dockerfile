FROM python:3.9
COPY . /usr/src/dipAut
WORKDIR /usr/src/dipAut
RUN pip install -r requirements.txt
CMD ["/bin/bash"]
