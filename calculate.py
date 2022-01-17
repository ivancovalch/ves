# КАЛЬКУЛЯЦИЯ ВВЕДЕННЫХ ПАРАМЕТРОВ ЧЕЛОВЕКА
from vars import BMI as BMI
from vars import Normval as Normval
from vars import Brok as Brok

def Calculate(app, screen):
    def NoDataInfo(MiddleWidget, RightWidget, absentData = ""):  # информирование об отсутствии данных в полях результатов (1ая карта)
        screen.ids[MiddleWidget].text = "введите:"
        screen.ids[MiddleWidget].text_color = app.col.unselected
        screen.ids[RightWidget].text = errmes
        screen.ids[RightWidget].text_color = app.col.unselected
        screen.ids[RightWidget].halign = "right"

    def f_input_ok(screen, widget):
        pass

    def f_input_error(screen, err, widget):
        pass

    print ('Start calculation')
    nv = Normval() #создаем новый экземпляр класса с данными о мин-макс значениях переменных
    errmes = "" # сообщение об ошибке
# ПРОВЕРКА ПАРАМЕТРОВ _______________________________________
    # ПОЛ _______________________________________________________________________
    s_gender = ''
    try:
        if screen.ids.ic_male.text_color == app.col.selected:
            s_gender = 'male'
        if screen.ids.ic_female.text_color == app.col.selected:
            s_gender = 'female'
    except: # Ошибка не критична, только информируем
        print("Gender undefined")
    # ГОД РОЖДЕНИЯ -------------------------------------------------------------------------
    s_birthyear = screen.ids.i_birthyear.text # Загрузка данных
    try:
        i_birthyear = int(s_birthyear)
        if i_birthyear < nv.birthyea['min']:
            errmes = "Возраст меньше допустимого"; raise ValueError (errmes)
        if i_birthyear > nv.birthyea['max']:
            errmes = "Возраст больше допустимого"; raise ValueError (errmes)
        f_input_ok(screen, 'i_age')  # если мы здесь - значит все хорошо, устанавливаем нормальный вид формы (возможно он был изменен ранее)
    except ValueError:
        f_input_error(screen, errmes, 'i_age')  # Обработка ошибки
    except:
        f_input_error(screen, "Некорректное значение возраста", 'i_age')  # Обработка ошибки

    # ЕДИНИЦЫ ----------------------------------------------------------------------
    b_metrics       = True # флаг метрической системы
    metric_len      = 1
    metric_weight   = 1
    try:
        if screen.ids.b_metric.text == app.col.selected:
            b_metrics = True
        if screen.ids.b_imperial.text == app.col.selected:
            b_metrics = False
            metric_len      = .393700787 # 1 см / 1 дюйм = 2,54 см
            metric_weight   = .45359237 # 1 кг / 1 фунт
    except:
        print ("Can not read metric system data")

    # РОСТ ___________________________________________________________________________
    s_height = screen.ids.i_hheight.text  # РОСТ
    try:
        height = float(s_height) * metric_len
        if height < nv.height['min']:
            raise ValueError
        if height > nv.height['max']:
            raise ValueError
        f_input_ok(screen, 'ti_interest')  # если мы здесь - значит все хорошо, устанавливаем нормальный вид формы (возможно он был изменен ранее)
    except:
        f_input_error(screen, "Некорректный рост", 'ti_interest')  # Обработка ошибки
        print ('can not read height data')
        return # ОТСУТСТВИЕ ДАННЫХ КРИТИЧНО

    # ВЕС ________________________________________________________________________
    errmes = "Ошибка ввода"
    s_weight = screen.ids.i_weight.text  # ВЕС
    try:
        weight = float(s_weight)
        weightmin = nv.weight['min'] * metric_len
        if weight < weightmin:
            errmes = f"Значение меньше допустимого {round (weightmin,1)}"; raise ValueError
        weightmax = nv.weight['max'] * metric_len
        if weight > weightmax:
            errmes = f"Значение больше допустимого {round (weightmax,1)}"; raise ValueError
        f_input_ok(screen, 'i_weight')  # если мы здесь - значит все хорошо, устанавливаем нормальный вид формы (возможно он был изменен ранее)
    except:
        f_input_error(screen, errmes, 'i_weight')  # Обработка ошибки
        return # ОТСУТСТВИЕ ДАННЫХ КРИТИЧНО

    # ЗАПЯСТЬЕ ________________________________________________________________________
    try:
        errmes = "Ошибка ввода"
        s_wreck = screen.ids.i_wreck.text  # пытаемся считать данные по запястью
        wreck = float(s_wreck)
        wreckmin = nv.wreck['min'] *  metric_len
        if wreck < wreckmin:
            errmes = f"Значение меньше допустимого {round (wreckmin,1)}"; raise ValueError;
        wreckmax = nv.wreck['max'] * metric_len
        if wreck > wreckmax:
            errmes = f"Значение больше допустимого {round (wreckmax,1)}"; raise ValueError;
        f_input_ok(screen, 'i_wreck')  # если мы здесь - значит все хорошо, устанавливаем нормальный вид формы (возможно он был изменен ранее)
    except:
        f_input_error(screen, errmes, 'i_wreck')  # Обработка ошибки
        wreck = 0

