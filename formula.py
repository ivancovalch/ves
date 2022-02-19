# ИНИЦИАЦИЯ КОНСТАНТ ПРОЕКТА
def getKoef (metrics):
    koef = [1, 1, 1]
    if metrics == False:
        koef[0] = 1  # дата, совпадает в метрической и имперской системах
        koef[1] = .393700787  # 1 см / 1 дюйм = 2,54 см  # metric_len
        koef[2] = .45359237  # 1 кг / 1 фун
    return koef


# ТИП ФИГУРЫ, источники для формул: https://calculator-online.net/body-shape-calculator/
# обхываты: bust-грудь,
# waist-талия,
# hips-бедра,
# highhip-верхняя часть бедер (опция)  - все значения float или int > 0 выраженые в метрических единицах (см)

class Bodytype ():
    def __init__(self, bust, waist, hips, metric, highhip = 0):
        self.bodytype = 0
        self.bodysubtype = ""

        if highhip == 0: # Данные об окружности верхней части бедер не полученны
            highhip = .9 * hips # рассчитываем данные на основе информации об охвате бедер

        B_min_H =  bust - hips
        H_min_B = hips - bust
        B_min_W = bust - waist
        W_min_B = waist - bust
        H_min_W = hips - waist
        HH_min_W = highhip - waist
        hip_per_waist = hips / waist

        print(f"B_min_H {B_min_H}")
        print(f"H_min_B {H_min_B}")
        print(f"B_min_W {B_min_W}")
        print(f"W_min_B {W_min_B}")
        print(f"H_min_W {H_min_W}")
        print(f"HH_min_W {HH_min_W}")
        print(f"hip_per_waist {hip_per_waist}")

        # Hourglass
        if B_min_H <= 2.5 and H_min_B < 9 and (B_min_W >= 22.6 or H_min_W >= 25.1):
            self.bodytype = 1 # hourglass
        # Top hourglass
        elif B_min_H > 2.5 and  B_min_H < 25.1 and B_min_W >= 22.6:
            self.bodytype = 2 # top hourglass
        # bottom hourglass
        elif H_min_B > 9 and  H_min_B < 25.1 and B_min_W >= 22.6  and HH_min_W < 1.193:
            self.bodytype = 3 # bottom hourglass
        # Triangle
        elif H_min_B > 5.2 and  H_min_W >= 17.6 and hip_per_waist >= 1.193:
            self.bodytype = 4 # Triangle
        # Invert Triangle
        elif B_min_H >= 9 and  B_min_W < 22.6:    # B_min_H >= 9 and  B_min_W < 22.6
            self.bodytype = 5 # Invert Triangle
        # Rectangle
        elif H_min_B < 9 and B_min_H < 9 and B_min_W < 22.6 and H_min_W < 25.1 and (B_min_W > 0 or H_min_W >= 0): # добавил последнее условие
            self.bodytype = 6 # Rectangle
        # Round
        elif B_min_W < 0 and H_min_W < 0 : # H_min_B >= 9 and H_min_W <  22.6
            self.bodytype = 7 # Round


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

# ЦЕНТРАЛЬНОЕ ОЖИРЕНИЕ. ТАЛИЯ
    # АРГУМЕНТЫ
    # waist - размер талии , см. FLOAT
    # hip - бедра , см. FLOAT
    # height - рост, см. FLOAT
    # gender: половая принадлежность 0 - Не определен, 1-Ж, 2-М  INTEGER (0+3)

class AbdoObesy(): # расчет параметров центрального ожирения

    def __init__(self, waist, hip, height, gender):

        abdo_height  = waist / height
        WHR          = waist / hip

        # Нормативные величины показателей для разных полов: 1) талия, 2) abdo_height, 3) abdo_burst 4) abdo_hip
        waist_norm          = [87, 80, 94]
        abdo_height_norm    = [.5, .5, .5]
        WHR_norm            = [.85, .8, .9]

        self.waist              = round (waist, 0)
        self.waist_to_normal    = WHR/WHR_norm[gender]

        self.abdo_height        = round (abdo_height,2)
        self.abdo_height_normal = abdo_height/abdo_height_norm[gender]

        self.WHR                = round (WHR, 2)
        self.WHR_normal         = WHR/WHR_norm[gender]

        # Интегральная оценка величины талии  / абдоминального ожирения
        integral = 1 # стартовое интегральное значение
        for indicator in  [self.waist_to_normal,  self.abdo_height_normal, self.WHR_normal]:
            if indicator < 1:
                integral *= 1
            else:
                integral *= 1 / indicator**2 # 1 / куб соотношения с нормой

        self.integral = round (integral*100)

    def printmetric(self):
        for key, value in self.__dict__.items():
            print(f"{key} is: {value.metric}")