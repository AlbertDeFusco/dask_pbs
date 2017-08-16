from distributed.deploy.ssh import SSHCluster
import os

class PBSJob(SSHCluster):
    '''Initialize a cluster from within a PBS/Torque job

    PBSJob is meant to be launched from within a running PBS/Torque job.
    It will read the PBS_NODEFILE
      1. Start the dask-scheduler on the FIRST node
      2. Start the dask-worker on ALL nodes

    Arguments:
      scheduler_port: Default is 8786
      interface: Append hostnames with chosen interface (i.e, -eth0, -ib0)
                 The default is None and no modifications to the hostnames
                 In the PBS_NODEFILE are made.
      nthreads: The number of threads (NumPy, Pandas) to run per dask-worker. Default 0
      nprocs: The number of Python processes to start per dask-worker. Default 1
      logdir: Change the directory where logs are written. Default None
    '''
    def __init__(self, scheduler_port=8786, interface=None, nthreads = 0, nprocs = 1, logdir = None):
        nodefile = os.environ.get('PBS_NODEFILE')
        if nodefile:
            with open(nodefile) as f:
                nodes = [l.strip() for l in f.readlines()]
        else:
            raise ValueError('Must be run within a PBS job')

        if not nthreads:
            try:
                nthreads = os.environ.get('PBS_NUM_PPN')
            except KeyError:
                raise ValueError('Could not determine threads per node. Use the nthreads keyword argument')

        #TODO: use a specific interface
        if interface:
            nodes = ['{:s}-{:s}'.format(n,interface) for n in nodes]

        super(PBSCluster, self).__init__(scheduler_addr=nodes[0], scheduler_port=scheduler_port,
                worker_addrs=set(nodes), nthreads=nthreads, nprocs=nprocs, logdir=logdir)

