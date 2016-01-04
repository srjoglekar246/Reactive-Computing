from django.db import models


class Dependency(models.Model):
    """
    Models a Parent-Child relationship between computational
    nodes. Also defines the order in which the children are to be
    arranged, to get the Parent's value.
    """

    parent = models.CharField('Parent Node', max_length=25)
    child = models.CharField('Child Node', max_length=25)
    argno = models.IntegerField('Argument Number')


class FunctionType(models.Model):
    """
    Stores information about the type of function/computation
    associated with a node.
    The function name should have a corresponding mapping in
    reactivecompute.functions.Functions.mapping
    """

    node = models.CharField('Node', max_length=25)
    functionname = models.CharField('Function Name', max_length=25)
    noofargs = models.IntegerField('Number of Arguments')


class DataLog(models.Model):
    """
    Stores information about the type of function/computation
    associated with nodes.
    """

    node = models.CharField('Node', max_length=25)
    timestamp = models.DateTimeField('Time Stamp')
    value = models.FloatField('Value', null=True)
