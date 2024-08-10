import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
import webbrowser

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel('Hostname:'))
        self.hostname_input = QLineEdit(central_widget)
        layout.addWidget(self.hostname_input)

        layout.addWidget(QLabel('API Key:'))
        self.api_key_input = QLineEdit(central_widget)
        layout.addWidget(self.api_key_input)

        layout.addWidget(QLabel('IP Address:'))
        self.ip_input = QLineEdit(central_widget)
        layout.addWidget(self.ip_input)

        self.query_button = QPushButton('Géolocaliser', central_widget)
        self.query_button.clicked.connect(self.on_query)
        layout.addWidget(self.query_button)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Client')
        self.show()

    def query(self, hostname, api_key, ip):
        url = f"http://{hostname}/ip/{ip}?key={api_key}"
        r = requests.get(url)
        print(r.text)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
            return None
        elif r.status_code == requests.codes.OK:
            return r.json()
        else:
            QMessageBox.about(self, "Erreur", f"Erreur: {r.status_code}")
            return None

    def on_query(self):
        hostname = self.hostname_input.text()
        api_key = self.api_key_input.text()
        ip = self.ip_input.text()

        res = self.query(hostname, api_key, ip)
        if res:
            if "Error" in res:
                QMessageBox.about(self, "Erreur", res["Error"])
            else:
                latitude = res['latitude']
                longitude = res['longitude']
                osm_url = f"https://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}"
                webbrowser.open(osm_url)  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
