# Legendre key-recovery attacks

This repository translates the Python POC implementation by @dankrad into a faster Go implementation.
The POC was based on work by Dmitry Khovratovich, see https://eprint.iacr.org/2019/862.pdf

Run Go benchmark:

```bash
go test . -test.bench=BenchmarkRecovery -test.benchtime=1x -test.count=10
```

Install and run Python code:

```bash
cd dankrad_poc
# install
python3 -m venv ./venv
. venv/bin/activate
pip3 install -r requirements.txt

# run
python3 khovratovich_algorithm.py
```