import csv
import os

FILENAME = "score.csv"


def load_best_times():
    best_times = {
        "Лёгкий": float("0"),
        "Средний": float("0"),
        "Сложный": float("0"),
        "Хардкор": float("0")
    }

    if os.path.exists(FILENAME):
        with open(FILENAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if len(row) == 2:
                    mode, time = row
                    try:
                        best_times[mode] = float(time)
                    except ValueError:
                        print(f"Ошибка")
    return best_times


def save_best_time(mode, new_time):
    best_times = load_best_times()

    mode_translation = {
        "easy": "Лёгкий",
        "medium": "Средний",
        "hard": "Сложный",
        "mega_hard": "Хардкор"
    }

    mode = mode_translation.get(mode, mode)

    if new_time > best_times[mode]:
        best_times[mode] = new_time

        try:
            with open(FILENAME, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Режим", "Время"])
                for mode, time in best_times.items():
                    writer.writerow([mode, time])

            with open(FILENAME, "r", newline="", encoding="utf-8") as file:
                print(file.read())

        except Exception as e:
            print(f"Ошибка при записи в файл {FILENAME}: {e}")
