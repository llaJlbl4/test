import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox

API_URL = "http://127.0.0.1:8000/predict"

# Доступные значения (из анализа файла)
MODELS = ["Средняя продолжительность жизни", "Возрастной коэффицент смертности", "Стандартизированный возрастной коэффициент смертности"]
SEXES = ["Оба пола", "Мужчины", "Женщины"]
AGES = [0, 15, 50, 65]
OBJECTS = [
    "Российская Федерация", "Белгородская область", "Брянская область", "Владимирская область",
    "Воронежская область", "Ивановская область", "Калужская область", "Костромская область",
    "Курская область", "Липецкая область", "Московская область", "Орловская область",
    "Рязанская область", "Смоленская область", "Тамбовская область", "Тверская область",
    "Тульская область", "Ярославская область", "Москва", "Республика Карелия", "Республика Коми",
    "Архангельская область", "Вологодская область", "Калининградская область", "Ленинградская область",
    "Мурманская область", "Новгородская область", "Псковская область", "Санкт-Петербург",
    "Республика Адыгея", "Республика Калмыкия", "Краснодарский край", "Астраханская область",
    "Волгоградская область", "Ростовская область", "Республика Дагестан",
    "Кабардино-Балкарская Республика", "Республика Северная Осетия — Алания", "Ставропольский край",
    "Республика Башкортостан", "Республика Марий Эл", "Республика Мордовия", "Республика Татарстан",
    "Удмуртская Республика", "Чувашская Республика", "Пермский край", "Кировская область",
    "Нижегородская область", "Оренбургская область", "Пензенская область", "Самарская область",
    "Саратовская область", "Ульяновская область", "Курганская область", "Свердловская область",
    "Тюменская область", "Челябинская область", "Республика Бурятия", "Республика Тыва",
    "Республика Хакасия", "Алтайский край", "Забайкальский край", "Красноярский край",
    "Иркутская область", "Кемеровская область", "Новосибирская область", "Омская область",
    "Томская область", "Республика Саха (Якутия)", "Камчатский край", "Приморский край",
    "Хабаровский край", "Амурская область", "Сахалинская область", "Карачаево-Черкесская Республика",
    "Ханты-Мансийский автономный округ — Югра", "Ямало-Ненецкий автономный округ",
    "Республика Ингушетия", "Чеченская Республика", "Республика Крым", "Севастополь",
    "Архангельская область", "Тюменская область"
]  # Заполните списком из CSV
YEARS = [
    1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 
    2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 
    2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 
    2022, 2023, 2024
]

class MLApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ML Prediction App")
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        # модель
        self.label = QLabel("Выберите модель:")
        layout.addWidget(self.label)
        self.input_model = QComboBox()
        self.input_model.addItems(MODELS)
        layout.addWidget(self.input_model)
        self.input_model.activated.connect(self.current_text)

        # Пол
        self.label1 = QLabel("Выберите пол:")
        layout.addWidget(self.label1)
        self.input_sex = QComboBox()
        self.input_sex.addItems(SEXES)
        layout.addWidget(self.input_sex)

        # Возраст
        self.label2 = QLabel("Выберите возраст:")
        layout.addWidget(self.label2)
        self.input_age = QComboBox()
        self.input_age.addItems([str(age) for age in AGES])
        layout.addWidget(self.input_age)
        
        # Объект (город, регион)
        self.label3 = QLabel("Выберите объект:")
        layout.addWidget(self.label3)
        self.input_object = QComboBox()
        self.input_object.addItems(OBJECTS)
        layout.addWidget(self.input_object)

        # Год
        self.label4 = QLabel("Выберите год:")
        layout.addWidget(self.label4)
        self.input_year = QComboBox()
        self.input_year.addItems([str(year) for year in YEARS])
        layout.addWidget(self.input_year)

        # Кнопка предсказания
        self.predict_button = QPushButton("Получить предсказание")
        self.predict_button.clicked.connect(self.get_prediction)
        layout.addWidget(self.predict_button)

        # Результат
        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def get_prediction(self):
        """ Отправляет запрос на API и получает предсказание """
        data = {
            "model": self.input_model.currentText(),
            "sex": self.input_sex.currentText(),
            "age": self.input_age.currentText(),
            "object_name": self.input_object.currentText(),
            "year": int(self.input_year.currentText()),
        }

        try:
            response = requests.post(API_URL, json=data)
            response.raise_for_status()
            prediction = response.json()["prediction"]
            self.result_label.setText(f"Предсказание: {prediction}")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка запроса: {e}")
    
    def current_text(self, _): # We receive the index, but don't use it.
        ctext = self.input_model.currentText()
        if ctext == "Средняя продолжительность жизни":
            AGES = [0, 15, 50, 65]
            self.input_age.clear()
            self.input_age.addItems([str(age) for age in AGES])
        elif ctext == "Возрастной коэффицент смертности":
            AGES = ["0 лет", "1-4 года", "5-9 лет", "10-14 лет", "15-19 лет", "20-24 лет", "25-29 лет", "30-34 лет", "35-39 лет", "40-44 лет", "45-49 лет", "50-54 лет", "55-59 лет", "60-64 лет", "65-69 лет", "70-74 лет", "75-79 лет", "80-84 лет", "85 лет и более"]
            self.input_age.clear()
            self.input_age.addItems([str(age) for age in AGES])
        elif ctext == "Стандартизированный возрастной коэффициент смертности":
            AGES = ["0-14 лет", "15-49 лет", "50-64 лет", "65 лет и более", "Все возраста"]
            self.input_age.clear()
            self.input_age.addItems([str(age) for age in AGES])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MLApp()
    window.show()
    sys.exit(app.exec_())
