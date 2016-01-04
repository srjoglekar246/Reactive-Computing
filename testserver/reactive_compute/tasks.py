from __future__ import absolute_import
from celery import shared_task
from reactive_compute.models import Dependency, FunctionType
from reactive_compute.db import save_node_value
from reactive_compute.functions import Functions
from redis import StrictRedis
import redis_lock


@shared_task
def compute_nodes(nodes, timeout=60):
    """
    Computes values for all computational nodes as defined in the
    FunctionType model. Recursive calls are made based on information
    present in respective Dependency entries.

    'nodes' should be a dict mapping name of computational node, to:
    A floating point number as input, OR
    None, if the value is to be (possibly) computed.
    'timeout' defines the time interval for which the values of the
    nodes mentioned in 'nodes' will be valid. Default is a minute.
    """

    #First handle the boundary case
    if len(nodes) == 0:
        return None

    #Get a connection to Redis
    conn = StrictRedis()

    #This will contain all the parent nodes that we will try to compute
    #recursively based on the args currently provided.
    parents = set([])

    #Default initialization for Celery
    value = None

    #Iterate over all nodes
    for node in nodes:
        ##First obtain the value of the node
        if nodes[node] is not None:
            #Value has been provided as input
            try:
                #Ensure the given value can be parsed/converted to
                #a float.
                value = float(nodes[node])
            except:
                #If representing the value as a float fails,
                #skip this one.
                continue
        else:
            #Value has to be computed.

            #First acquire lock for the particular node.
            #This ensures that the inputs needed for computing
            #the current node don't get modified midway(unless
            #one expires, in which case the computation may or may
            #not go through).
            lock = redis_lock.RedisLock(conn, node + '_lock')
            if lock.acquire():
                try:
                    #This will indicate if all args are present for
                    #computation of the result
                    all_args_flag = True
                    #This will store all the required arguments in order
                    args = []
                    #Get the pertinent FunctionType instance
                    func_info = FunctionType.objects.get(node=node)
                    #Iterate over all arguments
                    for i in range(func_info.noofargs):
                        #Get Redis value
                        v = conn.get(node + '_' + `i`)
                        if v is None or v == 'None':
                            #If value not present stop iterations
                            all_args_flag = False
                            break
                        else:
                            args.append(float(v))
                    #If any arg was absent, abort processing of this node
                    if not all_args_flag:
                        continue
                    #Compute the value, since all args are present
                    value = Functions.mapping[func_info.functionname](
                        args)
                    #Delete info about current args
                    for i in range(func_info.noofargs):
                        conn.delete(node + '_' + `i`)
                except:
                    pass
                finally:
                    #Release lock
                    lock.release()

        ##Now that the value has been obtained, update the args info
        ##for all parent nodes
        parent_objs = Dependency.objects.filter(child=node)
        for parent_obj in parent_objs:
            #Get lock for parent
            lock = redis_lock.RedisLock(conn, parent_obj.parent + '_lock')
            if lock.acquire():
                try:
                    #Set value
                    conn.set(parent_obj.parent + '_' + `parent_obj.argno`,
                             value)
                    #Set expiry time
                    conn.expire(parent_obj.parent + '_' + `parent_obj.argno`,
                                timeout)
                except:
                    pass
                finally:
                    #Release lock
                    lock.release()
            #Add this parent to the set of parents to process
            parents.add(parent_obj.parent)

        #Save value in database as needed
        save_node_value(node, value)

    #Make the recursive call on parent nodes
    compute_nodes.delay(dict((parent, None) for parent in parents),
                        timeout)
