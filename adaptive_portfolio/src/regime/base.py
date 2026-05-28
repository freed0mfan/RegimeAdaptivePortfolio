"""Базовый интерфейс модели режимов и датакласс параметров."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import pandas as pd


@dataclass
class RegimeParams:
    """Параметры марков-переключающейся модели."""

    k: int
    mu: np.ndarray  # shape (K,)
    sigma2: np.ndarray  # shape (K,)
    transition_matrix: np.ndarray  # shape (K, K)
    stationary_dist: np.ndarray  # shape (K,)
    log_likelihood: float
    aic: float
    bic: float
    n_obs: int
    extra: dict = field(default_factory=dict)


def stationary_distribution(P: np.ndarray) -> np.ndarray:
    """Стационарное распределение марковской цепи: левый собственный вектор."""
    K = P.shape[0]
    # eigenvectors of P^T at eigenvalue 1
    vals, vecs = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(vals - 1.0))
    pi = np.real(vecs[:, idx])
    pi = pi / pi.sum()
    pi = np.where(pi < 0, 0.0, pi)
    s = pi.sum()
    if s <= 0:
        return np.ones(K) / K
    return pi / s


class RegimeModel(ABC):
    """Абстрактный интерфейс модели идентификации режимов."""

    def __init__(self, k_regimes: int = 2, random_state: int = 42):
        if k_regimes < 1:
            raise ValueError("k_regimes должно быть >= 1")
        self.k_regimes = int(k_regimes)
        self.random_state = int(random_state)
        self._fitted = False
        self._params: Optional[RegimeParams] = None
        self._returns_index: Optional[pd.Index] = None

    @abstractmethod
    def fit(self, returns: pd.Series) -> "RegimeModel":
        """Оценить модель на ряде доходностей."""

    @abstractmethod
    def get_filtered_proba(self, returns: pd.Series) -> pd.DataFrame:
        """Фильтрованные апостериорные вероятности (online)."""

    @abstractmethod
    def get_smoothed_proba(self, returns: pd.Series) -> pd.DataFrame:
        """Сглаженные апостериорные вероятности (offline)."""

    @abstractmethod
    def predict_next(self, last_return: float) -> np.ndarray:
        """Прогноз вероятностей режимов для следующего шага."""

    def get_regime_params(self) -> RegimeParams:
        if not self._fitted or self._params is None:
            raise RuntimeError("Модель не обучена. Вызовите fit() сначала.")
        return self._params
