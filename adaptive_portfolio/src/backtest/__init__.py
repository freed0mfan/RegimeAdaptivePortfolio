"""Модуль бэктестирования."""
from .engine import Backtester, BacktestResult
from .metrics import PerformanceMetrics
from .stats import StatisticsModule
from .strategies import (
    ALL_BENCHMARKS,
    BaseStrategy,
    EqualWeightStrategy,
    ImoexStrategy,
    MaxSharpeStrategy,
    MinVarianceStrategy,
    RiskParityStrategy,
    StaticMVOStrategy,
    build_strategy,
)

__all__ = [
    "Backtester",
    "BacktestResult",
    "PerformanceMetrics",
    "StatisticsModule",
    "BaseStrategy",
    "EqualWeightStrategy",
    "ImoexStrategy",
    "StaticMVOStrategy",
    "RiskParityStrategy",
    "MinVarianceStrategy",
    "MaxSharpeStrategy",
    "build_strategy",
    "ALL_BENCHMARKS",
]
