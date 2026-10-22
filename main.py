import timeit
from boyer_moore import boyer_moore_search
from kmp import kmp_search
from rabin_karp import rabin_karp_search

def load_file(filename):
    encodings = ['utf-8', 'cp1251', 'windows-1251', 'latin-1']
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Неможливо прочитати файл {filename} жодним із підтримуваних кодувань.")


def benchmark_algorithms(text, real_pattern, fake_pattern, number=1000):
    """Вимірює час виконання алгоритмів за допомогою timeit."""
    algorithms = {
        "Боєр-Мур": boyer_moore_search,
        "Кнут-Морріс-Пратт": kmp_search,
        "Рабін-Карп": rabin_karp_search
    }
    
    results = {}
    
    for name, func in algorithms.items():
        # Час для існуючого підрядка
        time_real = timeit.timeit(lambda: func(text, real_pattern), number=number)
        # Час для вигаданого підрядка
        time_fake = timeit.timeit(lambda: func(text, fake_pattern), number=number)
        
        results[name] = {
            "real": time_real,
            "fake": time_fake,
            "total": time_real + time_fake  # Для визначення найшвидшого алгоритму враховуємо суму обох часів
        }
        
    return results

def print_results(article_name, results):
    print(f"\n{'='*15} Результати для: {article_name} {'='*15}")
    print(f"{'Алгоритм':<20} | {'Існуючий підрядок (сек)':<25} | {'Вигаданий підрядок (сек)':<25} | {'Сума (сек)':<12}")
    print("-" * 90)
    
    fastest_overall = None
    min_time = float('inf')
    
    for algo, data in results.items():
        print(f"{algo:<20} | {data['real']:<25.6f} | {data['fake']:<25.6f} | {data['total']:<12.6f}")
        if data['total'] < min_time:
            min_time = data['total']
            fastest_overall = algo
            
    print("-" * 90)
    print(f"🏆 Найшвидший алгоритм для {article_name}: {fastest_overall}")
    return fastest_overall

def main():
    try:
        text1 = load_file("стаття 1.txt")
        text2 = load_file("стаття 2.txt")
    except FileNotFoundError as e:
        print(f"Помилка: {e}. Не знайшов файли стаття 1.txt та стаття 2.txt у папці зі скриптом.")
        return

    # Підрядки для тестування
    real_pattern_1 = "алгоритм" 
    fake_pattern_1 = "ОлексійМарченко1234567890"  # вигаданий рядок, який не зустрічається в тексті

    real_pattern_2 = "даних"
    fake_pattern_2 = "тестовийрядокякийніколиневзустрінеться"  # вигаданий рядок, який не зустрічається в тексті

    print("Запуск бенчмарку (timeit виконає кожну функцію по 1000 разів)...")
    
    results1 = benchmark_algorithms(text1, real_pattern_1, fake_pattern_1)
    results2 = benchmark_algorithms(text2, real_pattern_2, fake_pattern_2)

    fastest1 = print_results("Стаття 1", results1)
    fastest2 = print_results("Стаття 2", results2)

    print(f"\n{'='*40}")
    print(f"🏁 Загальний підсумок:")
    print(f"- Найшвидший для Статті 1: {fastest1}")
    print(f"- Найшвидший для Статті 2: {fastest2}")
    if fastest1 == fastest2:
        print(f"🌟 Абсолютний переможець загалом: {fastest1}")
    else:
        print("🌟 Абсолютний переможець залежить від структури тексту конкретної статті.")
    print(f"{'='*40}")

if __name__ == "__main__":
    main()