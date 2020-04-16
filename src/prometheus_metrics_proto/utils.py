"""
This module provides wrapper functions to help create the various data types
used in Prometheus metrics.
"""

import collections
import datetime

from .prometheus_metrics_pb2 import (
    COUNTER,
    GAUGE,
    SUMMARY,
    HISTOGRAM,
    Bucket,
    Counter,
    Gauge,
    Histogram,
    LabelPair,
    Metric,
    MetricFamily,
    Summary,
    Quantile,
)
from typing import Dict, List, Sequence, Tuple, Union


# typing aliases
MetricType = int  # one of COUNTER, GAUGE, SUMMARY, HISTOGRAM
LabelsType = Dict[str, str]
NumericValueType = Union[int, float]
SummaryDictKeyType = Union[float, str]  # e.g. sum, 0.25, etc
SummaryDictType = Dict[SummaryDictKeyType, NumericValueType]
HistogramDictKeyType = Union[float, str]  # e.g. sum, 0.25, etc
HistogramDictType = Dict[HistogramDictKeyType, NumericValueType]
CollectorsType = Union[Counter, Gauge, Histogram, Summary]
MetricValueType = Union[float, SummaryDictType, HistogramDictType]
MetricTupleType = Tuple[LabelsType, MetricValueType]


def create_counter_metric(
    labels: LabelsType,
    value: float,
    timestamp: bool = False,
    const_labels: LabelsType = None,
    ordered: bool = True,
) -> Metric:
    """ Create a Metric object containing a Counter object.

    A Metric object is a container for a single multi-dimensional (e.g.
    different labels) instance of a specific metric, in this case a Counter.

    :param labels: a dict of labels that define this particular instance of a
      metric.
    :param value: a float representing the value of the metric.
    :param timestamp: a boolean that determines if a timestamp is added to
      the metric. By default this is False.
    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True.
    :returns: a Metric object containing a Counter object
    """
    unified_labels = _unify_labels(labels, const_labels, ordered=ordered)
    labels = [LabelPair(name=k, value=str(v)) for k, v in unified_labels.items()]
    counter = Counter(value=value)
    metric = Metric(label=labels, counter=counter)
    if timestamp:
        metric.timestamp_ms = _timestamp_ms()
    return metric


def create_gauge_metric(
    labels: LabelsType,
    value: float,
    timestamp: bool = None,
    const_labels: LabelsType = None,
    ordered=True,
) -> Metric:
    """ Create a Metric object containing a Gauge object.

    A Metric object is a container for a single multi-dimensional (e.g.
    different labels) instance of a specific metric, in this case a Gauge.

    :param labels: a dict of labels that define this particular instance of a
      metric.
    :param value: a float representing the value of the metric.
    :param timestamp: a boolean that determines if a timestamp is added to
      the metric. By default this is False.
    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True.
    :returns: a Metric object containing a Gauge object
    """
    unified_labels = _unify_labels(labels, const_labels, ordered=ordered)
    labels = [LabelPair(name=k, value=str(v)) for k, v in unified_labels.items()]
    gauge = Gauge(value=value)
    metric = Metric(label=labels, gauge=gauge)
    if timestamp:
        metric.timestamp_ms = _timestamp_ms()
    return metric


def create_summary_metric(
    labels: LabelsType,
    values: SummaryDictType,
    samples_count: int,
    samples_sum: float,
    timestamp: bool = None,
    const_labels: LabelsType = None,
    ordered=True,
) -> Metric:
    """ Create a Metric object containing a Summary object.

    A Metric object is a container for a single multi-dimensional (e.g.
    different labels) instance of a specific metric, in this case a Summary.

    :param labels: a dict of labels that define this particular instance of a
      metric.
    :param values: a dict representing the various quantile values of the
      metric. The count and sum may be present in this dict.
    :param samples_count: an integer representing the number of samples.
    :param samples_sum: a float representing the sum of samples.
    :param timestamp: a boolean that determines if a timestamp is added to
      the metric. By default this is False.
    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True.
    :returns: a Metric object containing a Summary object
    """
    unified_labels = _unify_labels(labels, const_labels, ordered=ordered)
    labels = [LabelPair(name=k, value=str(v)) for k, v in unified_labels.items()]
    # The count and sum values may also be present in the values.
    # Only process non-string keys into quantile objects.
    quantiles = []
    for k, v in values.items():
        # sample_count += v
        # sample_sum += k * v
        if not isinstance(k, str):
            quantiles.append(Quantile(quantile=k, value=v))
    summary = Summary(
        sample_count=samples_count, sample_sum=samples_sum, quantile=quantiles
    )
    metric = Metric(label=labels, summary=summary)
    if timestamp:
        metric.timestamp_ms = _timestamp_ms()
    return metric


