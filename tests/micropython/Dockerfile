FROM micropython/unix

WORKDIR /code
ENV PYTHONPATH="/code:${PYTHONPATH}"

# Library code
ADD src .
# Unit tests. Currently only these tests pass in MicroPython.
ADD tests/test_transform_spec.py tests/
ADD tests/test_source.py tests/
# pytest shim
ADD tests/micropython/pytest_shim.py pytest.py
# Test runner
ADD tests/micropython/run.py .

CMD micropython run.py
