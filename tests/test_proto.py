import datetime
import time
import unittest

import prometheus_metrics_proto as pmp


class TestProtobufFormat(unittest.TestCase):

    # Test Utils
    def _create_protobuf_object(self, data, metrics, metric_type, ts=False):
        pb_metrics = []
        for i in metrics:
            labels = [pmp.LabelPair(name=k, value=v) for k, v in i[0].items()]

            if metric_type == pmp.COUNTER:
                metric = pmp.Metric(
                    counter=pmp.Counter(value=i[1]),
                    label=labels)
            elif metric_type == pmp.GAUGE:
                metric = pmp.Metric(
                    gauge=pmp.Gauge(value=i[1]),
                    label=labels)
            elif metric_type == pmp.SUMMARY:
                quantiles = []

                for k, v in i[1].items():
                    if not isinstance(k, str):
                        q = pmp.Quantile(quantile=k, value=v)
                        quantiles.append(q)

                metric = pmp.Metric(
                    summary=pmp.Summary(quantile=quantiles,
                                        sample_sum=i[1]['sum'],
                                        sample_count=i[1]['count']),
                    label=labels)
            elif metric_type == pmp.HISTOGRAM:
                buckets = []

                for k, v in i[1].items():
                    if not isinstance(k, str):
                        bucket = pmp.Bucket(
                            cumulative_count=v, upper_bound=k)
                        buckets.append(bucket)

                metric = pmp.Metric(
                    summary=pmp.Histogram(buckets=buckets,
                                          histogram_sum=i[1]['sum'],
                                          histogram_count=i[1]['count']),
                    label=labels)

            else:
                raise TypeError("Not a valid metric")

            if ts:
                metric.timestamp_ms = int(
                    datetime.datetime.now(
                        tz=datetime.timezone.utc).timestamp() * 1000)

            pb_metrics.append(metric)

        valid_result = pmp.MetricFamily(
            name=data['name'],
            help=data['doc'],
            type=metric_type,
            metric=pb_metrics
        )

        return valid_result

    def _protobuf_metric_equal(self, ptb1, ptb2):
        if ptb1 is ptb2:
            return True

        if not ptb1 or not ptb2:
            return False

        # start all the filters
        # 1st level:  Metric Family
        if (ptb1.name != ptb2.name) or\
           (ptb1.help != ptb2.help) or\
           (ptb1.type != ptb2.type) or\
           (len(ptb1.metric) != len(ptb2.metric)):
            return False

        def sort_metric(v):
            """ Small function to order the lists of protobuf """
            x = sorted(v.label, key=lambda x: x.name + x.value)
            return("".join([i.name + i.value for i in x]))

        # Before continuing, sort stuff
        mts1 = sorted(ptb1.metric, key=sort_metric)
        mts2 = sorted(ptb2.metric, key=sort_metric)

        # Now that they are ordered we can compare each element with each
        for k, m1 in enumerate(mts1):
            m2 = mts2[k]

            # Check ts
            if m1.timestamp_ms != m2.timestamp_ms:
                return False

            # Check value
            if ptb1.type == pmp.COUNTER and ptb2.type == pmp.COUNTER:
                if m1.counter.value != m2.counter.value:
                    return False
            elif ptb1.type == pmp.GAUGE and ptb2.type == pmp.GAUGE:
                if m1.gauge.value != m2.gauge.value:
                    return False
            elif ptb1.type == pmp.SUMMARY and ptb2.type == pmp.SUMMARY:
                mm1, mm2 = m1.summary, m2.summary
                if ((mm1.sample_count != mm2.sample_count) or
                        (mm1.sample_sum != mm2.sample_sum)):
                    return False

                # order quantiles to test
                mm1_quantiles = sorted(
                    [(x.quantile, x.value) for x in mm1.quantile])
                mm2_quantiles = sorted(
                    [(x.quantile, x.value) for x in mm2.quantile])

                if mm1_quantiles != mm2_quantiles:
                    return False

            elif ptb1.type == pmp.HISTOGRAM and ptb2.type == pmp.HISTOGRAM:
                mm1, mm2 = m1.summary, m2.summary
                if ((mm1.sample_count != mm2.sample_count) or
                        (mm1.sample_sum != mm2.sample_sum)):
                    return False

                # order buckets to test
                # mm1_buckets = sorted(mm1.bucket, key=lambda x: x.bucket)
                mm1_buckets = sorted(
                    [(x.upper_bound, x.cumulative_count) for x in mm1.bucket])
                # mm2_buckets = sorted(mm2.bucket, key=lambda x: x.bucket)
                mm2_buckets = sorted(
                    [(x.upper_bound, x.cumulative_count) for x in mm2.bucket])

                if mm1_buckets != mm2_buckets:
                    return False

            else:
                return False

            # Check labels
            # Sort labels
            l1 = sorted(m1.label, key=lambda x: x.name + x.value)
            l2 = sorted(m2.label, key=lambda x: x.name + x.value)
            if not all([l.name == l2[k].name and l.value == l2[k].value for k, l in enumerate(l1)]):
                return False

        return True

    def test_create_protobuf_object_wrong(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        values = (
            ({'country': "sp", "device": "desktop"}, 520),
            ({'country': "us", "device": "mobile"}, 654),
        )

        with self.assertRaises(TypeError) as context:
            self._create_protobuf_object(data, values, 7)

        self.assertEqual("Not a valid metric", str(context.exception))

    def test_test_timestamp(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        values = (
            ({'country': "sp", "device": "desktop"}, 520),
            ({'country': "us", "device": "mobile"}, 654),
        )

        c = self._create_protobuf_object(data, values, pmp.COUNTER)
        for i in c.metric:
            self.assertEqual(0, i.timestamp_ms)

        c = self._create_protobuf_object(data, values, pmp.COUNTER, True)
        for i in c.metric:
            self.assertIsNotNone(i.timestamp_ms)

        self.assertEqual(c, c)
        self.assertTrue(self._protobuf_metric_equal(c, c))
        time.sleep(0.1)
        c2 = self._create_protobuf_object(data, values, pmp.COUNTER, True)
        self.assertFalse(self._protobuf_metric_equal(c, c2))

    def test_test_protobuf_metric_equal_not_metric(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        values = (({"device": "mobile", 'country': "us"}, 654),
                  ({'country': "sp", "device": "desktop"}, 520))
        pt1 = self._create_protobuf_object(data, values, pmp.COUNTER)

        self.assertFalse(self._protobuf_metric_equal(pt1, None))
        self.assertFalse(self._protobuf_metric_equal(None, pt1))

    def test_test_protobuf_metric_equal_not_basic_data(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        pt1 = self._create_protobuf_object(data, (), pmp.COUNTER)

        data2 = data.copy()
        data2['name'] = "other"
        pt2 = self._create_protobuf_object(data2, (), pmp.COUNTER)
        self.assertFalse(self._protobuf_metric_equal(pt1, pt2))

        data2 = data.copy()
        data2['doc'] = "other"
        pt2 = self._create_protobuf_object(data2, (), pmp.COUNTER)
        self.assertFalse(self._protobuf_metric_equal(pt1, pt2))

        pt2 = self._create_protobuf_object(data, (), pmp.SUMMARY)
        self.assertFalse(self._protobuf_metric_equal(pt1, pt2))

        pt3 = self._create_protobuf_object(data, (), pmp.HISTOGRAM)
        self.assertFalse(self._protobuf_metric_equal(pt2, pt3))

    def test_test_protobuf_metric_equal_not_labels(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        values = (({"device": "mobile", 'country': "us"}, 654),)
        pt1 = self._create_protobuf_object(data, values, pmp.COUNTER)

        values2 = (({"device": "mobile", 'country': "es"}, 654),)
        pt2 = self._create_protobuf_object(data, values2, pmp.COUNTER)

        self.assertFalse(self._protobuf_metric_equal(pt1, pt2))

    def test_test_protobuf_metric_equal_counter(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        counter_data = (
            {
                'pt1': (({'country': "sp", "device": "desktop"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'pt2': (({'country': "sp", "device": "desktop"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': True
            },
            {
                'pt1': (({'country': "sp", "device": "desktop"}, 521),
                        ({'country': "us", "device": "mobile"}, 654),),
                'pt2': (({'country': "sp", "device": "desktop"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': False
            },
            {
                'pt1': (({'country': "sp", "device": "desktop"}, 520),
                        ({"device": "mobile", 'country': "us"}, 654),),
                'pt2': (({"device": "desktop", 'country': "sp"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': True
            },
            {
                'pt1': (({"device": "mobile", 'country': "us"}, 654),
                        ({'country': "sp", "device": "desktop"}, 520)),
                'pt2': (({"device": "desktop", 'country': "sp"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': True
            },
        )

        for i in counter_data:
            p1 = self._create_protobuf_object(data, i['pt1'], pmp.COUNTER)
            p2 = self._create_protobuf_object(data, i['pt2'], pmp.COUNTER)

            if i['ok']:
                self.assertTrue(self._protobuf_metric_equal(p1, p2))
            else:
                self.assertFalse(self._protobuf_metric_equal(p1, p2))

    def test_test_protobuf_metric_equal_gauge(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        gauge_data = (
            {
                'pt1': (({'country': "sp", "device": "desktop"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'pt2': (({'country': "sp", "device": "desktop"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': True
            },
            {
                'pt1': (({'country': "sp", "device": "desktop"}, 521),
                        ({'country': "us", "device": "mobile"}, 654),),
                'pt2': (({'country': "sp", "device": "desktop"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': False
            },
            {
                'pt1': (({'country': "sp", "device": "desktop"}, 520),
                        ({"device": "mobile", 'country': "us"}, 654),),
                'pt2': (({"device": "desktop", 'country': "sp"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': True
            },
            {
                'pt1': (({"device": "mobile", 'country': "us"}, 654),
                        ({'country': "sp", "device": "desktop"}, 520)),
                'pt2': (({"device": "desktop", 'country': "sp"}, 520),
                        ({'country': "us", "device": "mobile"}, 654),),
                'ok': True
            },
        )

        for i in gauge_data:
            p1 = self._create_protobuf_object(data, i['pt1'], pmp.GAUGE)
            p2 = self._create_protobuf_object(data, i['pt2'], pmp.GAUGE)

            if i['ok']:
                self.assertTrue(self._protobuf_metric_equal(p1, p2))
            else:
                self.assertFalse(self._protobuf_metric_equal(p1, p2))

    def test_test_protobuf_metric_equal_summary(self):
        data = {
            'name': "logged_users_total",
            'doc': "Logged users in the application",
        }

        summary_data = (
            {
                'pt1': (({'interval': "5s"}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4}),
                        ({'interval': "10s"}, {0.5: 90, 0.9: 149, 0.99: 150, "sum": 385, "count": 10}),),
                'pt2': (({'interval': "10s"}, {0.5: 90, 0.9: 149, 0.99: 150, "sum": 385, "count": 10}),
                        ({'interval': "5s"}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4})),
                'ok': True
            },
            {
                'pt1': (({'interval': "5s"}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4}),
                        ({'interval': "10s"}, {0.5: 90, 0.9: 149, 0.99: 150, "sum": 385, "count": 10}),),
                'pt2': (({'interval': "5s"}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4}),
                        ({'interval': "10s"}, {0.5: 90, 0.9: 150, 0.99: 150, "sum": 385, "count": 10}),),
                'ok': False
            },
            {
                'pt1': (({'interval': "5s"}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4}),
                        ({'interval': "10s"}, {0.5: 90, 0.9: 149, 0.99: 150, "sum": 385, "count": 10}),),
                'pt2': (({'interval': "5s"}, {0.5: 4.0, 0.9: 5.2, 0.99: 5.2, "sum": 25.2, "count": 4}),
                        ({'interval': "10s"}, {0.5: 90, 0.9: 149, 0.99: 150, "sum": 385, "count": 11}),),
                'ok': False
            },
        )

        for i in summary_data:
            p1 = self._create_protobuf_object(data, i['pt1'], pmp.SUMMARY)
            p2 = self._create_protobuf_object(data, i['pt2'], pmp.SUMMARY)

            if i['ok']:
                self.assertTrue(self._protobuf_metric_equal(p1, p2))
            else:
                self.assertFalse(self._protobuf_metric_equal(p1, p2))
