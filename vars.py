from formula import getKoef as getKoef

class Colorpallet():
    def __init__(self, light = True):
        self.primary    = [1, 1, 0, 1]
        self.secondary  = [1, 1, 0, 1]
        self.bg         = [1, 1, 1, 1]

        self.black      = [0, 0, 0, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.white      = [1, 1, 1, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.darkgray   = [.3, .3, .3, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.gray       = [.6, .6, .6, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.lightray   = [.8, .8, .8, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА

        self.navy       = [.25, .2, 1, 1]
        self.blue       = [.4, .5, .95, 1]
        self.lightblue  = [.45, .75, .9, 1]
        self.green      = [.3, .7, .2, 1]
        self.yellow     = [1, .85, .25, 1]
        self.orange     = [1, .65, .2, 1]
        self.red        = [1, .45, .2, 1]
        self.deepred    = [1, .25, .2, 1]

        self.mrestext   = [.34, .12, .12, 1]  # основной текстовый цвет
        self.unselected = [.65, .55, .35, 1] #[.7, .7, .7, 1]  # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.selected   = [.45, .25, .05, 1] #[.55, .25, .07, 1]  # [.87, .50, .1, 1] # пользовательский цвет ВЫБРАННОГО ЭЛЕМЕНТА
        self.hint_text  = [.8, .8, .8, 1]
        self.bg_medium  = [.95, .95, .95, 1]  # пользовательский цвет ФОНА небольших элементов
        self.bg_pale    = [.98, .96, .91, 1]  # пользовательский цвет ФОНА небольших элементов
        self.bg_light   = [.98, .98, .98, 1]  # пользовательский цвет ФОНА небольших элементов
        self.bg         = [.99, .99, .99, 1]

# Связка классов для трансформации словарей в свойства классов.
class ADictMeta(type): #
    def __setitem__(self, key, value):
        setattr(self, key, value)
    def __getitem__(self, key):
        return getattr(self, key)
class Words(metaclass=ADictMeta):
    pass

# ПОЛЕ ВВОДА И ЕГО ПАРАМЕТРИЧЕСКИЕ ЗНАЧЕНИЯ
# АРГУМЕНТЫ
# min, - минимальное значение
# std, - стандартное
# max, - максимальное
# widgetname - название поля для ввода данных,
# type - тип данных, возможные значения "int", 'str', 'float', bool real=0
class InputField ():
    def __init__(self, min, std, max, type, widgetname):
        self.min = min
        self.std = std
        self.max = max
        self.type = type  # 0 - даты, 1 - длина, обхват, 2 - вес
        self.widgetname = widgetname
        # значения присваиваемые по умолчанию
        self.metric = 0
        self.error = False
        self.errortype = 0

# СЛОВАРЬ-КЛАСС ПАРАМЕТРОВ
class Normval(): # допустимый диапазон значений (в метрической системе)
    def __init__(self):
        self.birthyea        = InputField (1000, 2000,  2030,  0,    'i_birthyear') # дата рождения
        self.height          = InputField (130,  170,   250,   1,  'i_hheight')              # рост
        self.weight          = InputField (20,   70,    450,   2,  'i_weight') # Обхват грудной клетки
        self.age             = InputField (10,   30,    130,   1,  'i_age') # Обхват грудной клетки
        self.burst           = InputField (40,   90,    300,   1,  'i_chest') # Обхват грудной клетки
        self.chest           = self.burst   # Обхват грудной клетки СИНОНИМ
        self.waist           = InputField (40,   90,    300,   1,  'i_waist') # Обхват талии
        self.hip             = InputField (40,   90,    300,   1,  'i_hip') # Обхват бедер

    def input_ok(screen, widget):
        pass

    def input_error(screen, err, widget):
        pass

    # Чтение и проверка данных форм ввода
    def check_inputs (self, screen, metrics = True):

        koef = getKoef(metrics) # получаем коэффициенты (=1 при метрической системы, или иные, при имперской)

        for key,value in self.__dict__.items():
            errmes = 0 # сообщение об ошибке по умолчанию
            try:
                errmes = 1
                str_from_input = screen.ids[value.widgetname].text
                errmes = 2
                num_val = float(str_from_input)
                errmes = 3
                num_val_m = num_val * koef[value.type] # переводим данные в метрическую систему
                if num_val_m < value.min:
                    errmes = 4 #f"Значение меньше допустимого {round(wreckmin, 1)}";
                    raise ValueError;
                if num_val > value.max:
                    errmes = 5 # f"Значение больше допустимого {round(wreckmax, 1)}";
                    raise ValueError;

                value.metric = num_val_m
                value.error = False
                # input_error добавить действия по нормализации формы НЕТ ОШИБКИ

            except:
                value.error = True
                value.errortype = errmes
                value.metric = 0 # в случае ошибки присваиваем для расчетов нулевое значение
                # input_ok добавить действия по информированию об ошибке и модификации ФОРМЫ ВВОДА

            print(f"Read input: {key} value: {value.metric}  error: {value.error}") # логгирование

    # Распечатка данных формы
    def printmetric(self):
        for key, value in self.__dict__.items():
            print(f"{key} is: {value.metric}")


class Weightcathegory:
    def __init__(self, code, min_index, max_index):
        self.code = code # имя
        self.min_index = min_index  # минимальная граница диапазона
        self.max_index = max_index  # максимальная граница диапазона
        self.diapason = max_index - min_index

class Weightscale:
    def __init__(self, weight_real, weight_ideal, L2 = .6, L1 = .7, D = .8, N = 0.9, A = 1.1, F1 = 1.15, F2 = 1.3, F3 = 1.5, F4 = 2):
        for cathegory in [L1, D, N , A, F1, F2, F3, F4]:
            self.cathegory = Weightcathegory()

class BMI():
    def __init__(self, L2 = 14, L1 = 16, D = 17, N = 18.5, A = 25, F1 = 30, F2 = 35, F3 = 40, F4 = 45): # scale = True -- безразмерные единицы (индекс), False - единица скалы - килограмм
        self.L3 = L2
        self.L2 = L1
        self.L1 = D
        self.N = N # нижняя граница нормы
        self.A = A # верхняя граница нормы
        self.F1 = F1
        self.F2 = F2
        self.F3 = F3
        self.F4 = F4
        self.set_diapason() # метод рассчитывающий диапазоны категорий
    def set_diapason(self):
        self.diapason = self.F4 - self.L3 # абсолютное значение диапазона в единицах BMI Для расчета графической шкалы

    def set_params(self, height, weight):
        print (f"set params with height: {height}, weight: {weight}")
        height_corrected = (height/100)**2              # квадрат роста в метрах
        bmi = weight / height_corrected                 # индекс ИМТ для полученных аргументов
        weight_normal_low = height_corrected * self.N   # нижняя граница нормы веса
        weight_normal_high = height_corrected * self.A   # верхняя граница нормы веса
        overweight = 0                                  # избыток (+) или нехватка (-) веса
        if weight > weight_normal_high:
            overweight = weight - weight_normal_high
        if weight < weight_normal_low:
            overweight = weight - weight_normal_low     # значение со знаком минус

        # Количественные параметры оценки ИМТ
        bmi_quality = 100
        if bmi > self.A:
            if bmi > self.F4:
                bmi_quality = 0
                arrow_position = 1
            else:
                bmi_quality = 100 - (bmi - self.A) / (self.F4 - self.A) * 100
                arrow_position = (bmi - 14) / self.diapason
        elif bmi < 18:
            if bmi < 14:
                bmi_quality = 0
                arrow_position = 0
            else:
                bmi_quality = 100 - (self.N - bmi ) / (self.N - self.L2) * 100
                arrow_position = (bmi - self.L3) / self.diapason
        else:
            arrow_position = (bmi - self.L3) / self.diapason
            #coordinates = {"left":  arrow_position, "top": 1}

        # Качественная оценка ИМТ________________________________
        bmi_assessment = ""
        if bmi < self.L2:
            bmi_assessment = "L2"
        elif bmi < self.L1:
            bmi_assessment = "L1"
        elif bmi < self.N:
            bmi_assessment = "D"
        elif bmi < self.A:
            bmi_assessment = "N"
        elif bmi < self.F1:
            bmi_assessment = "A"
        elif bmi < self.F2:
            bmi_assessment = "F1"
        elif bmi < self.F3:
            bmi_assessment = "F2"
        else: # все значения равные или превышающие self.F3
            bmi_assessment = "F3"
        # УСТАНАВЛИВАЕМ НОВЫЕ СВОЙСТВА
        self.bmi = bmi
        self.bmiround = round(bmi,1)  # индекс ИМТ для полученных аргументов
        self.weight_normal_low = weight_normal_low   # нижняя граница нормы веса
        self.weight_normal_high = weight_normal_high   # верхняя граница нормы веса
        self.overweight = overweight
        self.bmi_quality = bmi_quality
        self.bmi_assessment = bmi_assessment
        self.arrow_position = arrow_position
        print (f"weight_normal_low: {weight_normal_low}  weight_normal_high: {weight_normal_high} overweight {overweight}")



