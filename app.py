from flask import Flask


app = Flask(__name__)

# установка секретного ключа
app.secret_key = b' 5#y2L"F4Q8z\n\xec]/'

# импорт всех программ контроллеров
import controllers.index
