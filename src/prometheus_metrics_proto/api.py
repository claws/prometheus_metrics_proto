"""
This module provides high level functions to assist generating Prometheus
metrics.
"""

from google.protobuf.internal.decoder import _DecodeVarint as varintDecoder
from google.protobuf.internal.encoder import _EncodeVarint as varintEncoder

from . import utils
from .prometheus_metrics_pb2 import (
    COUNTER,
    GAUGE,
    SUMMARY,
    HISTOGRAM,
    Metric,
    MetricFamily,
)
from typing import List, Sequence, Union


def create_counter(
    metric_name: str,
    metric_help: str,
    metrics: Union[Sequence[Metric], Sequence[utils.MetricTupleType]],
    timestamp: bool = False,
    const_labels: utils.LabelsType = None,
    ordered=True,
) -> MetricFamily:
    """ Create a MetricsFamily object containing a Counter.

    A MetricFamily object is the parent container for Metric objects.
    A MetricFamily object holds the name and help string for a metric along
    with all of its multi-dimensional (e.g. different labels) metric
    instances.

    :param metric_name: a string representing the metric name.

    :param metric_help: a string representing the metric help.

    :param metrics: This argument can take two forms. The first is a sequence
      of pre-generated Metric objects. The second is a sequence of 2-Tuple's
      containing the raw labels and values for each multi-dimensional metric
      instance that will be generated and added to the MetricsFamily object.
      It is valid for metrics to be an empty, this represents a declared
      metric that just has not received any updates yet.

    :param timestamp: a boolean that determines if a timestamp is added to
      generated metric instances. By default this is False. This parameter
      is only used if the ``metrics`` argument is not a pre-generated list of
      Metrics objects.

    :param const_labels: an extra dict of labels that should be added to
      labels of any generated Metrics objects. This parameter is only used if
      the ``metrics`` argument is not a pre-generated list of Metrics
      objects.

    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True. This parameter is only used if the ``metrics``
      argument is not a pre-generated list of Metrics objects.

    :returns: a MetricFamily object populated with metrics data
    """
    return utils.create_metric_family(
        metric_name,
        metric_help,
        COUNTER,
        metrics,
        timestamp=timestamp,
        const_labels=const_labels,
        ordered=ordered,
    )


def create_gauge(
    metric_name: str,
    metric_help: str,
    metrics: Union[Sequence[Metric], Sequence[utils.MetricTupleType]],
    timestamp: bool = False,
    const_labels: utils.LabelsType = None,
    ordered=True,
) -> MetricFamily:
    """ Create a MetricsFamily object containing a Gauge.

    A MetricFamily object is the parent container for Metric objects.
    A MetricFamily object holds the name and help string for a metric along
    with all of its multi-dimensional (e.g. different labels) metric
    instances.

    :param metric_name: a string representing the metric name.

    :param metric_help: a string representing the metric help.

    :param metrics: This argument can take two forms. The first is a sequence
      of pre-generated Metric objects. The second is a sequence of 2-Tuple's
      containing the raw labels and values for each multi-dimensional metric
      instance that will be generated and added to the MetricsFamily object.
      It is valid for metrics to be an empty, this represents a declared
      metric that just has not received any updates yet.

    :param timestamp: a boolean that determines if a timestamp is added to
      generated metric instances. By default this is False. This parameter
      is only used if the ``metrics`` argument is not a pre-generated list of
      Metrics objects.

    :param const_labels: an extra dict of labels that should be added to
      labels of any generated Metrics objects. This parameter is only used if
      the ``metrics`` argument is not a pre-generated list of Metrics
      objects.

    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True. This parameter is only used if the ``metrics``
      argument is not a pre-generated list of Metrics objects.

    :returns: a MetricFamily object populated with metrics data
    """
    return utils.create_metric_family(
        metric_name,
        metric_help,
        GAUGE,
        metrics,
        timestamp=timestamp,
        const_labels=const_labels,
        ordered=ordered,
    )


