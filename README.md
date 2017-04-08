# evolene
A Python rewrite of https://gita.sys.kth.se/Infosys/zermatt

Pipeline functionality for building, testing and pushing Docker images.

To run: 
```bash
python run.py docker run-pipeline
```

To create dist:
```bash
./create_dist.sh
```
The version of the dist is defined in `setup.py`

To run tests:
```bash
./run_tests.sh
```
