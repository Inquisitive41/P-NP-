import numpy as np
import matplotlib.pyplot as plt

# Базовые параметры
OMICRON_INF = 10**73030
UPSILON_INF = 10**36518
G_TOTAL_BASE = 231_000_000
N_INF = 1.799e6
PHI = 1.618
C_META2_BASE = 617
C_13 = 479
SQRT2 = np.sqrt(2)
PI = np.pi
D_OMICRON_BASE = 1.92
C_META = 15
S_INF_BASE = 3.736
H_INF = 1.055e-34
C_INF = 3e8
K_INF = 1.381e-23
T_COSMO_BASE = 2.7
T_INF = 1.0  # Интегрируем по 1 секунде

def compute_rho(G_total, C_meta2, D_omicron, S_inf, T_cosmo):
    # Аргумент косинуса
    cos_arg = 2 * PI * (N_INF * PI * PHI * C_meta2) / (C_13 * SQRT2 * D_omicron)
    cos_val = 0.5  # Среднее значение из-за высокой частоты

    # Экспонента
    exp_arg = (G_total * H_INF * C_INF) / (C_META * K_INF * T_cosmo * S_inf)
    exp_val = np.exp(exp_arg)

    # Подынтегральное выражение
    f_t = OMICRON_INF * UPSILON_INF * cos_val * exp_val

    # Интеграл
    rho_infinity = f_t * T_INF

    return rho_infinity

# --- Тестирование ---
def run_benchmark():
    print("🚀 Запуск бенчмарка...")

    # 1. Изменение G_total
    g_values = np.linspace(1e8, 5e8, 5)
    rho_g = []
    for g in g_values:
        rho = compute_rho(g, C_META2_BASE, D_OMICRON_BASE, S_INF_BASE, T_COSMO_BASE)
        rho_g.append((g, rho))

    # 2. Изменение C_meta2
    c_values = np.linspace(500, 700, 5)
    rho_c = []
    for c in c_values:
        rho = compute_rho(G_TOTAL_BASE, c, D_OMICRON_BASE, S_INF_BASE, T_COSMO_BASE)
        rho_c.append((c, rho))

    # 3. Изменение D_omicron
    d_values = np.arange(1.8, 2.3, 0.1)
    rho_d = []
    for d in d_values:
        rho = compute_rho(G_TOTAL_BASE, C_META2_BASE, d, S_INF_BASE, T_COSMO_BASE)
        rho_d.append((d, rho))

    # 4. Изменение S_inf
    s_values = np.arange(1, 10, 1)
    rho_s = []
    for s in s_values:
        rho = compute_rho(G_TOTAL_BASE, C_META2_BASE, D_OMICRON_BASE, s, T_COSMO_BASE)
        rho_s.append((s, rho))

    # 5. Изменение T_cosmo
    t_values = np.arange(2, 5.5, 0.5)
    rho_t = []
    for t in t_values:
        rho = compute_rho(G_TOTAL_BASE, C_META2_BASE, D_OMICRON_BASE, S_INF_BASE, t)
        rho_t.append((t, rho))

    return {
        "rho_g": rho_g,
        "rho_c": rho_c,
        "rho_d": rho_d,
        "rho_s": rho_s,
        "rho_t": rho_t
    }

# --- Визуализация ---
def plot_benchmarks(results):
    fig, axs = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle("📊 Бенчмарк: Чувствительность $ \\Rho^{\\infty} $ к параметрам", fontsize=16)

    def log_plot(ax, data, xlabel, ylabel="log(ρ^∞)", title=""):
        x, y = zip(*data)
        ax.plot(x, np.log10(y), 'o-', color='teal')
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.set_title(title)

    log_plot(axs[0, 0], results["rho_g"], "$ G_{total} $", title="Влияние $ G_{total} $")
    log_plot(axs[0, 1], results["rho_c"], "$ C_{meta2} $", title="Влияние $ C_{meta2} $")
    log_plot(axs[0, 2], results["rho_d"], "$ D_{\\Omicron} $", title="Влияние $ D_{\\Omicron} $")
    log_plot(axs[1, 0], results["rho_s"], "$ S^{\\infty} $", title="Влияние $ S^{\\infty} $")
    log_plot(axs[1, 1], results["rho_t"], "$ T^{\\infty} $", title="Влияние $ T^{\\infty} $")

    for i in range(2):
        for j in range(3):
            if i == 1 and j == 2:
                axs[i, j].axis('off')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

# --- Запуск бенчмарка ---
results = run_benchmark()
plot_benchmarks(results)