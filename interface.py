from presencas import *
import pyautogui as p
from connection import connection
from datetime import date
import socket
import requests as r
import json
from time import sleep

sem = ("Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", 'Domingo')
data_atual = date.today().strftime('%d/%m/%Y')
weekday = sem[date.today().weekday()]
alert = "font-size:16px;position: relative; padding: 0.75rem 1.25rem; margin-bottom: 1rem; border: 1px solid transparent;border-radius: 0.25rem;"
alertPrimary = alert+"color: #004085; background-color: #cce5ff; border-color: #b8daff;"
alertSuccess = alert+"color: #155724;background-color: #d4edda;border-color: #c3e6cb;"
alertDanger = alert+"color: #721c24; background-color: #f8d7da; border-color: #f5c6cb;"

def cleanCheckboxes():
    ui.oito.setCheckState(0) if ui.oito.isChecked() else None,
    ui.nove.setCheckState(0) if ui.nove.isChecked() else None,
    ui.dez.setCheckState(0) if ui.dez.isChecked() else None,
    ui.onze.setCheckState(0) if ui.onze.isChecked() else None,
    ui.doze.setCheckState(0) if ui.doze.isChecked() else None,
    ui.treze.setCheckState(0) if ui.treze.isChecked() else None,
    ui.catorze.setCheckState(0) if ui.catorze.isChecked() else None,
    ui.quinze.setCheckState(0) if ui.quinze.isChecked() else None,
    ui.dezesseis.setCheckState(0) if ui.dezesseis.isChecked() else None,
    ui.dezessete.setCheckState(0) if ui.dezessete.isChecked() else None,
    ui.dezoito.setCheckState(0) if ui.dezoito.isChecked() else None,
    ui.dezenove.setCheckState(0) if ui.dezenove.isChecked() else None,

def cleanCodigoContratoNomeCompleto():
    ui.CodigoContrato.setText('')
    formEsqueci.NomeCompleto.setText('')


def cleanFormPresenca():
    ui.CodigoContrato.setText('')
    ui.alert.setStyleSheet('')
    ui.fechar_alert.setStyleSheet('border:none')
    ui.fechar_alert.setEnabled(False)
    ui.alert.clear()
    ui.fechar_alert.setText('')
    ui.CodigoContrato.setFocus()

def cleanFormEsqueci():
    formEsqueci.NomeCompleto.setText('')
    formEsqueci.lbl_usuario.setText('')
    formEsqueci.lbl_senha.setText('')
    formEsqueci.alert.setText('')
    formEsqueci.alert.setStyleSheet('')
    formEsqueci.frame_dados.setStyleSheet('')

def cleanAll():
   cleanCheckboxes()
   cleanFormEsqueci()
   cleanFormPresenca()

def timerEvent(max_wait = 59):
    global time
    time = time.addSecs(1)
    decorrido = int(time.toString("ss"))
    if decorrido >= max_wait:
        cleanAll()
        timer.stop()
        return True
    print(decorrido)
        
def insert(dados):
    db = connection(host='servidorouro', user="prepara2", password="prepara", database="bd_presencas")
    insert2 = db.insert(dados=dados)
    return insert2
    
def verificarPresenca(CodigoContrato, DataPresenca, HoraPresenca):
    db = connection(host='servidorouro', user="prepara2", password="prepara", database="bd_presencas")
    user = db.selectUserPresenca(CodigoContrato, DataPresenca, HoraPresenca)
    return user

def verificarUsuario(CodigoContrato):
    db = connection(host='servidorouro', user="prepara2", password="prepara", database="ouromoderno")
    user = db.selectUserOuro(CodigoContrato)
    if user['NomeAluno'] != None or user['NomeAluno']: 
        return user
    else:
        user = r.get("http://192.168.1.11/presencas/controllers/ApiController.php?CodigoContrato="+CodigoContrato)
        return json.loads(user.content)

