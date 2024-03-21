FROM micropython/unix
WORKDIR /code
ENV PYTHONPATH="/code:${PYTHONPATH}"
ADD src .
ADD tests/micropython/smoke_test.py .
CMD micropython smoke_test.py
