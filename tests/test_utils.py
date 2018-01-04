
import unittest

import prometheus_metrics_proto as pmp

# from prometheus_metrics_proto.prometheus_metrics_pb2 import (
#     COUNTER,
#     GAUGE,
#     SUMMARY,
#     HISTOGRAM,
#     LabelPair,
#     Metric,
#     MetricFamily,
#     Bucket,
#     Quantile)


class UtilsTestCase(unittest.TestCase):

    def setUp(self):

        # Counter test fields
        self.counter_metric_name = 'logged_users_total'
        self.counter_metric_help = 'Logged users in the application.'
        self.counter_metric_type = pmp.COUNTER
        self.counter_metric_data = (
            ({'country': "sp", "device": "desktop"}, 520),
            ({'country': "us", "device": "mobile"}, 654),
            ({'country': "uk", "device": "desktop"}, 1001),
            ({'country': "de", "device": "desktop"}, 995),
            ({'country': "zh", "device": "desktop"}, 520),
        )

        # Gauge test fields
        self.gauge_metric_name = 'logged_users_total'
        self.gauge_metric_help = 'Logged users in the application.'
        self.gauge_metric_type = pmp.GAUGE
        self.gauge_metric_data = (
            ({'country': "sp", "device": "desktop"}, 520),
            ({'country': "us", "device": "mobile"}, 654),
            ({'country': "uk", "device": "desktop"}, 1001),
            ({'country': "de", "device": "desktop"}, 995),
            ({'country': "zh", "device": "desktop"}, 520),
        )

        # Summary test fields
        self.summary_metric_name = 'request_payload_size_bytes'
        self.summary_metric_help = 'Request payload size in bytes.'
        self.summary_metric_type = pmp.SUMMARY
        self.summary_metric_data = (
            ({'route': '/'}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, 'sum': 25.2, 'count': 4}),
            ({'route': '/data'}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, 'sum': 25.2, 'count': 4}),
        )

        # Histogram test fields
        self.histogram_metric_name = 'request_latency_seconds'
        self.histogram_metric_help = 'Request latency in seconds.'
        self.histogram_metric_type = pmp.HISTOGRAM
        # histogram data dict is composed as: {bucket upper bound: observations}
        POS_INF = float("inf")
        self.histogram_metric_data = (
            ({'route': '/'}, {5.0: 3, 10.0: 2, 15.0: 1, POS_INF: 0, 'count': 6, 'sum': 46.0}),
            ({'route': '/data'}, {5.0: 3, 10.0: 2, 15.0: 1, POS_INF: 0, 'count': 6, 'sum': 46.0}),
        )

        self.const_labels = {'app': 'my_app', 'host': 'examplehost'}

    def test_create_metric_using_invalid_type(self):
        ''' check using invalid metric type '''
        with self.assertRaises(Exception) as context:
            pmp.utils.create_metric_family(
                self.counter_metric_name,
                self.counter_metric_help,
                7,
                self.counter_metric_data)
        self.assertIn("Invalid metric_type", str(context.exception))

    def test_counter(self):
        ''' check creating counter using utils functions '''
        # Create a metrics with no metric instances
        mf = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            self.counter_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.counter_metric_name)
        self.assertEqual(mf.help, self.counter_metric_help)
        self.assertEqual(mf.type, self.counter_metric_type)

        # Create another and check equal
        mf_ = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            self.counter_metric_data)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        self.assertEqual(mf, mf_)

        for m in mf_.metric:
            self.assertEqual(m.timestamp_ms, 0)

        # Create another with timestamp
        mf_ = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            self.counter_metric_data,
            timestamp=True)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        for m in mf_.metric:
            self.assertNotEqual(m.timestamp_ms, 0)

        self.assertNotEqual(mf, mf_)

        # Create Counter with const_labels
        mf_ = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            self.counter_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

        # Check Counter can be round-tripped through encode and decode
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)

    def test_gauge(self):
        ''' check creating gauge using utils functions '''
        # Create a metrics with no metric instances
        mf = pmp.utils.create_metric_family(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_type,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.utils.create_metric_family(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_type,
            self.gauge_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.gauge_metric_name)
        self.assertEqual(mf.help, self.gauge_metric_help)
        self.assertEqual(mf.type, self.gauge_metric_type)

        # Create another and check equal
        mf_ = pmp.utils.create_metric_family(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_type,
            self.gauge_metric_data)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        self.assertEqual(mf, mf_)

        for m in mf_.metric:
            self.assertEqual(m.timestamp_ms, 0)

        # Create another with timestamp
        mf_ = pmp.utils.create_metric_family(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_type,
            self.gauge_metric_data,
            timestamp=True)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        for m in mf_.metric:
            self.assertNotEqual(m.timestamp_ms, 0)

        self.assertNotEqual(mf, mf_)

        # Create Gauge with const_labels
        mf_ = pmp.utils.create_metric_family(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_type,
            self.gauge_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

        # Check Gauge can be round-tripped through encode and decode
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)

    def test_summary(self):
        ''' check creating summary using utils functions '''
        # Create a metrics with no metric instances
        mf = pmp.utils.create_metric_family(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_type,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.utils.create_metric_family(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_type,
            self.summary_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.summary_metric_name)
        self.assertEqual(mf.help, self.summary_metric_help)
        self.assertEqual(mf.type, self.summary_metric_type)

        # Create another and check equal
        mf_ = pmp.utils.create_metric_family(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_type,
            self.summary_metric_data)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        self.assertEqual(mf, mf_)

        for m in mf_.metric:
            self.assertEqual(m.timestamp_ms, 0)

        # Create another with timestamp
        mf_ = pmp.utils.create_metric_family(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_type,
            self.summary_metric_data,
            timestamp=True)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        for m in mf_.metric:
            self.assertNotEqual(m.timestamp_ms, 0)

        self.assertNotEqual(mf, mf_)

        # Create Summary with const_labels
        mf_ = pmp.utils.create_metric_family(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_type,
            self.summary_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

        # Check Summary can be round-tripped through encode and decode
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)

    def test_histogram(self):
        ''' check creating histogram using utils functions '''
        # Create a metrics with no metric instances
        mf = pmp.utils.create_metric_family(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_type,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.utils.create_metric_family(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_type,
            self.histogram_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.histogram_metric_name)
        self.assertEqual(mf.help, self.histogram_metric_help)
        self.assertEqual(mf.type, self.histogram_metric_type)

        # Create another and check equal
        mf_ = pmp.utils.create_metric_family(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_type,
            self.histogram_metric_data)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        self.assertEqual(mf, mf_)

        for m in mf_.metric:
            self.assertEqual(m.timestamp_ms, 0)

        # Create another with timestamp
        mf_ = pmp.create_histogram(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_data,
            timestamp=True)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        for m in mf_.metric:
            self.assertNotEqual(m.timestamp_ms, 0)

        self.assertNotEqual(mf, mf_)

        # Create Histogram with const_labels
        mf_ = pmp.utils.create_metric_family(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_type,
            self.histogram_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

        # Check Histogram can be round-tripped through encode and decode
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)

    def test_equality(self):
        ''' simple confidence check of equality '''

        # Create a counter
        c1 = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            self.counter_metric_data)
        self.assertIsInstance(c1, pmp.MetricFamily)

        # Create another
        c2 = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            self.counter_metric_data)
        self.assertIsInstance(c2, pmp.MetricFamily)

        # they should be equal
        self.assertEqual(c1, c2)

        # Create another metric with the first metric label country modified
        # from 'sp' to 'es'
        modified_metric_data = []
        for index, metric_instance_data in enumerate(self.counter_metric_data):
            labels, value = metric_instance_data
            if index == 0:
                _labels = labels.copy()
                _labels['country'] = 'es'
                labels = _labels
            metric_instance_data = (labels, value)
            modified_metric_data.append(metric_instance_data)

        c3 = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            modified_metric_data)
        self.assertIsInstance(c3, pmp.MetricFamily)

        # They should not be equal
        self.assertNotEqual(c2, c3)

        # Create another metrics with the first metric value modified
        # from 520 to 521
        modified_metric_data = []
        for index, metric_instance_data in enumerate(self.counter_metric_data):
            labels, value = metric_instance_data
            if index == 0:
                value = 521
            metric_instance_data = (labels, value)
            modified_metric_data.append(metric_instance_data)

        c4 = pmp.utils.create_metric_family(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_type,
            modified_metric_data)
        self.assertIsInstance(c4, pmp.MetricFamily)

        # They should not be equal
        self.assertNotEqual(c2, c4)

    def test_create_labels(self):
        ''' check creating labels using utils functions '''
        test_labels = {'app': 'my_app', 'host': 'examplehost'}
        labels = pmp.utils.create_labels(test_labels)
        self.assertIsInstance(labels, list)
        self.assertTrue(all([isinstance(x, pmp.LabelPair) for x in labels]))

    def test_create_quantile(self):
        ''' check creating quantile using utils functions '''
        quantile = pmp.utils.create_quantile(0.5, 4.0)
        self.assertIsInstance(quantile, pmp.Quantile)

    def test_create_bucket(self):
        ''' check creating bucket using utils functions '''
        bucket = pmp.utils.create_bucket(3, 5.0)
        self.assertIsInstance(bucket, pmp.Bucket)

        POS_INF = float("inf")
        bucket = pmp.utils.create_bucket(0, POS_INF)
        self.assertIsInstance(bucket, pmp.Bucket)
