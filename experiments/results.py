"""
ARIA Results Generator
Executes all scenarios and exports results.csv
"""

import os
import pandas as pd

from experiments.runner import BenchmarkRunner


def main():

    print("=" * 80)
    print("ARIA Benchmark")
    print("=" * 80)

    runner = BenchmarkRunner()

    results = runner.run()

    df = pd.DataFrame(results)

    print()
    print(df)
    print()

    os.makedirs("results", exist_ok=True)

    csv_path = "results/results.csv"

    df.to_csv(

        csv_path,

        index=False

    )

    print("=" * 80)

    print(f"Results saved to {csv_path}")

    print("=" * 80)

    return df


if __name__ == "__main__":

    main()
    