def create_histogram_metric(
    labels: LabelsType,
    values: HistogramDictType,
    samples_count: int,
    samples_sum: float,
    timestamp: bool = None,
    const_labels: LabelsType = None,
    ordered=True,
) -> Metric:
    """ Create a Metric object containing a Histogram object.

    A Metric object is a container for a single multi-dimensional (e.g.
    different labels) instance of a specific metric, in this case a Histogram.

    :param labels: a dict of labels that define this particular instance of a
      metric.
    :param values: a dict representing the various bucket values of the
      metric. The cumulative count and sum values may be present in this dict.
    :param samples_count: an integer representing the number of observations.
    :param samples_sum: a float representing the sum of observations.
    :param timestamp: a boolean that determines if a timestamp is added to
      the metric. By default this is False.
    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True.
    :returns: a Metric object containing a Summary object
    """
    unified_labels = _unify_labels(labels, const_labels, ordered=ordered)
    labels = [LabelPair(name=k, value=str(v)) for k, v in unified_labels.items()]
    # The count and sum values may also be present in the values.
    # Only process non-string keys into bucket objects.
    buckets = []
    for k, v in values.items():
        if not isinstance(k, str):
            buckets.append(Bucket(cumulative_count=v, upper_bound=k))
    histogram = Histogram(
        sample_count=samples_count, sample_sum=samples_sum, bucket=buckets
    )
    metric = Metric(label=labels, histogram=histogram)
    if timestamp:
        metric.timestamp_ms = _timestamp_ms()
    return metric


def create_metric_family(
    metric_name: str,
    metric_help: str,
    metric_type: MetricType,
    metrics: Union[Sequence[Metric], Sequence[MetricTupleType]],
    timestamp: bool = False,
    const_labels: LabelsType = None,
    ordered=True,
) -> MetricFamily:
    """ Create a MetricsFamily object.

    A MetricFamily object is the parent container for Metric objects.
    A MetricFamily object holds the name and help string for a metric along
    with all of its multi-dimensional (e.g. different labels) metric
    instances.

    :param metric_name: a string representing the metric name.

    :param metric_help: a string representing the metric help.

    :param metric_type: an enumeration from the set of COUNTER, GAUGE,
      HISTOGRAM, SUMMARY.

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
    if metrics:

        if not all([isinstance(m, Metric) for m in metrics]):
            # When the metrics argument is not a list of Metrics objects it
            # is expected to be a sequence of 2-tuple objects which contain labels
            # and values to use for generating Metrics objects.
            _metrics = []
            for metric_labels, metric_values in metrics:

                if metric_type == COUNTER:
                    metric = create_counter_metric(
                        metric_labels,
                        metric_values,
                        timestamp=timestamp,
                        const_labels=const_labels,
                        ordered=ordered,
                    )

                elif metric_type == GAUGE:
                    metric = create_gauge_metric(
                        metric_labels,
                        metric_values,
                        timestamp=timestamp,
                        const_labels=const_labels,
                        ordered=ordered,
                    )

                elif metric_type == SUMMARY:
                    # The count and sum values are expected to be present in the
                    # values dict.
                    count = metric_values["count"]
                    sum_ = metric_values["sum"]
                    metric = create_summary_metric(
                        metric_labels,
                        metric_values,
                        count,
                        sum_,
                        timestamp=timestamp,
                        const_labels=const_labels,
                        ordered=ordered,
                    )

                elif metric_type == HISTOGRAM:
                    # The count and sum values are expected to be present in the
                    # values dict.
                    count = metric_values["count"]
                    sum_ = metric_values["sum"]
                    metric = create_histogram_metric(
                        metric_labels,
                        metric_values,
                        count,
                        sum_,
                        timestamp=timestamp,
                        const_labels=const_labels,
                        ordered=ordered,
                    )

                else:
                    raise Exception("Invalid metric_type: {}".format(metric_type))

                if timestamp:
                    metric.timestamp_ms = _timestamp_ms()

                _metrics.append(metric)

            metrics = _metrics

    mf = MetricFamily(
        name=metric_name, help=metric_help, type=metric_type, metric=metrics
    )

    return mf


def create_labels(labels: LabelsType) -> List[LabelPair]:
    """ Create a list of LabelPair objects from a dict of labels. """
    return [LabelPair(name=k, value=str(v)) for k, v in labels.items()]


def create_quantile(quantile: float, value: float) -> Quantile:
    """ Create a Quantile object """
    return Quantile(quantile=quantile, value=value)


def create_bucket(cumulative_count: int, upper_bound: float) -> Bucket:
    """ Create a Bucket object """
    return Bucket(cumulative_count=cumulative_count, upper_bound=upper_bound)


def _timestamp_ms() -> int:
    """ Return a UTC timestamp, in milliseconds.

    This function is used to populate the timestamp_ms field in a Metric object.
    """
    return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp() * 1000)


def _unify_labels(
    labels: LabelsType = None, const_labels: LabelsType = None, ordered: bool = True
) -> LabelsType:
    """ Return a dict that combines labels and const_labels for a metric.

    If ordered is True then the combined labels are sorted by key.

    :param labels: a dict of labels for a metric.

    :param const_labels: a dict of constant labels to be associated with
      the metric.

    :param ordered: a boolean that determines if the labels are sorted by key.
      By default this is True.

    :returns: a dict of labels
    """
    unified_labels = {}

    if const_labels:
        unified_labels.update(const_labels.copy())

    if labels:
        unified_labels.update(labels.copy())

    if ordered and unified_labels:
        unified_labels = collections.OrderedDict(
            sorted(unified_labels.items(), key=lambda t: t[0])
        )

    return unified_labels
