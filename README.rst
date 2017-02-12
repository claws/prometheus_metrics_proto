prometheus_metrics_proto
========================

`prometheus_metrics_proto` provides the ability to read and write Prometheus'
binary format metrics data structures which improves performance and reduces
bandwidth usage.

`prometheus_metrics_proto` is an extension module based on
`Pyrobuf <https://github.com/appnexus/pyrobuf>`_ which is a Cython based
implementation of the Google Protocol Buffers serialisation library. Pyrobuf
does not repuire `protoc`.

The `prometheus_metrics_proto` module provides the low level primitives for
generating Prometheus' binary metrics objects and serializing them in
preparation for network transfer.

As `prometheus_metrics_proto` is only providing the low level primitives it
is expected that you will create helper functions to make generating metrics
easier in your project. An example of a project doing this is
`aioprometheus <https://github.com/claws/aioprometheus>`_

The Protocol Buffer specification used by `prometheus_metrics_proto` was
obtained from the Prometheus `client model <https://github.com/prometheus/client_model/blob/master/metrics.proto>`_ repo.


Install
-------

.. code-block:: console

    $ pip install prometheus_metrics_proto


Example
-------

Creating metrics objects that can be ingested by Prometheus is relatively
straight-forward, but does require knowledge of how they are constructed.
The example below shows how a Counter metric can be constructed and marshalled
into a format suitable to send to Prometheus in a response.

.. code:: python

    import collections
    import datetime
    import pyrobuf_util
    from prometheus_metrics_proto import (
        COUNTER, Counter, LabelPair, Metric, MetricFamily)


    def create_metric_family(metric_name, metric_help, metric_type, metrics):
        '''
        Create a MetricFamily object to hold the name and help string
        for a metric along with all of its multi-dimensional (e.g. different
        labels) instances.
        '''
        return MetricFamily(
            name=metric_name, help=metric_help, type=metric_type, metric=metrics)


    def create_counter(labels, value, timestamp=False, ordered=True):
        '''
        Return a Metric object containing a Counter object. A Metric object is a
        container for a single multi-dimensional (e.g. different labels) instance
        of a specific metric, in this case a Counter. A Metric gets added to a
        MetricFamily object.
        '''
        if ordered:
            labels = collections.OrderedDict(sorted(labels.items(), key=lambda t: t[0]))
        labels = [LabelPair(name=k, value=str(v)) for k, v in labels.items()]
        counter = Counter(value=value)
        metric = Metric(label=labels, counter=counter)
        if timestamp:
            metric.timestamp_ms = int(
                datetime.datetime.now(
                    tz=datetime.timezone.utc).timestamp() * 1000)
        return metric


    def marshall(metrics):
        '''
        Marshall a sequence of MetricFamily objects into a bytes object
        suitable for network transmission.
        '''
        payload = []
        for m in metrics:
            encoded_metric = m.SerializeToString()
            length = pyrobuf_util.to_varint(len(encoded_metric))
            payload.append(length + encoded_metric)
        return b''.join(payload)


    host = 'examplehost'
    c1 = create_counter({'host': host, 'route': '/'}, 384)
    c2 = create_counter({'host': host, 'route': '/data'}, 56)
    cm = create_metric_family('requests', 'Number of requests.', COUNTER, (c1, c2))
    payload = marshall((cm, ))


License
-------

`prometheus_metrics_proto` is released under the MIT license.
