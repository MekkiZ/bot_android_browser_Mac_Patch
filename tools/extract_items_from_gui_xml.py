
def main():
    # Using readlines()
    file1 = open('gui/gui.xml', 'r')
    Lines = file1.readlines()

    count = 0
    # Strips the newline character
    list_QPushButton = []
    list_QLabel = []
    list_QPlainTextEdit = []
    list_Line = []
    list_QWidget = []
    list_QLabel = []
    list_QRadioButton = []
    list_QComboBox = []
    list_QCheckBox = []
    list_QTabWidget = []
    list_QLineEdit = []

    list_items_tab_run=[]
    list_items_tab_run_one_task = []
    list_items_tab_settings = []
    list_items_tab_help = []
    mycategory=""
    for line in Lines:


        count += 1

        # Let's take care of categories
        begin_position_category = line.find('<widget class="QWidget" name="tab_')
        if begin_position_category != -1:
            end_position_category = line.find('"', begind_position_class + 35)
            mycategory = line[begin_position_category - 4 + 34:end_position_category]
            # print(f"begin_position_category:{begin_position_category}")
            # print(f"end_position_category:{end_position_category}")
            print(f"mycategory:{mycategory}")




        begind_position_class = line.find('<widget class="')
        if begind_position_class != -1:
            end_position_class = line.find('"', begind_position_class + 16)
            myclass = line[begind_position_class + 15:end_position_class]





            # print(f"""
            #    begind_position_class={begind_position_class}
            #    end_position_class={end_position_class}
            #    myclass=={myclass}
            # """)

            begind_position_name = line.find('name="')
            end_position_name = line.find('"', begind_position_name + 7)
            myname = line[begind_position_name + 6:end_position_name]
            # print(f"""
            #    begind_position_name={begind_position_name}
            #    end_position_name={end_position_name}
            #    myname={myname}
            # """)

            if mycategory == 'tab_run':
                list_items_tab_run.append(myname)
            elif mycategory == 'tab_run_one_task':
                list_items_tab_run_one_task.append(myname)
            elif mycategory == 'tab_settings':
                list_items_tab_settings.append(myname)
            elif mycategory == 'tab_help':
                list_items_tab_help.append(myname)

            if myclass=="QPushButton":
                list_QPushButton.append(myname)

            if myclass=="QLabel":
                list_QLabel.append(myname)

            if myclass=="QPlainTextEdit":
                list_QPlainTextEdit.append(myname)

            if myclass=="Line":
                list_Line.append(myname)

            if myclass=="QWidget":
                list_QWidget.append(myname)

            if myclass=="list_QLabel":
                list_QLabel.append(myname)

            if myclass=="QRadioButton":
                list_QRadioButton.append(myname)

            if myclass=="QComboBox":
                list_QComboBox.append(myname)

            if myclass=="QCheckBox":
                list_QCheckBox.append(myname)

            if myclass=="QTabWidget":
                list_QTabWidget.append(myname)

            if myclass=="QLineEdit":
                list_QLineEdit.append(myname)



    print(f"""
    list_QPushButton =	{list_QPushButton}
    list_QLabel =	{list_QLabel}
    list_QPlainTextEdit =	{list_QPlainTextEdit}
    list_Line =	{list_Line}
    list_QWidget =	{list_QWidget}
    list_QLabel =	{list_QLabel}
    list_QRadioButton =	{list_QRadioButton}
    list_QComboBox =	{list_QComboBox}
    list_QCheckBox =	{list_QCheckBox}
    list_QTabWidget =	{list_QTabWidget}
    list_QLineEdit =	{list_QLineEdit}
    """)

    print(f"""
    list_items_tab_run={list_items_tab_run}
    list_items_tab_run_one_task = {list_items_tab_run_one_task}
    list_items_tab_settings = {list_items_tab_settings}
    list_items_tab_help = {list_items_tab_help}   

    """)

    return list_QPushButton,list_QLabel,list_QPlainTextEdit,list_Line,list_QWidget,list_QLabel,list_QRadioButton,list_QComboBox,list_QCheckBox,list_QTabWidget,list_QLineEdit

#result=main()







