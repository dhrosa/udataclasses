FROM micropython/unix

WORKDIR /code
ENV PYTHONPATH="/code:${PYTHONPATH}"

# Library code
ADD src .
# Unit tests. Currently only this test passes in MicroPython.
ADD tests/test_transform_spec.py tests/
# pytest shim
ADD tests/micropython/pytest_shim.py pytest.py
# Test runner
ADD tests/micropython/run.py .

CMD micropython run.py
