FROM public.ecr.aws/sam/build-python3.12:latest

COPY requirements.txt /app/
COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8086

ENTRYPOINT ["gunicorn", "-b", ":8086", "app.main:APP", "--workers=1", "--threads=2", "--timeout=120"]