"""
============================================================
ARIA Research Prototype
Benchmark Configuration
============================================================
Central configuration for all experiments.
"""

from dataclasses import dataclass


@dataclass
class BenchmarkConfig:
    """
    Global benchmark configuration.
    """

    # ==========================================================
    # Experiment Settings
    # ==========================================================

    repetitions: int = 30

    random_seed: int = 42

    # ==========================================================
    # Scalability Experiments
    # ==========================================================

    agent_counts = [
        1,
        10,
        25,
        50,
        100,
        250,
        500
    ]

    # ==========================================================
    # Statistics
    # ==========================================================

    confidence_level: float = 0.95

    export_raw_results: bool = True

    export_statistics: bool = True

    # ==========================================================
    # Figure Generation
    # ==========================================================

    generate_figures: bool = True

    save_png: bool = True

    save_pdf: bool = True

    dpi: int = 600

    # ==========================================================
    # Output Directories
    # ==========================================================

    results_dir: str = "results"

    figures_dir: str = "figures"

    publication_dir: str = "figures/publication"

    # ==========================================================
    # Logging
    # ==========================================================

    verbose: bool = True