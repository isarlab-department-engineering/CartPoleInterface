
from ArduinoGui import PyArduinoGUIView
from PyArduinoGUIController import PyArduinoGUIController


if __name__ == "__main__":
    controller = PyArduinoGUIController()
    view = PyArduinoGUIView(controller, False)
    controller.view = view
    controller.aggiorna_porte()
    view.run()
