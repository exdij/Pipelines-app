from fbs_runtime.application_context.PyQt5 import ApplicationContext
import sys
from PyQt5 import uic
from PyQt5.QtCore import QFile, QIODevice, QTimer
from request import getEnviromentInfo
from PyQt5.QtGui import QIcon
import datetime

import sys


def setEnviromentsInfo():
    setDev()
    setUat()
    setPreProd()
    setProd()

def setDev():
    devUrl = 'https://timeports2-backend-dev.test.jit.ninja'

    info = getEnviromentInfo(devUrl)
    window.devTimestamp.setText(info['timestamp'])
    window.devSourceBranch.setText(info['sourceBranch'])
    window.devAuthor.setText(info['author'])
    window.devJenkinsNumber.setText(info['jenkinsNumber'])
    window.devCommitMessage.setText(info['commitMessage'])

def setUat():
    uatUrl = 'https://timeports2-backend-uat.test.jit.ninja'

    info = getEnviromentInfo(uatUrl)
    window.uatTimestamp.setText(info['timestamp'])
    window.uatSourceBranch.setText(info['sourceBranch'])
    window.uatAuthor.setText(info['author'])
    window.uatJenkinsNumber.setText(info['jenkinsNumber'])
    window.uatCommitMessage.setText(info['commitMessage'])

def setPreProd():
    preProdUrl = 'https://timeports2-backend-preprod.prod.jit.ninja'

    info = getEnviromentInfo(preProdUrl)
    window.pprodTimestamp.setText(info['timestamp'])
    window.pprodSourceBranch.setText(info['sourceBranch'])
    window.pprodAuthor.setText(info['author'])
    window.pprodJenkinsNumber.setText(info['jenkinsNumber'])
    window.pprodCommitMessage.setText(info['commitMessage'])

def setProd():
    prodUrl = 'https://timeports2-backend-prod.prod.jit.ninja'

    info = getEnviromentInfo(prodUrl)
    window.prodTimestamp.setText(info['timestamp'])
    window.prodSourceBranch.setText(info['sourceBranch'])
    window.prodAuthor.setText(info['author'])
    window.prodJenkinsNumber.setText(info['jenkinsNumber'])
    window.prodCommitMessage.setText(info['commitMessage'])

def startTimer():
    if(window.timerEnabled.checkState() == 2):
        msec = getTimerMsec()
        timer.start(msec)

def stopTimer():
    timer.stop()

def checkBox(state):
    if(state == 2):
        startTimer()
    else:
        stopTimer()

def getTimerMsec():
    minutes = window.updateFreq.time().minute()
    seconds = window.updateFreq.time().second()
    return minutes * 60 * 1000 + seconds * 1000


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    file = appctxt.get_resource('pipelines.ui')
    logo = appctxt.get_resource('logo.png')
    ui_logo = QIcon(logo)
    ui_file = QFile(file)

    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {file}: {ui_file.errorString()}")
        sys.exit(-1)
    window = uic.loadUi(ui_file)
    ui_file.close()

    window.setWindowIcon(ui_logo)
    window.show()
    
    setEnviromentsInfo()
    timer = QTimer()
    timer.timeout.connect(setEnviromentsInfo)
    window.timerEnabled.stateChanged.connect(checkBox)
    window.updateFreq.dateTimeChanged.connect(startTimer)
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)