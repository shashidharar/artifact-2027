"""
============================================================
ARIA Research Prototype
Repeated Benchmark Runner
============================================================
Executes benchmark multiple times and generates:
    - raw_results.csv
    - metrics.csv
    - aggregated_results.csv
============================================================
"""

import os
import random
import numpy as np
import pandas as pd

from experiments.runner import BenchmarkRunner
from experiments.benchmark_config import BenchmarkConfig

class RepeatedBenchmarkRunner:

    def __init__(self):

        self.cfg = BenchmarkConfig()

        random.seed(self.cfg.random_seed)

        np.random.seed(self.cfg.random_seed)

        os.makedirs(
            self.cfg.results_dir,
            exist_ok=True
        )

    ##########################################################
    # Execute repeated benchmark
    ##########################################################

    def run(self):

        benchmark = BenchmarkRunner()

        all_rows = []

        total_runs = self.cfg.repetitions

        print("=" * 80)
        print("ARIA REPEATED BENCHMARK")
        print("=" * 80)
        print(f"Repetitions : {total_runs}")
        print()

        for run in range(total_runs):

            print(f"Run {run+1}/{total_runs}")

            results = benchmark.run()

            df = pd.DataFrame(results)

            df["Run"] = run + 1

            all_rows.append(df)

        ######################################################
        # Merge all runs
        ######################################################

        raw_df = pd.concat(
            all_rows,
            ignore_index=True
        )

        raw_path = os.path.join(
            self.cfg.results_dir,
            "raw_results.csv"
        )

        raw_df.to_csv(
            raw_path,
            index=False
        )

        print()
        print("✓ raw_results.csv generated")

        ######################################################
        # Generate metrics
        ######################################################

        ######################################################
        ######################################################
        # Reload latest evaluation modules
        ######################################################

        import importlib

        import evaluation.metrics
        import evaluation.statistics

        importlib.reload(evaluation.metrics)
        importlib.reload(evaluation.statistics)

        MetricsEngine = evaluation.metrics.MetricsEngine
        StatisticsEngine = evaluation.statistics.StatisticsEngine

        ######################################################
        # Metrics
        ######################################################

        metrics_engine = MetricsEngine(
            csv_path=raw_path,
            output_dir=self.cfg.results_dir
        )

        metrics_engine.export()

        ######################################################
        # Statistics
        ######################################################

        stats_engine = StatisticsEngine(
            csv_path=os.path.join(
                self.cfg.results_dir,
                "metrics.csv"
            ),
            output_dir=self.cfg.results_dir
        )

        stats_engine.export()

        print()
        print("=" * 80)
        print("Benchmark completed successfully")
        print("=" * 80)

        return raw_df


##############################################################
# Standalone execution
##############################################################

if __name__ == "__main__":

    runner = RepeatedBenchmarkRunner()

    runner.run()