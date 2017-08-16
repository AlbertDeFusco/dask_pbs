# Dask Distributed PBS integration

This tool provides a convenient way to initialize a Dask Distributed Cluster
from *within* a PBS/Torque job.

It reads the `PBS_NODEFILE` and starts the `dask-scheduler` and `dask-workers`
according to your job specification. This includes number of nodes and `-ppn` flags.

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

## Caveats

As of August 2017:
* Dask Distributed cannot utilize InfiniBand interconnects
* You will need to include a wait after calling `PBSJob()` before calling `Client()`
    * There is not yet any polling to check that all of the services have been started
