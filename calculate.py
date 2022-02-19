# КАЛЬКУЛЯЦИЯ ВВЕДЕННЫХ ПАРАМЕТРОВ ЧЕЛОВЕКА
from vars import BMI as BMI
from vars import Normval as Normval
from formula import Brok as Brok
from formula import Bodytype as Bodytype
from formula import AbdoObesy as AbdoObesy

def NoDataInfo(MiddleWidget, RightWidget,
               absentData=""):  # информирование об отсутствии данных в полях результатов (1ая карта)
    pass
    # screen.ids[MiddleWidget].text = "введите:"
    # screen.ids[MiddleWidget].text_color = app.col.unselected
    # screen.ids[RightWidget].text = errmes
    # screen.ids[RightWidget].text_color = app.col.unselected
    # screen.ids[RightWidget].halign = "right"

# ЧТЕНИЕ ДАННЫХ ПОЛЕЙ ВВОДА И РАСЧЕТ ПОКАЗАТЕЛЕЙ ФИГУРЫ
def Calculate(app, screen):
    print ('Start calculation')

    # Считываем показатели настроек
    gender = app.gender     # пол -1 Ж, 0 - не определен, 1 - М
    metric = app.metric  # флаг метрической системы
    print (f"Metric {metric} gender {gender}")

    nv = Normval() #создаем новый экземпляр класса с данными о мин-макс значениях переменных
    nv.check_inputs(screen, metric) # расчет и проверка метрических значений

    # ИМТ________________________________
    if not True in [nv.height.error, nv.weight.error] : # если необходимые значения получены без ошибок
        bmicur = BMI () #создаем новый экземпляр класса BMI со стандартными значениями
        bmicur.set_params(nv.height.metric, nv.weight.metric) # загружаем и устанавливаем параметры
        # позиционирование стрелки
        screen.ids.bmi_pos_L.size_hint[0] = bmicur.arrow_position# {"left": .3, "top": 1}
        screen.ids.bmi_pos_R.size_hint[0] = 1-bmicur.arrow_position  # {"left": .3, "top": 1}
        screen.ids.l_bmi_resText.text = str(bmicur.bmiround)  # вывод данных ИМТ
        if False == True:
            if bmicur.overweight > 0:
                #screen.ids.l_bmi_resVerb.text = "избыток"
                #screen.ids.l_bmi_resVerb.text_color = app.col.deepred
                screen.ids.l_bmi_resText.text_color = app.col.deepred
            elif bmicur.overweight < 0:
                #screen.ids.l_bmi_resVerb.text = "дефицит"
                #screen.ids.l_bmi_resVerb.text_color = app.col.navy
                screen.ids.l_bmi_resText.text_color = app.col.navy
            else:
                #screen.ids.l_bmi_resVerb.text = "норма"
                #screen.ids.l_bmi_resVerb.text_color = app.col.green
                screen.ids.l_bmi_resText.text_color = app.col.green

        print(f"calculate BMI: {str(bmicur.bmiround)} asses qulity {bmicur.bmi_assessment} arrow_position {bmicur.arrow_position} diapason {bmicur.diapason}")

