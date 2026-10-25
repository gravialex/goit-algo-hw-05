import timeit
from boyer_moore import boyer_moore_search
from kmp import kmp_search
from rabin_karp import rabin_karp_search

def load_file(filename):
    """Безпечне завантаження файлу з перебором кодувань."""
    for encoding in ['utf-8', 'cp1251', 'windows-1251', 'latin-1']:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Неможливо прочитати файл {filename}.")

def benchmark(text, real_pattern, fake_pattern, number=1000):
    """Вимірює час виконання трьох алгоритмів."""
    algorithms = {
        "Боєр-Мур": boyer_moore_search,
        "Кнут-Морріс-Пратт": kmp_search,
        "Рабін-Карп": rabin_karp_search
    }
    
    real_results = {}
    fake_results = {}
    total_results = {}
    
    for name, func in algorithms.items():
        t_real = timeit.timeit(lambda: func(text, real_pattern), number=number)
        t_fake = timeit.timeit(lambda: func(text, fake_pattern), number=number)
        
        real_results[name] = t_real
        fake_results[name] = t_fake
        total_results[name] = t_real + t_fake
        
    return real_results, fake_results, total_results

def main():
    try:
        text1 = load_file("стаття1.txt")
        text2 = load_file("стаття2.txt")
    except FileNotFoundError as e:
        print(f"Помилка: {e}. Перевірте наявність файлів 'Стаття 1.txt' та 'Стаття 2.txt' у поточній директорії.")
        return

    # Підрядки для тестування (замініть на слова зі своїх статей)
    real_p1, fake_p1 = "алгоритм", "ОлексійМарченко1234567890"
    real_p2, fake_p2 = "даних", "тестовийрядокякийніколиневзустрінеться"

    print("Вимірюю час виконання (1000 ітерацій)...")
    
    real1, fake1, total1 = benchmark(text1, real_p1, fake_p1)
    real2, fake2, total2 = benchmark(text2, real_p2, fake_p2)

    # Вивід результатів для Статті 1
    print("=== СТАТТЯ 1 ===")
    print("Час для існуючого підрядка:", real1)
    print("Час для вигаданого підрядка:", fake1)
    print("Найшвидший для існуючого:", min(real1, key=real1.get))
    print("Найшвидший для вигаданого:", min(fake1, key=fake1.get))
    print("Найшвидший в цілому (сума):", min(total1, key=total1.get))
    
    print("\n=== СТАТТЯ 2 ===")
    print("Час для існуючого підрядка:", real2)
    print("Час для вигаданого підрядка:", fake2)
    print("Найшвидший для існуючого:", min(real2, key=real2.get))
    print("Найшвидший для вигаданого:", min(fake2, key=fake2.get))
    print("Найшвидший в цілому (сума):", min(total2, key=total2.get))

if __name__ == "__main__":
    main()