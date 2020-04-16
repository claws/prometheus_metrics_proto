#!/usr/bin/env python
"""
This script demonstrates the high level helper functions used to assist
creating various metrics kinds as well as how to encode the metrics into
a form that can be sent to Prometheus server.
"""

import prometheus_metrics_proto as pmp


def main():

    # Define some labels that we want added to all metrics. These labels are
    # independent of the instance labels that define a metric as unique.
    # These could be used to add hostname, app name, etc.
    const_labels = {"host": "examplehost", "app": "my_app"}

    # Create a Counter metric to track logged in users. This counter has
    # 5 separate instances.
    # We'll make use of the optional const_labels argument to add extra
    # constant labels.
    # We will also add a timestamp to the metric instances.
    # We will request that the labels be sorted.
    cm = pmp.create_counter(
        "logged_users_total",
        "Logged users in the application.",
        (
            ({"country": "sp", "device": "desktop"}, 520),
            ({"country": "us", "device": "mobile"}, 654),
            ({"country": "uk", "device": "desktop"}, 1001),
            ({"country": "de", "device": "desktop"}, 995),
            ({"country": "zh", "device": "desktop"}, 520),
        ),
        timestamp=True,
        const_labels=const_labels,
        ordered=True,
    )

    # Create a Gauge metric, similar to the counter above.
    gm = pmp.create_gauge(
        "logged_users_total",
        "Logged users in the application.",
        (
            ({"country": "sp", "device": "desktop"}, 520),
            ({"country": "us", "device": "mobile"}, 654),
            ({"country": "uk", "device": "desktop"}, 1001),
            ({"country": "de", "device": "desktop"}, 995),
            ({"country": "zh", "device": "desktop"}, 520),
        ),
        timestamp=True,
        const_labels=const_labels,
        ordered=True,
    )

    # Now lets create a Summary and Histogram metric object. These forms
    # of metrics are slightly more complicated.
    #
    # Remember, the collection of metrics and the management of Summary
    # Quantiles and Histogram Buckets are outside the scope of
    # functionality provided by this package.
    #
    # The following examples assume they are taking the data values from
    # a management library that can also emit the sum and count fields
    # expected for both Summary and Histogram metrics.

    # Create a Summary metric. The values for a summary are slightly
    # different to a Counter or Gauge. They are composed of a dict representing
    # the various quantile values of the metric. The count and sum are
    # expected to be present in this dict.
    sm = pmp.create_summary(
        "request_payload_size_bytes",
        "Request payload size in bytes.",
        (
            ({"route": "/"}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4}),
            (
                {"route": "/data"},
                {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4},
            ),
        ),
        timestamp=True,
        const_labels=const_labels,
        ordered=True,
    )

    # Create a Histogram metric. The values for a histogram are slightly
    # different to a Counter or Gauge. They are composed of a dict representing
    # the various bucket values of the metric. The cumulative count and sum
    # values are expected to be present in this dict.
    #
    # Libraries manageing buckets typically have add a POS_INF upper bound to
    # catch values beyond the largest bucket bound. Simulate this behavior in
    # the data below.
    POS_INF = float("inf")

    hm = pmp.create_histogram(
        "request_latency_seconds",
        "Request latency in seconds.",
        (
            (
                {"route": "/"},
                {5.0: 3, 10.0: 2, 15.0: 1, POS_INF: 0, "count": 6, "sum": 46.0},
            ),
            (
                {"route": "/data"},
                {5.0: 3, 10.0: 2, 15.0: 1, POS_INF: 0, "count": 6, "sum": 46.0},
            ),
        ),
        timestamp=True,
        const_labels=const_labels,
        ordered=True,
    )

    # Serialize a sequence of metrics into a payload suitable for network
    # transmission.
    input_metrics = (cm, gm, sm, hm)
    payload = pmp.encode(*input_metrics)
    assert isinstance(payload, bytes)

    # De-serialize the payload into a sequence of MetricsFamily objects.
    recovered_metrics = pmp.decode(payload)

    # Confirm that the round trip re-produced the same number of metrics
    # and that the metrics are identical.
    assert len(recovered_metrics) == len(input_metrics)
    for recovered_metric, input_metric in zip(recovered_metrics, input_metrics):
        assert recovered_metric == input_metric

    for metric in input_metrics:
        print(metric)


if __name__ == "__main__":
    main()
