# КАЛЬКУЛЯЦИЯ ВВЕДЕННЫХ ПАРАМЕТРОВ ЧЕЛОВЕКА

def Calculate(app, screen):
    print ('calculation')
# НАСТРОЙКИ _______________________________________
    # ПОЛ __________
    s_gender = 'undefined'
    try:
        if screen.ids.ic_male.text_color == app.col.selected:
            s_gender = 'male'
        if screen.ids.ic_female.text_color == app.col.selected:
            s_gender = 'female'
    except: # Ошибка не критична, только информируем
        print("Can not read gender data from UI")

    # ВОЗРАСТ __________
    s_age = screen.ids.i_age.text
    try:
        i_age = int(s_age)
        if i_age < 1 or i_age > 125:
            raise ValueError
        f_input_ok(screen, 'i_age')  # если мы здесь - значит все хорошо, устанавливаем нормальный вид формы (возможно он был изменен ранее)
    except:
        f_input_error(screen, "Некорректное значение возраста", 'i_age')  # Обработка ошибки

    # ЕДИНИЦЫ __________
    b_metrics = True # флаг метрической системы
    try:
        if screen.ids.b_metric.text == app.col.selected:
            b_metrics = True
        if screen.ids.b_imperial.text == app.col.selected:
            b_metrics = False
    except:
        print ("Can not read metric system data")
#------------------------------------------------------------------------------------
    # РОСТ __________
    s_height = screen.ids.i_hheight.text  # РОСТ
    try:
        i_height = float(s_height)
        if i_height < 10 or i_height > 1000:
            raise ValueError
        f_input_ok(screen, 'ti_interest')  # если мы здесь - значит все хорошо, устанавливаем нормальный вид формы (возможно он был изменен ранее)
    except:
        f_input_error(screen, "Рост введен неверно", 'ti_interest')  # Обработка ошибки
        print ('can not read height data')
        return # ОТСУТСТВИЕ ДАННЫХ КРИТИЧНО

    # ВЕС __________
    s_weight = screen.ids.i_weight.text  # ВЕС
    try:  # ПРОЦЕНТНАЯ СТАВКА
        i_weight = float(s_weight)
        if i_weight < 1 or i_weight > 1000:
            raise ValueError
        if i_weight == 0:
            raise ValueError
        f_input_ok(screen, 'ti_interest')  # если мы здесь - значит все хорошо, устанавливаем нормальный вид формы (возможно он был изменен ранее)
    except:
        f_input_error(screen, "Некорректное значение процентной ставки", 'ti_interest')  # Обработка ошибки
        print('can not read weight data')
        return

# КАЛЬКУЛЯЦИЯ ИМТ________________________________
    i_bmi = i_weight / (i_height/100)**2
    i_bmi = round(i_bmi, 1)
    screen.ids.l_iweight_resText.text = str(i_bmi)
    # качественная оценка
    i_bmi_qulity = 100
    if i_bmi > 24.5:
        if i_bmi > 45:
            i_bmi_qulity = 0
        else:
            i_bmi_qulity = 100 - (i_bmi - 24.5) / (45-24.5) * 100
    if i_bmi < 18:
        if i_bmi < 14:
            i_bmi_qulity = 0
        else:
            i_bmi_qulity = 100 - (18.5 - i_bmi ) / (18.5 - 14) * 100
    i_bmi_qulity = round(i_bmi_qulity,0)

    text_qulity = "норма"



    print(f"calculate BMI: {str(i_bmi)} asses qulity {i_bmi_qulity}")


    s_wreck = screen.ids.i_wreck.text  # ЗАПЯСТЬЕ
    s_chest = screen.ids.i_chest.text  # ГРУДЬ
    s_waist = screen.ids.i_waist.text  # ТАЛИЯ
    s_hip = screen.ids.i_hip.text  # БЕДРА
    s_neck = screen.ids.i_neck.text  # БЕДРА
    s_armR = screen.ids.i_armR.text  # РУКА П
    s_armL = screen.ids.i_armL.text  # РУКА Л

    # Проверка переменных
    s_new = s_height + s_weight

    screen.ids.l_iweight_resVerb.text =  "111"
    #self.screen.ids.l_iweight_resVerb.text = "121"

def f_input_ok(screen, widget):
    pass

def f_input_error(screen, err, widget):
    pass