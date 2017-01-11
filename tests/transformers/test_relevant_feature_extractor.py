# -*- coding: utf-8 -*-
# This file as well as the whole tsfresh package are licenced under the MIT licence (see the LICENCE.txt)
# Maximilian Christ (maximilianchrist.com), Blue Yonder Gmbh, 2016

import pandas as pd
from tests.fixtures import DataTestCase
from tsfresh.feature_extraction import ComprehensiveFCParameters
from tsfresh.transformers.relevant_feature_augmenter import RelevantFeatureAugmenter


class RelevantFeatureAugmenterTestCase(DataTestCase):
    def setUp(self):
        self.test_df = self.create_test_data_sample()
        para_map = {"length": None}
        self.kind_to_para_map = {"a": para_map.copy(),
                                                     "b": para_map.copy()}

    def test_not_fitted(self):
        augmenter = RelevantFeatureAugmenter()

        X = pd.DataFrame()

        self.assertRaises(RuntimeError, augmenter.transform, X)

    def test_no_timeseries(self):
        augmenter = RelevantFeatureAugmenter()

        X = pd.DataFrame()
        y = pd.Series()

        self.assertRaises(RuntimeError, augmenter.fit, X, y)

    def test_nothing_relevant(self):
        augmenter = RelevantFeatureAugmenter(kind_to_para_map=self.kind_to_para_map,
                                             column_value="val", column_id="id", column_sort="sort",
                                             column_kind="kind")

        y = pd.Series({10: 1, 500: 0})
        X = pd.DataFrame(index=[10, 500])

        augmenter.set_timeseries_container(self.test_df)
        augmenter.fit(X, y)

        transformed_X = augmenter.transform(X.copy())

        self.assertEqual(list(transformed_X.columns), [])
        self.assertEqual(list(transformed_X.index), list(X.index))

    def test_impute_works(self):
        self.kind_to_para_map["a"].update({"kurtosis": None})

        augmeter = RelevantFeatureAugmenter(kind_to_para_map=self.kind_to_para_map,
                                            column_value="val", column_id="id", column_sort="sort",
                                            column_kind="kind")

        y = pd.Series({10: 1, 500: 0})
        X = pd.DataFrame(index=[10, 500])

        augmeter.set_timeseries_container(self.test_df)
        augmeter.fit(X, y)

        transformed_X = augmeter.transform(X.copy())

        self.assertEqual(list(transformed_X.columns), [])
        self.assertEqual(list(transformed_X.index), list(X.index))