"""Консольный интерфейс аналитической станции временных рядов (вариант Б)."""

from well_series import analytics, config


def render_bar(val: float, min_v: float, max_v: float) -> str:
    """Строит текстовую полоску # пропорционально значению в диапазоне [min_v; max_v]."""
    span = max_v - min_v
    if span <= 0:
        return "#" * 10
    ratio = (val - min_v) / span
    count = 1 + int(round(ratio * (config.BAR_MAX_WIDTH - 1)))
    return "#" * count

def main() -> None:
    print("АНАЛИТИЧЕСКАЯ СТАНЦИЯ ОБРАБОТКИ ВРЕМЕННЫХ РЯДОВ (ВАРИАНТ Б)")
    print("=" * 72)
    raw = input("Введите ваш номер по журналу N: ").strip()
    student_n = int(raw) if raw.isdigit() and int(raw) > 0 else 5

    rates = analytics.build_series_12d(student_n)
    mean_v = analytics.calc_mean(rates)
    med_v = analytics.calc_median(rates)
    min_v, max_v, rng_v = analytics.calc_extremes_and_range(rates)

    sma3 = analytics.calc_sma_aligned(rates, config.SHORT_WINDOW)
    sma5 = analytics.calc_sma_aligned(rates, config.LONG_WINDOW)
    trend_str = analytics.detect_trend(sma3)

    print(f"\nХронологический ряд (12 сут.): {rates}")
    print("-" * 72)
    print(f"Среднее: {mean_v:.2f} | Медиана: {med_v:.2f} | Разница (Среднее - Медиана): {mean_v -
    med_v:+.2f}")
    print(f"Минимум: {min_v:.2f} | Максимум: {max_v:.2f} | Размах вариации R: {rng_v:.2f} м³/сут")
    print(f"Оценка тренда по SMA({config.SHORT_WINDOW}): {trend_str}")
    print("\nСВОДНАЯ ТАБЛИЦА СГЛАЖИВАНИЯ И ВИЗУАЛИЗАЦИИ РЯДА")
    print("-" * 72)
    print(f"{'День':<6}{'Q факт':>10}{'SMA(3)':>10}{'SMA(5)':>10}{'Откл. от SMA(3)':>16} {'Профиль дебита'}")
    print("-" * 72)

    for idx, q in enumerate(rates):
        day = idx + 1
        s3 = sma3[idx]
        s5 = sma5[idx]
        s3_str = f"{s3:10.2f}" if s3 is not None else f"{'—':>10}"
        s5_str = f"{s5:10.2f}" if s5 is not None else f"{'—':>10}"
        dev_str = f"{q - s3:+16.2f}" if s3 is not None else f"{'—':>16}"
        bar = render_bar(q, min_v, max_v)
        print(f"{day:<6}{q:>10.2f}{s3_str}{s5_str}{dev_str} {bar}")


if __name__ == "__main__":
    main()