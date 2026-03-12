import RPi.GPIO as GPIO
import time

class R2R_ADC:
    """
    Класс для управления 8-битным ЦАП (R-2R лестница) и использования его
    для реализации АЦП последовательного счёта.
    """
    
    def init(self, dynamic_range, compare_time=0.01, verbose=False):
        """
        Конструктор класса.
        
        Аргументы:
            dynamic_range (float): Динамический диапазон ЦАП в вольтах (опорное напряжение).
            compare_time (float): Время задержки для стабилизации компаратора (в секундах).
            verbose (bool): Флаг для вывода отладочной информации.
        """
        self.dynamic_range = dynamic_range
        self.compare_time = compare_time
        self.verbose = verbose
        
        # Номера GPIO пинов для 8-битного ЦАП (R-2R лестница)
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        # Номер GPIO пина для компаратора (вход)
        self.comp_gpio = 21
        
        # Настройка GPIO
        GPIO.setmode(GPIO.BCM)
        # Настройка пинов ЦАП как выходов, начальное состояние 0
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=GPIO.LOW)
        # Настройка пина компаратора как входа
        GPIO.setup(self.comp_gpio, GPIO.IN)
        
        if self.verbose:
            print(f"Инициализация R2R_ADC: диапазон={dynamic_range}В, время сравнения={compare_time}с")
            print(f"GPIO битов ЦАП: {self.bits_gpio}")
            print(f"GPIO компаратора: {self.comp_gpio}")
    
    def del(self):
        """
        Деструктор класса. Очищает настройки GPIO и выставляет 0 на выходе ЦАП.
        """
        if self.verbose:
            print("Очистка GPIO и завершение работы...")
        # Выставляем 0 на всех пинах ЦАП
        self.number_to_dac(0)
        # Очищаем настройки GPIO
        GPIO.cleanup()
    
    def number_to_dac(self, number):
        """
        Подает целое число (0-255) на параллельный вход ЦАП.
        
        Аргументы:
            number (int): Число для установки на ЦАП (0-255).
        """
        if number < 0 or number > 255:
            raise ValueError("Число должно быть в диапазоне 0-255 для 8-битного ЦАП")
        
        if self.verbose:
            print(f"Установка числа {number} (0b{number:08b}) на ЦАП")
        
        # Для каждого бита числа устанавливаем соответствующий GPIO пин
        for i, gpio_pin in enumerate(self.bits_gpio):
            # Получаем значение i-го бита (начиная с младшего)
            bit_value = (number >> i) & 1
            GPIO.output(gpio_pin, bit_value)
    
    def sequential_counting_adc(self):
        """
        Реализация АЦП методом последовательного счета.
        
        Возвращает:
            int: Цифровое значение (0-255), соответствующее входному напряжению.
        """
        if self.verbose:
            print("Начало последовательного счета АЦП")
        
        # Последовательно подаем числа от 0 до 255 на ЦАП
        for code in range(256):
            # Устанавливаем текущее число на ЦАП
            self.number_to_dac(code)
            
            # Ждем, пока компаратор стабилизируется
            time.sleep(self.compare_time)
            
            # Читаем состояние компаратора
            # Предполагаем, что компаратор выдает 1, когда U_ЦАП < U_вх,
            # и 0, когда U_ЦАП >= U_вх (или наоборот - проверьте вашу схему!)
            comp_value = GPIO.input(self.comp_gpio)
            
            if self.verbose:
                print(f"  Код={code}, компаратор={comp_value}")
            
            # Если компаратор переключился (напряжение ЦАП превысило входное)
            # Примечание: логика зависит от подключения компаратора!
            # Предположим, что компаратор выдает 0, когда U_ЦАП >= U_вх
            if comp_value == 0:  # Измените условие согласно вашей схеме
            if self.verbose:
                    print(f"  Найдено значение: {code}")
                return code
        
        # Если превышение не найдено (входное напряжение выше максимума)
        if self.verbose:
            print(f"  Превышение не найдено, возвращаем максимум: 255")
        return 255
    
    def get_sc_voltage(self):
        """
        Измеряет напряжение методом последовательного счета и возвращает
        значение в вольтах.
        
        Возвращает:
            float: Измеренное напряжение в вольтах.
        """
        # Получаем цифровое значение
        digital_code = self.sequential_counting_adc()
        
        # Переводим в напряжение: U = (код / 255) * динамический диапазон
        voltage = (digital_code / 255.0) * self.dynamic_range
        
        if self.verbose:
            print(f"Измеренное напряжение: {voltage:.3f} В (код={digital_code})")
        
        return voltage


# Основной охранник модуля
if name == "main":
    # Динамический диапазон ЦАП (измерьте мультиметром ваше опорное напряжение!)
    # Например, если у вас опорное напряжение 3.3В, то dynamic_range = 3.3
    DYNAMIC_RANGE = 3.3  # ИЗМЕНИТЕ ЭТО ЗНАЧЕНИЕ ПОСЛЕ ИЗМЕРЕНИЯ!
    
    adc = None
    try:
        # Создаем объект АЦП
        print(f"Создание объекта R2R_ADC с диапазоном {DYNAMIC_RANGE}В")
        adc = R2R_ADC(dynamic_range=DYNAMIC_RANGE, compare_time=0.01, verbose=True)
        
        # Бесконечный цикл измерения напряжения
        print("Начинаем измерения напряжения. Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        while True:
            # Измеряем напряжение
            voltage = adc.get_sc_voltage()
            
            # Выводим результат в терминал
            print(f"Измеренное напряжение: {voltage:.3f} В")
            
            # Небольшая пауза между измерениями
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nИзмерения прерваны пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        # Деструктор будет вызван автоматически при удалении объекта,
        # но для надежности вызываем cleanup явно через удаление объекта
        if adc:
            # Можно явно вызвать деструктор, но лучше просто удалить ссылку
            # и позволить сборщику мусора сделать свое дело
            del adc
        print("Программа завершена")
