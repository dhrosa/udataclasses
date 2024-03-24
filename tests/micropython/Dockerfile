FROM micropython/unix

WORKDIR /code
ENV PYTHONPATH="/code:${PYTHONPATH}"

# Library code
ADD src .
# Unit tests.
ADD tests/test_*.py tests/
# pytest shim
ADD tests/micropython/pytest_shim.py pytest.py
# Test runner
ADD tests/micropython/run.py .

CMD micropython run.py
