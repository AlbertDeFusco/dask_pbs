from distributed.deploy.ssh import SSHCluster
import os

class PBSJob(SSHCluster):
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

