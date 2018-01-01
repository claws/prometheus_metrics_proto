
import unittest

import prometheus_metrics_proto as pmp


class ApiTestCase(unittest.TestCase):

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
        # summary_metric_data_values = (3, 5.2, 13, 4)
        self.summary_metric_data = (
            ({'host': 'examplehost', 'route': '/'}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, 'sum': 25.2, 'count': 4}),
            ({'host': 'examplehost', 'route': '/data'}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, 'sum': 25.2, 'count': 4}),
        )

        # Histogram test fields
        self.histogram_metric_name = 'request_latency_seconds'
        self.histogram_metric_help = 'Request latency in seconds.'
        self.histogram_metric_type = pmp.HISTOGRAM
        # histogram_metric_data_values = (3, 5.2, 13, 4)
        # histogram data dict is composed as: {bucket upper bound: observations}
        POS_INF = float("inf")
        self.histogram_metric_data = (
            ({'host': 'examplehost', 'route': '/'}, {5.0: 3, 10.0: 2, 15.0: 1, POS_INF: 0, 'sum': 25.2, 'count': 4}),
            ({'host': 'examplehost', 'route': '/data'}, {5.0: 3, 10.0: 2, 15.0: 1, POS_INF: 0, 'sum': 25.2, 'count': 4}),
        )

        self.const_labels = {"app": "my_app"}

    def test_create_counter(self):
        ''' check creating counter using api functions '''
        # Create a metrics with no metric instances
        mf = pmp.create_counter(
            self.counter_metric_name,
            self.counter_metric_help,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.create_counter(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.counter_metric_name)
        self.assertEqual(mf.help, self.counter_metric_help)
        self.assertEqual(mf.type, self.counter_metric_type)

        # Create another and check equal
        mf_ = pmp.create_counter(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_data)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        self.assertEqual(mf, mf_)

        for m in mf_.metric:
            self.assertEqual(m.timestamp_ms, 0)

        # Create another with timestamp
        mf_ = pmp.create_counter(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_data,
            timestamp=True)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        for m in mf_.metric:
            self.assertNotEqual(m.timestamp_ms, 0)

        self.assertNotEqual(mf, mf_)

        # Create Counter with const_labels
        mf_ = pmp.create_counter(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

    def test_create_gauge(self):
        ''' check creating gauge using api functions '''
        # Create a metrics with no metric instances
        mf = pmp.create_gauge(
            self.gauge_metric_name,
            self.gauge_metric_help,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.create_gauge(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.gauge_metric_name)
        self.assertEqual(mf.help, self.gauge_metric_help)
        self.assertEqual(mf.type, self.gauge_metric_type)

        mf_ = pmp.create_gauge(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_data)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        self.assertEqual(mf, mf_)

        for m in mf_.metric:
            self.assertEqual(m.timestamp_ms, 0)

        # Create another with timestamp
        mf_ = pmp.create_gauge(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_data,
            timestamp=True)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        for m in mf_.metric:
            self.assertNotEqual(m.timestamp_ms, 0)

        self.assertNotEqual(mf, mf_)

        # Create Gauge with const_labels
        mf_ = pmp.create_gauge(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

    def test_create_summary(self):
        ''' check creating summary using api functions '''
        # Create a metrics with no metric instances
        mf = pmp.create_summary(
            self.summary_metric_name,
            self.summary_metric_help,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.create_summary(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.summary_metric_name)
        self.assertEqual(mf.help, self.summary_metric_help)
        self.assertEqual(mf.type, self.summary_metric_type)

        mf_ = pmp.create_summary(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_data)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        self.assertEqual(mf, mf_)

        for m in mf_.metric:
            self.assertEqual(m.timestamp_ms, 0)

        # Create another with timestamp
        mf_ = pmp.create_summary(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_data,
            timestamp=True)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        for m in mf_.metric:
            self.assertNotEqual(m.timestamp_ms, 0)

        self.assertNotEqual(mf, mf_)

        # Create Summary with const_labels
        mf_ = pmp.create_summary(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

    def test_create_histogram(self):
        ''' check creating histogram using api functions '''
        # Create a metrics with no metric instances
        mf = pmp.create_histogram(
            self.histogram_metric_name,
            self.histogram_metric_help,
            [])
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(len(mf.metric), 0)

        # Create it with metrics
        mf = pmp.create_histogram(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_data)
        self.assertIsInstance(mf, pmp.MetricFamily)
        self.assertEqual(mf.name, self.histogram_metric_name)
        self.assertEqual(mf.help, self.histogram_metric_help)
        self.assertEqual(mf.type, self.histogram_metric_type)

        mf_ = pmp.create_histogram(
            self.histogram_metric_name,
            self.histogram_metric_help,
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
        mf_ = pmp.create_histogram(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_data,
            const_labels=self.const_labels)
        self.assertIsInstance(mf_, pmp.MetricFamily)

        # Check that const_label is present in the LabelPair associated
        # with each metric instance.
        for m in mf_.metric:
            labels = [lp.name for lp in m.label]
            self.assertIn('app', labels)

        self.assertNotEqual(mf, mf_)

    def test_encode_decode(self):
        ''' check encode and decode functions '''

        # check passing no metrics raises an exception
        input_metrics = None
        with self.assertRaises(Exception) as ctx:
            payload = pmp.encode(input_metrics)
        self.assertIn(
            'Expected metrics to be instances of MetricFamily, got ',
            str(ctx.exception))

        cm = pmp.create_counter(
            self.counter_metric_name,
            self.counter_metric_help,
            self.counter_metric_data)
        self.assertIsInstance(cm, pmp.MetricFamily)

        gm = pmp.create_gauge(
            self.gauge_metric_name,
            self.gauge_metric_help,
            self.gauge_metric_data)
        self.assertIsInstance(gm, pmp.MetricFamily)

        sm = pmp.create_summary(
            self.summary_metric_name,
            self.summary_metric_help,
            self.summary_metric_data)
        self.assertIsInstance(sm, pmp.MetricFamily)

        hm = pmp.create_histogram(
            self.histogram_metric_name,
            self.histogram_metric_help,
            self.histogram_metric_data)
        self.assertIsInstance(hm, pmp.MetricFamily)

        # check encode can take a single valid metric
        input_metrics = [cm]
        payload = pmp.encode(input_metrics[0])
        self.assertIsInstance(payload, bytes)
        # check round-trip
        metrics = pmp.decode(payload)
        self.assertIsInstance(metrics, list)
        self.assertEqual(len(metrics), len(input_metrics))
        for m_in, m_out in zip(input_metrics, metrics):
            self.assertEqual(m_in, m_out)

        # check passing invalid type raises an exception
        input_metrics = ['a']
        with self.assertRaises(Exception) as ctx:
            payload = pmp.encode(*input_metrics)
        self.assertIn(
            'Expected metrics to be instances of MetricFamily, got ',
            str(ctx.exception))

        # check parser can take multiple valid metrics
        input_metrics = (cm, gm, sm, hm)
        payload = pmp.encode(*input_metrics)
        self.assertIsInstance(payload, bytes)
        # check round-trip
        metrics = pmp.decode(payload)
        self.assertIsInstance(metrics, list)
        self.assertEqual(len(metrics), len(input_metrics))
        for m_in, m_out in zip(input_metrics, metrics):
            self.assertEqual(m_in, m_out)

        # check decoding empty bytes returns empty list
        metrics = pmp.decode(b'')
        self.assertIsInstance(metrics, list)
        self.assertEqual(len(metrics), 0)

    def test_encode_counter(self):
        ''' check encode of counter matches expected output '''
        valid_result = (b'[\n\x0ccounter_test\x12\nA counter.\x18\x00"=\n\r'
                        b'\n\x08c_sample\x12\x011\n\x10\n\x0bc_subsample\x12'
                        b'\x01b\n\x0f\n\x04type\x12\x07counter\x1a\t\t\x00\x00'
                        b'\x00\x00\x00\x00y@')
        metric_name = "counter_test"
        metric_help = "A counter."
        metric_type = pmp.COUNTER
        metric_data = (
            ({'c_sample': '1', 'c_subsample': 'b'}, 400),
        )
        mf = pmp.utils.create_metric_family(
            metric_name, metric_help, metric_type, metric_data,
            const_labels={'type': "counter"})
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        self.assertEqual(valid_result, payload)

        # Check Counter can be round-tripped through encode and decode
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)

    def test_encode_gauge(self):
        ''' check encode of gauge matches expected output '''
        valid_result = (b'U\n\ngauge_test\x12\x08A gauge.\x18\x01";'
                        b'\n\r\n\x08g_sample\x12\x011\n\x10\n\x0bg_subsample'
                        b'\x12\x01b\n\r\n\x04type\x12\x05gauge\x12\t\t\x00'
                        b'\x00\x00\x00\x00\x00\x89@')
        metric_name = "gauge_test"
        metric_help = "A gauge."
        metric_type = pmp.GAUGE
        metric_data = (
            ({'g_sample': '1', 'g_subsample': 'b'}, 800),
        )
        mf = pmp.utils.create_metric_family(
            metric_name, metric_help, metric_type, metric_data,
            const_labels={'type': "gauge"})
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        self.assertEqual(valid_result, payload)

        # Check Gauge can be round-tripped through encode and decode
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)

    def test_encode_summary(self):
        ''' check encode of summary matches expected output '''
        valid_result = (b'\x99\x01\n\x0csummary_test\x12\nA summary.'
                        b'\x18\x02"{\n\r\n\x08s_sample\x12\x011\n\x10\n'
                        b'\x0bs_subsample\x12\x01b\n\x0f\n\x04type\x12\x07'
                        b'summary"G\x08\x16\x11\x00\x00\x00\x00\x90"\xf8@'
                        b'\x1a\x12\t\x00\x00\x00\x00\x00\x00\xe0?\x11\x00'
                        b'\x00\x00\x00\x00\x8b\xb0@\x1a\x12\t\xcd\xcc\xcc'
                        b'\xcc\xcc\xcc\xec?\x11\x00\x00\x00\x00\x00v\xb1@'
                        b'\x1a\x12\t\xaeG\xe1z\x14\xae\xef?\x11\x00\x00\x00'
                        b'\x00\x00\xa5\xb1@')
        metric_name = "summary_test"
        metric_help = "A summary."
        metric_type = pmp.SUMMARY
        metric_data = (
            ({'s_sample': '1', 's_subsample': 'b'},
             {0.5: 4235.0, 0.9: 4470.0, 0.99: 4517.0, 'count': 22, 'sum': 98857.0}),
        )
        mf = pmp.utils.create_metric_family(
            metric_name, metric_help, metric_type, metric_data,
            const_labels={'type': "summary"})
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        self.assertEqual(valid_result, payload)

        # Check Summary can be round-tripped through encode and decode
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)

    def test_encode_histogram(self):
        ''' check encode of histogram matches expected output '''
        valid_result = (b'\x97\x01\n\x0ehistogram_test\x12\x0cA histogram.'
                        b'\x18\x04"u\n\r\n\x08h_sample\x12\x011\n\x10\n'
                        b'\x0bh_subsample\x12\x01b\n\x11\n\x04type\x12\t'
                        b'histogram:?\x08\x06\x11\x00\x00\x00\x00\x00\x00G@'
                        b'\x1a\x0b\x08\x03\x11\x00\x00\x00\x00\x00\x00\x14@'
                        b'\x1a\x0b\x08\x02\x11\x00\x00\x00\x00\x00\x00$@\x1a'
                        b'\x0b\x08\x01\x11\x00\x00\x00\x00\x00\x00.@\x1a\x0b'
                        b'\x08\x00\x11\x00\x00\x00\x00\x00\x00\xf0\x7f')
        metric_name = "histogram_test"
        metric_help = "A histogram."
        metric_type = pmp.HISTOGRAM
        # buckets typically have a POS_INF upper bound to catch values
        # beyond the largest bucket bound. Simulate this behavior.
        POS_INF = float("inf")
        metric_data = (
            ({'h_sample': '1', 'h_subsample': 'b'},
             {5.0: 3, 10.0: 2, 15.0: 1, POS_INF: 0, 'count': 6, 'sum': 46.0}),
        )
        mf = pmp.utils.create_metric_family(
            metric_name, metric_help, metric_type, metric_data,
            const_labels={'type': "histogram"})
        payload = pmp.encode(mf)
        self.assertIsInstance(payload, bytes)
        self.assertEqual(valid_result, payload)

        # Check Histogram can be round-tripped through encode and decode
        _mf = pmp.decode(payload)[0]
        self.assertEqual(mf, _mf)
