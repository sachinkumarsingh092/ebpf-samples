**Problem statement**: Write an eBPF code to allow traffic only at a specific TCP port (default 4040) for a given process name (for e.g, "myprocess"). All the traffic to all other ports for only that process should be dropped.

**Solution and Learnings**
Even though the problem statement says that this is for experieced folks, I took a stab at it.
My approach here is to use a hash map to get the *PID* of the "process" from the userspace and then apply a sililar apporach to the previous problem to block the packets to a particular port.
I think I'm close but the verifier is giving me some errors. I think this can become a great exercise to pair-program and hack on to in one of the sessions.

**References**:
- https://github.com/iovisor/bcc/blob/master/docs/reference_guide.md

- https://github.com/iovisor/bcc/blob/ec49363e2e9daec026ee6cae4c5fc316f8fab0ff/examples/tracing/hello_perf_output_using_ns.py