# ТИП ФИГУРЫ И ТАЛИЯ _______________________________________
    if not True in [nv.burst.error, nv.waist.error, nv.hip.error]:

        # ТИП ФИГУРЫ
        print (f"Bodytype calculate")
        bt = Bodytype(nv.burst.metric, nv.waist.metric, nv.hip.metric, metric) # расчетный экземпляр класса "тип фигуры"
        body_type_code = "bt"+str(bt.bodytype) # код типа фигуры
        print(f"body_type_code {body_type_code} bodytype {bt.bodytype}")
        screen.ids.l_bodytype_resVerb.text = app.wrd[body_type_code]
        # подсвечивание картинки
        bfg_select = "bfg_"+str(bt.bodytype) # наименование виджета, который нужно подсветить
        for thebodyfig in ['bfg_1','bfg_2','bfg_3','bfg_4','bfg_5','bfg_6','bfg_7']: # перебираем список виджетов-картинок по идентификатору
            if thebodyfig == bfg_select:
                screen.ids[thebodyfig].color = app.col.selected
                print(f"thebodyfig {thebodyfig}")
            else:
                screen.ids[thebodyfig].color = app.col.lightray

        # ТАЛИЯ (ЦЕНТРАЛЬНОЕ ОЖИРЕНИЕ) --------------------------------------------------------------------
    if not True in [nv.burst.error, nv.waist.error, nv.hip.error, nv.height.error]:
        print(f"AbdoObesy calculate")
        ao = AbdoObesy (nv.waist.metric, nv.hip.metric, nv.height.metric, gender)

        # Текстовые значения нормализованных показателей
        integral = ao.integral

        if integral < 40:
            theIntcolor = app.col.deepred
            int_verb = ""
        elif integral < 70:
            theIntcolor = app.col.red
        elif integral < 100:
            theIntcolor = app.col.orange
        else:
            theIntcolor = app.col.green
        screen.ids.l_TitleWaist_resVerb.text = str(integral) + "/100"

        # Нормализованные показатели
        screen.ids.l_wst_indic_norm.text = str(ao.waist)
        screen.ids.l_wh_indic_norm.text = str(ao.WHR)
        screen.ids.l_whh_indic_norm.text = str(ao.abdo_height)

        indicator_list  = [ao.waist_to_normal, ao.WHR_normal, ao.abdo_height_normal]
        widget_list     = ['l_wst_indic', 'l_wh_indic', 'l_whh_indic']

        for norm_val in range (0, len(indicator_list)): # перебираем нормализованные значения
            indicator_to_norm = indicator_list[norm_val]
            left_box_widg = widget_list[norm_val]+'_boxL'
            center_box_widg = widget_list[norm_val] + '_boxC'
            right_box_widg = widget_list[norm_val] + '_boxR'
            # определяем цвет основной шкалы
            if indicator_to_norm < 1:
                thecolor = app.col.green
            elif indicator_to_norm < 1.15:
                thecolor = app.col.orange
            elif indicator_to_norm < 1.3:
                thecolor = app.col.red
            else:
                thecolor = app.col.deepred

            widget_text_res = widget_list[norm_val] + '_norm' # задаем цвет текстового элемента
            screen.ids[widget_text_res].text_color = thecolor

            # Если у индикатора нормальное значение
            if indicator_to_norm < 1:
                left_box_size = indicator_list[norm_val]/2 # относительная ширина левого (рабочего элемента)
                screen.ids[left_box_widg].size_hint_x = left_box_size  # размер левого бокса (шкала)
                center_box_size = .5 - left_box_size  # относительная среднего (до нормы)
                screen.ids[center_box_widg].size_hint_x = center_box_size
                screen.ids[right_box_widg].size_hint_x = .5
                # цветовая окраска
                screen.ids[left_box_widg].md_bg_color = thecolor
                screen.ids[center_box_widg].md_bg_color = app.col.lightray
                screen.ids[right_box_widg].md_bg_color = [0,0,0,0]

            # Если у индикатора значение больше нормы
            elif indicator_to_norm < 2: # превышение но значение вписывается в шкалу
                screen.ids[left_box_widg].size_hint_x = .5  # размер левого бокса (шкала)
                center_add = (indicator_to_norm - 1)/2 # диапазон значени 0 +0.5
                screen.ids[center_box_widg].size_hint_x = center_add
                screen.ids[right_box_widg].size_hint_x = .5 - center_add
                # цветовая окраска
                screen.ids[left_box_widg].md_bg_color = app.col.green
                screen.ids[center_box_widg].md_bg_color = thecolor
                screen.ids[right_box_widg].md_bg_color = [0,0,0,0]
                print (f"center add {center_add}")

            else:  # Индикатор больше >2
                screen.ids[left_box_widg].size_hint_x = .5  # размер левого бокса (шкала)
                screen.ids[center_box_widg].size_hint_x = .25
                screen.ids[right_box_widg].size_hint_x = .25
                # цветовая окраска
                screen.ids[left_box_widg].md_bg_color = thecolor
                screen.ids[center_box_widg].md_bg_color = thecolor
                screen.ids[center_box_widg].md_bg_color = thecolor









