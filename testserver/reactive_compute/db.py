from reactive_compute.models import DataLog
from django.utils import timezone


def save_node_value(node, value):
    """
    Saves the latest computed value of the given node.
    """
    data_entry = DataLog(node=str(node),
                         timestamp=timezone.now(),
                         value=value)
    data_entry.save()
