# Dask Distributed PBS integration

This tool provides a convenient way to initialize a Dask Distributed Cluster
from *within* a PBS/Torque job.

It reads the `PBS_NODEFILE` and starts the `dask-scheduler` and `dask-workers`
according to your job specification. This includes number of nodes and `-l nodes=xx:ppn=yy` flags.

The Dask processes will automatically shutdown when the job completes. Please check with your
PBS queue admins to ensure that this happens.

## Installation

1. Clone this repo
2. cd to the clone
3. run `python setup.py install`
    * Or `pip install .`

**Coming soon**: I'll get around to making a conda package


## Required packages

It is recommended that you use conda to install packages.
The following three packages are the minimum required package to use `dask_pbs`. Conda will also install all required dependencies.

* `dask`
* `distributed`
* `paramiko`

## Example

After installing `dask_pbs` your script would look like this

```python
#!/usr/bin/env python

from dask_pbs import PBSJob
from distributed import Client

s = PBSJob()

c = Client(s)

# continue with Dask code:
#  Delayed, Array, e.submit() etc.
```

You would then execute this script in your PBS job

```bash
#PBS -l nodes= ...

activate my-conda-env

python my-dask-distributed-script.py
```

## Caveats

As of August 2017:
* Dask Distributed cannot utilize InfiniBand interconnects
* You will need to include a wait after calling `PBSJob()` and before `Client()`
    * `PBSJob()` does not yet poll the nodes to check that all of the services have been started
* `dask_pbs` is a very new project and it hasn't been rigorously tested
    * It should work on both Python 2 and Python 3.

