import math
import numpy as np

# Константы
OMICRON_INF = 10**73030
UPSILON_INF = 10**36518
G_TOTAL = 231_000_000
N_INF = 1.799e6
PHI = 1.618
C_META2 = 617
C_13 = 479
SQRT2 = math.sqrt(2)
PI = math.pi
D_OMICRON = 1.92
C_META = 15
S_INF = 3.736
H_INF = 1.055e-34
C_INF = 3e8
K_INF = 1.381e-23
T_COSMO = 2.7

# Расчёт аргумента косинуса
def compute_cos_arg():
    numerator = N_INF * PI * PHI * C_META2
    denominator = C_13 * SQRT2 * D_OMICRON
    theta = 2 * PI * (numerator / denominator)
    return theta

# Расчёт показателя экспоненты
def compute_exp_arg():
    numerator = G_TOTAL * H_INF * C_INF
    denominator = C_META * K_INF * T_COSMO * S_INF
    alpha = numerator / denominator
    return alpha

# Основная функция вычисления Rho^∞
def simulate_rho_infinity(T_INF=1.0):
    # Аргумент косинуса
    cos_arg = compute_cos_arg()
    cos_val = 0.5  # среднее значение при высокой частоте

    # Показатель экспоненты
    exp_arg = compute_exp_arg()
    exp_val = math.exp(exp_arg)

    # Подынтегральное выражение
    f_t = OMICRON_INF * UPSILON_INF * cos_val * exp_val

    # Интегрирование по времени (предположим T_INF = 1 секунда)
    rho_infinity = f_t * T_INF

    return {
        "cos_arg": cos_arg,
        "cos_val_avg": cos_val,
        "exp_arg": exp_arg,
        "exp_val": exp_val,
        "f(t)": f_t,
        "Rho^∞ (сек)": rho_infinity,
        "Rho^∞ (лет)": rho_infinity / (365 * 24 * 3600),
        "exp(α)": exp_val,
        "cos(θ)": cos_val,
        "OMICRON_INF": OMICRON_INF,
        "UPSILON_INF": UPSILON_INF
    }