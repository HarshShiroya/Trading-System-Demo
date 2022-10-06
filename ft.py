from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
import pandas as pd
from datetime import datetime,date,timedelta
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QLabel
from PyQt5.QtCore import QAbstractTableModel, Qt, QTimer, QThread
from PyQt5.QtGui import QMovie
from smartapi import SmartConnect
import math, os
import pprint as pp
from time import time, sleep
from pprint import pprint
pd.options.mode.chained_assignment = None

class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.label_animation = QLabel(self)

        self.movie = QMovie((os.path.join(pth,'data','loading.gif')))
        self.label_animation.setMovie(self.movie)

        timer = QTimer(self)
        self.startAnimation()
        timer.singleShot(10000, self.stopAnimation)

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        MainWindow.show()
        self.movie.stop()
        self.close()

class Client:
    def __init__(self, code, password, capital) -> None:
        self.code = code
        self.password = password 
        self.capital = capital
        self.obj = SmartConnect(api_key='cNFet6Dy')
        self.data = self.obj.generateSession(code,password)
        self.profile = self.obj.getProfile(self.data['data']['refreshToken'])
        self.holdings = self.obj.holding()
        self.positions = self.obj.position()
    
    def getquantity(self, price):
        div = self.capital / 10
        quantity = div / price
        return math.floor(quantity)

    def gethpquantity(self, symbol):
        sym = symbol
        try:
            for i in range(0,len(self.holdings['data'])):
                # print(c1.holdings['data'][i]['tradingsymbol'])
                if self.holdings['data'][i]['tradingsymbol'] == sym:
                    return self.holdings['data'][i]['quantity']
            return 0
        except Exception as e:
            print(e)
            return 0

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(797, 602)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 791, 561))
        self.tabWidget.setObjectName("tabWidget")
        self.mainWindow = QtWidgets.QWidget()
        self.mainWindow.setObjectName("mainWindow")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.mainWindow)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 781, 31))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.fsymbol = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.fsymbol.setObjectName("fsymbol")
        self.horizontalLayout_2.addWidget(self.fsymbol)
        self.ftoken = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.ftoken.setObjectName("ftoken")
        self.horizontalLayout_2.addWidget(self.ftoken)
        self.fquantity = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.fquantity.setObjectName("fquantity")
        self.horizontalLayout_2.addWidget(self.fquantity)
        self.fprice = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.fprice.setObjectName("fprice")
        self.horizontalLayout_2.addWidget(self.fprice)
        self.ftprice = QtWidgets.QTextEdit(self.horizontalLayoutWidget_2)
        self.ftprice.setObjectName("ftprice")
        self.horizontalLayout_2.addWidget(self.ftprice)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.mainWindow)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 40, 501, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.buyBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.buyBtn.setObjectName("buyBtn")
        self.horizontalLayout_3.addWidget(self.buyBtn)
        self.sellBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.sellBtn.setObjectName("sellBtn")
        self.horizontalLayout_3.addWidget(self.sellBtn)
        self.checkBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.checkBtn.setObjectName("checkBtn")
        self.horizontalLayout_3.addWidget(self.checkBtn)
        self.error1Text = QtWidgets.QLabel(self.mainWindow)
        self.error1Text.setGeometry(QtCore.QRect(156, 510, 501, 20))
        self.error1Text.setText("")
        self.error1Text.setObjectName("error1Text")
        self.error1Text.setAlignment(Qt.AlignCenter)
        self.textBrowser = QtWidgets.QTextBrowser(self.mainWindow)
        self.textBrowser.setGeometry(QtCore.QRect(0, 70, 781, 431))
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser.setAcceptRichText(True)
        self.tabWidget.addTab(self.mainWindow, "")
        self.getToken = QtWidgets.QWidget()
        self.getToken.setObjectName("getToken")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.getToken)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 451, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.symbol = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.symbol.setObjectName("symbol")
        self.symbol.addItem("")
        self.symbol.addItem("")
        self.horizontalLayout.addWidget(self.symbol)
        self.segmentType = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.segmentType.setObjectName("segmentType")
        self.segmentType.addItem("")
        self.segmentType.addItem("")
        self.horizontalLayout.addWidget(self.segmentType)
        self.stikePrice = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.stikePrice.setObjectName("stikePrice")
        self.horizontalLayout.addWidget(self.stikePrice)
        self.optionType = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.optionType.setObjectName("optionType")
        self.optionType.addItem("")
        self.optionType.addItem("")
        self.horizontalLayout.addWidget(self.optionType)
        self.subBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.subBtn.setObjectName("subBtn")
        self.horizontalLayout.addWidget(self.subBtn)
        self.resData = QtWidgets.QTableView(self.getToken)
        self.resData.setGeometry(QtCore.QRect(0, 40, 781, 461))
        self.resData.setObjectName("resData")
        self.errorText = QtWidgets.QLabel(self.getToken)
        self.errorText.setGeometry(QtCore.QRect(90, 510, 571, 20))
        self.errorText.setAlignment(Qt.AlignCenter)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.errorText.setPalette(palette)
        self.errorText.setText("")
        self.errorText.setObjectName("errorText")
        self.tabWidget.addTab(self.getToken, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 797, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.subBtn.clicked.connect(self.pressed)
        self.buyBtn.clicked.connect(self.bpressed)
        self.sellBtn.clicked.connect(self.spressed)
        self.checkBtn.clicked.connect(self.checkmtom)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TechFin"))
        MainWindow.setWindowIcon(QtGui.QIcon((os.path.join(pth,'data','logo.png'))))
        self.comboBox.setItemText(0, _translate("MainWindow", "MARKET"))
        self.comboBox.setItemText(1, _translate("MainWindow", "LIMIT"))
        self.comboBox.currentTextChanged.connect(self.onCurrentTextChanged)
        self.fsymbol.setPlaceholderText(_translate("MainWindow", "Enter Symbol"))
        self.ftoken.setPlaceholderText(_translate("MainWindow", "Enter Token"))
        self.fquantity.setPlaceholderText(_translate("MainWindow", "Enter Quantity"))
        self.fprice.setPlaceholderText(_translate("MainWindow", "Enter Price"))
        self.ftprice.setPlaceholderText(_translate("MainWindow", "Enter Trigger Price"))
        self.fprice.setReadOnly(True)
        self.ftprice.setReadOnly(True)
        self.buyBtn.setText(_translate("MainWindow", "Buy"))
        self.sellBtn.setText(_translate("MainWindow", "Sell"))
        self.checkBtn.setText(_translate("MainWindow", "Check Pnl"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainWindow), _translate("MainWindow", "FMMI"))
        self.symbol.setItemText(0, _translate("MainWindow", "NIFTY"))
        self.symbol.setItemText(1, _translate("MainWindow", "BANKNIFTY"))
        self.segmentType.setItemText(0, _translate("MainWindow", "OPTION"))
        self.segmentType.setItemText(1, _translate("MainWindow", "FUTURE"))
        self.segmentType.currentTextChanged.connect(self.onCurrentTextChanged)
        self.stikePrice.setPlaceholderText(_translate("MainWindow", "Stirke Price"))
        self.optionType.setItemText(0, _translate("MainWindow", "CE"))
        self.optionType.setItemText(1, _translate("MainWindow", "PE"))
        self.subBtn.setText(_translate("MainWindow", "SUBMIT"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.getToken), _translate("MainWindow", "Get Data"))

    def onCurrentTextChanged(self):
        txt = self.comboBox.currentText()
        seg = self.segmentType.currentText()
        if txt == 'MARKET':
            self.fprice.setReadOnly(True)
            self.ftprice.setReadOnly(True)
        if txt == 'LIMIT':
            self.fprice.setReadOnly(False)
            self.ftprice.setReadOnly(False)

        if seg == 'FUTURE':
            self.stikePrice.setReadOnly(True)
        if seg == 'OPTION':
            self.stikePrice.setReadOnly(False)


    def place_orderts(self,token,symbol,qty,buy_sell,ordertype,price,triggerprice,variety= 'NORMAL',exch_seg='NFO'):
        self.textBrowser.clear()
        for i in range(len(df)):
            try:
                orderparams = {
                    "variety": variety,
                    "tradingsymbol": symbol,
                    "symboltoken": token,
                    "transactiontype": buy_sell,
                    "exchange": exch_seg,
                    "ordertype": ordertype,
                    "producttype": 'CARRYFORWARD',
                    "duration": "DAY",
                    "price": price,
                    "quantity": qty,
                    "triggerprice":triggerprice
                    }
                rule_id = globals()[f"c{i}"].obj.placeOrder(orderparams)
                print("The order id is: {}".format(rule_id))
                self.textBrowser.append(globals()[f"c{i}"].code + ' :- ' + "The order id is: {}".format(rule_id) )
            except Exception as e:
                sleep(1)
                try:
                    orderID = globals()[f"c{i}"].obj.placeOrder(orderparams)
                    print("The order id is: {}".format(orderID))
                    self.textBrowser.append(globals()[f"c{i}"].code + ' :- ' + "The order id is: {}".format(orderID))
                except Exception as e: 
                    sleep(1)
                    try:
                        orderID = globals()[f"c{i}"].obj.placeOrder(orderparams)
                        print("The order id is: {}".format(orderID))
                        self.textBrowser.append(globals()[f"c{i}"].code + ' :- ' + "The order id is: {}".format(orderID))
                    except Exception as e:
                        print("Order placement failed: {}".format(e))
                        self.textBrowser.append(globals()[f"c{i}"].code + ' :- ' + "Order placement failed: " + e)

    def checkmtom(self):
        self.errorText.setText('')
        self.textBrowser.clear()
        for i in range(len(df)):
            try:
                for j in range(0,len(globals()[f"c{i}"].positions['data'])):
                    # pprint(globals()[f"c{i}"].positions['data'][j]['tradingsymbol'],globals()[f"c{i}"].positions['data'][j]['pnl'])
                    # print(globals()[f"c{i}"].code, ' :- ',globals()[f"c{i}"].positions['data'][j]['tradingsymbol'], ':' ,globals()[f"c{i}"].positions['data'][j]['pnl'])
                    self.textBrowser.append(globals()[f"c{i}"].code + ' :- '+globals()[f"c{i}"].positions['data'][j]['tradingsymbol'] + ":" + globals()[f"c{i}"].positions['data'][j]['pnl'] )
            except Exception as e:
                # print("No positions")
                # self.error1Text.setText('No Positions')
                self.textBrowser.append(globals()[f"c{i}"].code  + ":-" + "No Positions")
                


    def getTokenInfo (self,symbol, exch_seg ='NSE',instrumenttype='OPTIDX',strike_price = '',pe_ce = '',expiry_day = None):
        df = token_df
        strike_price = strike_price*100
        if exch_seg == 'NSE':
            eq_df = df[(df['exch_seg'] == 'NSE') ]
            return eq_df[eq_df['name'] == symbol]
        elif exch_seg == 'NFO' and ((instrumenttype == 'FUTSTK') or (instrumenttype == 'FUTIDX')):
            return df[(df['exch_seg'] == 'NFO') & (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol)].sort_values(by=['expiry'])
        elif exch_seg == 'NFO' and (instrumenttype == 'OPTSTK' or instrumenttype == 'OPTIDX'):
            return df[(df['exch_seg'] == 'NFO')  &  (df['instrumenttype'] == instrumenttype) & (df['name'] == symbol) & (df['strike'] == strike_price) & (df['symbol'].str.endswith(pe_ce))].sort_values(by=['expiry'])

    def pressed(self):
        self.errorText.setText('')
        sym = self.symbol.currentText()
        seg = self.segmentType.currentText()
        try:

            if seg == 'FUTURE':
                res = self.getTokenInfo(sym,'NFO','FUTIDX')
                res = res.reset_index(drop=True)
                res = res.drop(['strike', 'instrumenttype', 'exch_seg', 'tick_size'], axis=1)
                model = pandasModel(res)
                self.resData.setModel(model)

            if seg == 'OPTION':
                sp = int(self.stikePrice.toPlainText())
                op = self.optionType.currentText()
                res = self.getTokenInfo(sym,'NFO','OPTIDX',sp,op)
                res = res.reset_index(drop=True)
                res = res.drop(['strike', 'instrumenttype', 'exch_seg', 'tick_size'], axis=1)
                model = pandasModel(res)
                self.resData.setModel(model)
        except Exception as e:
            self.errorText.setText('Invalid Input')

    def bpressed(self):
        self.error1Text.setText('')
        try:
            ordtype = self.comboBox.currentText()
            sym = self.fsymbol.toPlainText()
            tkn = int(self.ftoken.toPlainText())
            qt = int(self.fquantity.toPlainText())
            # print(ordtype,sym,tkn,qt)

            if ordtype == 'MARKET':
                self.place_orderts(tkn,sym,qt,"BUY",ordtype,0,0)
            if ordtype == 'LIMIT':
                p = int(self.fprice.toPlainText())
                tp = int(self.ftprice.toPlainText())
                self.place_orderts(tkn,sym,qt,"BUY",ordtype,p,tp)
        except Exception as e:
            self.error1Text.setText('Invalid Input')

    def spressed(self):
        self.error1Text.setText('')
        try:
            ordtype = self.comboBox.currentText()
            sym = self.fsymbol.toPlainText()
            tkn = int(self.ftoken.toPlainText())
            qt = int(self.fquantity.toPlainText())
            # print(ordtype,sym,tkn,qt)

            if ordtype == 'MARKET':
                self.place_orderts(tkn,sym,qt,"SELL",ordtype,0,0)
            if ordtype == 'LIMIT':
                p = int(self.fprice.toPlainText())
                tp = int(self.ftprice.toPlainText())
                self.place_orderts(tkn,sym,qt,"SELL",ordtype,p,tp)
        except Exception as e:
            self.error1Text.setText('Invalid Input')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    loading_screen = LoadingScreen()


    pth = Path(__file__).parent.absolute()

    df = pd.read_csv(os.path.join(pth,'data','clients.csv'))

    clientCode = ''   
    password = ''   

    r = 0
    while(r < 2):
        try:
            for i in range(len(df)):
                lc = df.iloc[i]
                # print(lc['Code'],lc['Pass'])
                globals()[f"c{i}"] = Client(lc['Code'],lc['Pass'],100000)
            
            obj=SmartConnect(api_key='oVSg38L0')
            data = obj.generateSession(clientCode, password)
            r = 5
            ui.error1Text.setText('Authentication Successful.')
            # print(obj.holding())
        except Exception as e:
            print(e, 'Authentication failed. Retrying...')
            ui.error1Text.setText('Authentication failed. Retrying...')
            


    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    d = requests.get(url).json()
    token_df = pd.DataFrame.from_dict(d)
    token_df['expiry'] = pd.to_datetime(token_df['expiry']).apply(lambda x: x.date())
    token_df = token_df.astype({'strike': float})

    # MainWindow.show()
    sys.exit(app.exec_())