def marcarPresenca():
    timer.timeout.connect(timerEvent)
    timer.start(1000)
    lista = [
            ui.oito.text() if ui.oito.isChecked() else None,
            ui.nove.text() if ui.nove.isChecked() else None,
            ui.dez.text() if ui.dez.isChecked() else None,
            ui.onze.text() if ui.onze.isChecked() else None,
            ui.doze.text() if ui.doze.isChecked() else None,
            ui.treze.text() if ui.treze.isChecked() else None,
            ui.catorze.text() if ui.catorze.isChecked() else None,
            ui.quinze.text() if ui.quinze.isChecked() else None,
            ui.dezesseis.text() if ui.dezesseis.isChecked() else None,
            ui.dezessete.text() if ui.dezessete.isChecked() else None,
            ui.dezoito.text() if ui.dezoito.isChecked() else None,
            ui.dezenove.text() if ui.dezenove.isChecked() else None,
        ]
    HoraPresenca = []
    for i in lista:
        if i != None:
            HoraPresenca.append(i)

    ui.fechar_alert.setStyleSheet("color: #fff; background-color: #dc3545;border-color: #dc3545;display: inline-block;font-weight: 400;text-align: center;white-space: nowrap;vertical-align: middle;border: 1px solid transparent;padding: 6px 12px;font-size: 16px;line-height: 1.5;border-radius: 4px;")
    ui.fechar_alert.raise_()
    ui.fechar_alert.setEnabled(True)
    ui.fechar_alert.setText("X")
    alert = ui.alert
    alert.setText("Aguarde...")
    alert.setStyleSheet(alertPrimary)
    alert.raise_
    i = 0
    
    CodigoContrato = ui.CodigoContrato.text()

    if CodigoContrato and len(HoraPresenca) >= 1:
        user = verificarUsuario(CodigoContrato)
        try:
            alert.setText(user['message'])
            alert.setStyleSheet(alertDanger)
        except:
            data = {
                "CodigoContrato" : CodigoContrato,
                "HoraPresenca": HoraPresenca,
                "NomeAluno" : user['NomeAluno'],
                "DataPresenca" : ui.DataPresenca.text(),
                "DiaSemana" : ui.DiaSemana.text(),
                "Computador" : ui.Computador.text(),
                "IpComputador" : ui.IpComputador.text(),
            }
            
            for HoraP in data["HoraPresenca"]:
                presencaConfirmada = verificarPresenca(CodigoContrato=data["CodigoContrato"], DataPresenca=data["DataPresenca"], HoraPresenca=HoraP)
                if(presencaConfirmada):
                    alert.setText('A sua presença já foi confirmada. Feche esta janela e boa aula!')
                    alert.setStyleSheet(alertPrimary)
                    cleanCheckboxes()
                    cleanCodigoContratoNomeCompleto()
                else:
                    data2 = {
                    "CodigoContrato" : CodigoContrato,
                    "HoraPresenca": HoraP,
                    "NomeAluno" : user['NomeAluno'],
                    "DataPresenca" : ui.DataPresenca.text(),
                    "DiaSemana" : ui.DiaSemana.text(),
                    "Computador" : ui.Computador.text(),
                    "IpComputador" : ui.IpComputador.text(),
                    }
                    insert2 = insert(data2)
                    if insert2:
                        alert.setText("Sucesso! A sua presença foi confirmada. Feche esta janela e boa aula!")
                        alert.setStyleSheet(alertSuccess)
                        cleanCheckboxes()
                        cleanCodigoContratoNomeCompleto()
                    else:
                        alert.setText("Falha! Houve erros na hora de confirmar sua presença.\nVerifique com seu educador(a).")
                        alert.setStyleSheet(alertDanger)
                        cleanCheckboxes()
                        cleanCodigoContratoNomeCompleto()


    else:
        alert.setText("Não foi possível validar os dados.\nPreencha o campo de usuário e marque os horários corretamente.")
        alert.setStyleSheet(alertDanger)
    