# ------------------------------------------------------------------------------------
# ИМТ________________________________
    bmicur = BMI () #создаем новый экземпляр класса BMI со стандартными значениями
    bmicur.set_params(height, weight) # загружаем и устанавливаем параметры
    # вывод данных в графический интерфейс
    screen.ids.b_navarrow.pos_hint = {"left": bmicur.arrow_position, "top": 1} # устанавливаем координаты для стрелки
    screen.ids.l_bmi_resText.text = str(bmicur.bmiround)  # вывод данных ИМТ
    if bmicur.overweight > 0:
        screen.ids.l_bmi_resVerb.text = "избыток"
        screen.ids.l_bmi_resVerb.text_color = app.col.deepred
    elif bmicur.overweight < 0:
        screen.ids.l_bmi_resVerb.text = "дефицит"
        screen.ids.l_bmi_resVerb.text_color = app.col.navy
    else:
        screen.ids.l_bmi_resVerb.text = "норма"
        screen.ids.l_bmi_resVerb.text_color = app.col.green

    print(f"calculate BMI: {str(bmicur.bmiround)} asses qulity {bmicur.bmi_assessment}")

# БРОК + ТИП ТЕЛОСЛОЖЕНИЯ _______________________________________
    errmes = ""
    if s_gender == "":
        errmes += " пол"
    if wreck == 0:
        errmes += " запястье"
    if len(errmes) != 0: # если данные по запястью и полу корректны рассчитываем уточненные данные по телосложению
        NoDataInfo('l_bodytype_resVerb', 'l_bodytype_resText', errmes)
        NoDataInfo('l_brok_resVerb', 'l_brok_resText', errmes)
        print (f"Can't calculate, no data for: {errmes}")
    else:
        brokcur = Brok(height, weight, wreck, s_gender) # создаем класс коэффициента Брокка и получаем нужные значения
        screen.ids.l_bodytype_resText.text = str(brokcur.bodytype)
        screen.ids.l_brok_resVerb.text = str(brokcur.ideal_weight)
        screen.ids.l_brok_resText.text = brokcur.brok_assessment


    s_chest = screen.ids.i_chest.text  # ГРУДЬ
    s_waist = screen.ids.i_waist.text  # ТАЛИЯ
    s_hip = screen.ids.i_hip.text  # БЕДРА
    s_neck = screen.ids.i_neck.text  # БЕДРА
    s_armR = screen.ids.i_armR.text  # РУКА П
    s_armL = screen.ids.i_armL.text  # РУКА Л