def create_summary(
    metric_name: str,
    metric_help: str,
    metrics: Union[Sequence[Metric], Sequence[utils.MetricTupleType]],
    timestamp: bool = False,
    const_labels: utils.LabelsType = None,
    ordered=True,
) -> MetricFamily:
    """ Create a MetricsFamily object containing a Summary.

    A MetricFamily object is the parent container for Metric objects.
    A MetricFamily object holds the name and help string for a metric along
    with all of its multi-dimensional (e.g. different labels) metric
    instances.

    :param metric_name: a string representing the metric name.

    :param metric_help: a string representing the metric help.

    :param metrics: This argument can take two forms. The first is a sequence
      of pre-generated Metric objects. The second is a sequence of 2-Tuple's
      containing the raw labels and values for each multi-dimensional metric
      instance that will be generated and added to the MetricsFamily object.
      It is valid for metrics to be an empty, this represents a declared
      metric that just has not received any updates yet.

    :param timestamp: a boolean that determines if a timestamp is added to
      generated metric instances. By default this is False. This parameter
      is only used if the ``metrics`` argument is not a pre-generated list of
      Metrics objects.

    :param const_labels: an extra dict of labels that should be added to
      labels of any generated Metrics objects. This parameter is only used if
      the ``metrics`` argument is not a pre-generated list of Metrics
      objects.

    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True. This parameter is only used if the ``metrics``
      argument is not a pre-generated list of Metrics objects.

    :returns: a MetricFamily object populated with metrics data
    """
    return utils.create_metric_family(
        metric_name,
        metric_help,
        SUMMARY,
        metrics,
        timestamp=timestamp,
        const_labels=const_labels,
        ordered=ordered,
    )


def create_histogram(
    metric_name: str,
    metric_help: str,
    metrics: Union[Sequence[Metric], Sequence[utils.MetricTupleType]],
    timestamp: bool = False,
    const_labels: utils.LabelsType = None,
    ordered=True,
) -> MetricFamily:
    """ Create a MetricsFamily object containing a Histogram.

    A MetricFamily object is the parent container for Metric objects.
    A MetricFamily object holds the name and help string for a metric along
    with all of its multi-dimensional (e.g. different labels) metric
    instances.

    :param metric_name: a string representing the metric name.

    :param metric_help: a string representing the metric help.

    :param metrics: This argument can take two forms. The first is a sequence
      of pre-generated Metric objects. The second is a sequence of 2-Tuple's
      containing the raw labels and values for each multi-dimensional metric
      instance that will be generated and added to the MetricsFamily object.
      It is valid for metrics to be an empty, this represents a declared
      metric that just has not received any updates yet.

    :param timestamp: a boolean that determines if a timestamp is added to
      generated metric instances. By default this is False. This parameter
      is only used if the ``metrics`` argument is not a pre-generated list of
      Metrics objects.

    :param const_labels: an extra dict of labels that should be added to
      labels of any generated Metrics objects. This parameter is only used if
      the ``metrics`` argument is not a pre-generated list of Metrics
      objects.

    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True. This parameter is only used if the ``metrics``
      argument is not a pre-generated list of Metrics objects.

    :returns: a MetricFamily object populated with metrics data
    """
    return utils.create_metric_family(
        metric_name,
        metric_help,
        HISTOGRAM,
        metrics,
        timestamp=timestamp,
        const_labels=const_labels,
        ordered=ordered,
    )


def encode(*metrics: MetricFamily) -> bytes:
    """ Encode MetricFamily objects into a bytes object.

    MetricFamily objects are encoded using the strategy expected by the
    Prometheus Server which expects each encoded MetricFamily object to be
    prefixed with a varint containing the size of the encoded MetricFamily
    object.

    :param metrics: MetricsFamily objects to encode.
    :returns: encoded MetricsFamily objects.
    """
    if not all([isinstance(m, MetricFamily) for m in metrics]):
        raise Exception(
            "Expected metrics to be instances of MetricFamily, got {}".format(
                [type(m) for m in metrics]
            )
        )

    buf = bytearray()
    for m in metrics:
        encoded_metric = m.SerializeToString()
        varintEncoder(buf.extend, len(encoded_metric), None)
        buf.extend(encoded_metric)
    return bytes(buf)


def decode(data: bytes) -> List[MetricFamily]:
    """ Decode a bytes object into a list of MetricFamily objects.

    Each encoded MetricFamily object is constructed of a two parts. The first
    is a varint containing the size of the following encoded MetricFamily
    object.

    :param data: a bytes object containing encoded MetricsFamily object.
    :returns: a list of MetricsFamily objects.
    """
    buffer = bytearray(data)
    metrics = []
    while buffer:
        mf_size, pos = varintDecoder(buffer, 0)
        buffer = buffer[pos:]
        mf_data = bytes(buffer[:mf_size])
        buffer = buffer[mf_size:]
        mf = MetricFamily()
        mf.ParseFromString(mf_data)
        metrics.append(mf)
    return metrics