def fecharAlert():
    ui.alert.setStyleSheet('')
    ui.fechar_alert.setStyleSheet('border:none')
    ui.fechar_alert.setEnabled(False)
    ui.alert.clear()
    ui.fechar_alert.setText('')

    
def getUserData():
    NomeAluno = formEsqueci.NomeCompleto.text()
    max_wait = 300
    timer.timeout.connect(timerEvent, max_wait)
    timer.start(1000)
    if not NomeAluno:
        formEsqueci.NomeCompleto.setText('')
        formEsqueci.alert.setStyleSheet(alertDanger)
        formEsqueci.alert.setText("Não foi possível validar os dados. Tente novamente!")
        formEsqueci.lbl_usuario.setText('')
        formEsqueci.lbl_senha.setText('')
        formEsqueci.frame_dados.setStyleSheet('')        
    else:
        db = connection(host='servidorouro', user="prepara2", password="prepara", database="ouromoderno")
        user = db.selectUserOuroByTheName(NomeAluno)
        if user != False:
            try:
                formEsqueci.frame_dados.setStyleSheet(alertSuccess)
                formEsqueci.lbl_usuario.setText(user['CodigoContrato'])
                formEsqueci.lbl_senha.setText(user['SenhaAluno'])
                formEsqueci.alert.setText('')
                formEsqueci.alert.setStyleSheet('')
                formEsqueci.NomeCompleto.setText('')
            except:
                formEsqueci.NomeCompleto.setText('')
                formEsqueci.alert.setStyleSheet(alertDanger)
                formEsqueci.alert.setText("Não foi possível validar os dados. Tente novamente!")
                formEsqueci.lbl_usuario.setText('')
                formEsqueci.lbl_senha.setText('')
                formEsqueci.frame_dados.setStyleSheet('')
        else:
            user = r.get("http://192.168.1.11/presencas/controllers/getUserData.php?NomeAluno="+NomeAluno)
            user2 = json.loads(user.content)
            try:
                formEsqueci.lbl_usuario.setText('')
                formEsqueci.lbl_senha.setText('')
                formEsqueci.alert.setStyleSheet(alertDanger)
                formEsqueci.alert.setText(user2['message'])
                formEsqueci.NomeCompleto.setText('')
                formEsqueci.frame_dados.setStyleSheet('')
            except:
                formEsqueci.NomeCompleto.setText('')
                formEsqueci.alert.setStyleSheet('')
                formEsqueci.alert.setText('')
                formEsqueci.frame_dados.setStyleSheet(alertSuccess)
                formEsqueci.lbl_usuario.setText(str(user2['CodigoContrato']))
                try:
                    formEsqueci.lbl_senha.setText(user2['SenhaAluno'])
                except:
                    formEsqueci.lbl_senha.setText("Prep-123")
  

def abrirEsqueci():
    formEsqueci.show()
    btnBuscar = formEsqueci.btnBuscar
    btnBuscar.clicked.connect(getUserData)
    formEsqueci.NomeCompleto.returnPressed.connect(getUserData)

    
if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = uic.loadUi('presencas.ui')
    formEsqueci = uic.loadUi('esqueci.ui')
    ui = Ui_widget()
    ui.setupUi(MainWindow)
    MainWindow.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    ui.registrar.clicked.connect(marcarPresenca)
    ui.fechar_alert.clicked.connect(fecharAlert)
    ui.DataPresenca.setText(data_atual)
    ui.Computador.setText(socket.gethostname())
    ui.IpComputador.setText(socket.gethostbyname(socket.gethostname()))
    ui.DiaSemana.setText(weekday)
    ui.DataPresenca.setStyleSheet('color:transparent;background:transparent;border:none;')
    ui.Computador.setStyleSheet('color:transparent;background:transparent;border:none;')
    ui.IpComputador.setStyleSheet('color:transparent;background:transparent;border:none;')
    ui.DiaSemana.setStyleSheet('color:transparent;background:transparent;border:none;')
    ui.btnEsqueci.clicked.connect(abrirEsqueci)
    sys.exit(app.exec_())
