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
        self.bg_medium = [.95, .95, .95, 1]  # пользовательский цвет ФОНА небольших элементов
        self.bg_light   = [.98, .98, .98, 1]  # пользовательский цвет ФОНА небольших элементов
        self.bg         = [.99, .99, .99, 1]

class Normval(): # допустимый диапазон значений (в метрической системе)
    def __init__(self):
        self.birthyea        = {'min':1000, 'std': 2000, 'max':2022}
        self.height          = {'min':130, 'std':170, 'max':250} # рост
        self.weight          = {'min':20, 'std':70, 'max':450}
        self.age             = {'min':10, 'std':30, 'max':130}
        self.wreck          = {'min': 10, 'std': 19, 'max': 40}

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
        arrow_position = (bmi - self.L2) / (self.diapason) # позиция стрелки на индикаторе
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
                arrow_position = (bmi - self.L2) / self.diapason
        else:
            arrow_position = (bmi - self.L2) / self.diapason
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

class Brok(): # расчет параметров центрального ожирения
    def __init__(self, height, weight, wreck, s_gender = 'male'):
        s_bodytype = 0  # нормостеник
        f_bodytype_k = 1
        # Оценка телосложения и коэффициента Брока в зависимости от запястья
        if s_gender == "male":
            if wreck < 18:
                s_bodytype = -1  # астеник
                f_bodytype_k = .9
            if wreck > 20:
                s_bodytype = 1  #
                f_bodytype_k = 1.1
        if s_gender == "female":
            if wreck < 15:
                s_bodytype = -1
                f_bodytype_k = .9
            if wreck > 17:
                s_bodytype = 1
                f_bodytype_k = 1.1

        f_height_k = 100
        if height < 160:
            f_height_k = f_height_k + (height - 160) / 2
        if height > 170:
            f_height_k = f_height_k + (height - 170) / 2
        f_brok_ideal_weight = (height  -  f_height_k) *  f_bodytype_k
        overweight          = weight - f_brok_ideal_weight # избыточный (- дефицитный) вес, в кг
        weight_to_ideal     = weight / f_brok_ideal_weight # соотношение фактического и идеального веса

        # качественная оценка веса
        brok_assessment = ""
        if   weight_to_ideal < .7:
            brok_assessment = "L2"
        elif weight_to_ideal < .8:
            brok_assessment = "L1"
        elif weight_to_ideal < .9:
            brok_assessment = "D"
        elif weight_to_ideal < 1.05:
            brok_assessment = "N"
        elif weight_to_ideal < 1.15:
            brok_assessment = "A"
        elif weight_to_ideal < 1.3:
            brok_assessment = "F1"
        elif weight_to_ideal < 1.5:
            brok_assessment = "F2"
        elif weight_to_ideal < 2.0:
            brok_assessment = "F3"
        else: # все значения равные или превышающие self.F3
            brok_assessment = "F4"

        self.bodytype       = s_bodytype
        self.brokbodytypeK  = f_bodytype_k
        self.brokbodytypeK  = f_height_k
        self.ideal_weight   = f_brok_ideal_weight
        self.overweight     = overweight
        self.brok_assessment = brok_assessment

        def __iter__(self):
            for attr, value in self.__dict__.iteritems():
                print( f"{attr}: {value}")

class CentObesy(): # расчет параметров центрального ожирения
    pass

