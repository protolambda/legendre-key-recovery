# Legendre key-recovery attacks

This repository translates the Python POC implementation by @dankrad into a faster Go implementation.
The POC was based on work by Dmitry Khovratovich, see https://eprint.iacr.org/2019/862.pdf

To run the Go code:

```bash
# no install, no dependencies other than a valid Go install with Go modules support

# the recovery
go test . -test.bench=BenchmarkRecovery -test.benchtime=1x -test.count=10

# the other Jacobi benches
go test . -test.bench=BenchmarkJacobiUint64
go test . -test.bench=BenchmarkJacobiBigInt
```

To run the Python code:

```bash
cd dankrad_poc
# install
python3 -m venv ./venv
. venv/bin/activate
pip3 install -r requirements.txt

# run recovery
python3 khovratovich_algorithm.py

# run jacobi bench
python3 bench_jacobi.py
```
