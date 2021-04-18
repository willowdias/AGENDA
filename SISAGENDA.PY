
from PyQt5 import QtGui
from PyQt5.QtGui import QMovie, QTextCursor
from PyQt5 import  uic, QtWidgets
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QCalendarWidget, QFormLayout, QLineEdit, QMessageBox, QPushButton, QTableWidgetItem, QTableWidget, QFileDialog, QHeaderView
from reportlab.pdfgen import canvas
from PyQt5.QtGui import QIcon
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch, cm
from PyQt5.QtWidgets import QPushButton,QLineEdit,QCompleter
from queryagenda import sqlite_db

class agenda(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(agenda, self).__init__()
        uic.loadUi('AGENDA.ui', self)
        self.show()
        #tamanho da tela
        startSize = QtCore.QSize(1080, 720)
        self.resize(startSize)
        self.setMinimumSize(startSize)
        ############################3#
        #icone
        self.setWindowIcon(QIcon("icon/agenda.ico"))
        self.setWindowTitle("OFF SISTEMA")#NOME SISTEMA
        
        self.ver_usuario_cliente()
    
        ######################gif#####################
        self.movie = QMovie("icon/giphy.gif")
        self.label_esquerdogif.setMovie(self.movie)
        self.label_direitogif.setMovie(self.movie)   
        self.movie.start()
        #self.movie.stop()
        #################################
        #CREATE BOTAO GERA PDF
        self.pushButton_gera_odf.clicked.connect(self.gera_pdf)
        
        ################tabela#cidade###########
        
        self.sistema_te = QTableWidget(self)
        self.sistema_te.setHorizontalHeaderLabels(["Header-1"])
        self.sistema_te.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sistema_te.move(850, 120)
        self.sistema_te.setColumnCount(1)
        self.sistema_te.setMinimumWidth(200)
        self.sistema_te.setMinimumHeight(500)
        self.sistema_te.verticalHeader().setVisible(False)
    #######################################
        #########complete cidaes###########
        self.mostra_bairro()#mostra bairros
        self.preencher_dados()
        self.ESTADOS_UF()#ver os estados banco de dados
        self.mostra_cidades()#ver cidades banco de dados                            
        ###########cadsatro de clientes###########
        self._2lineEdit_cpf.setInputMask("000.000.000.00;_")#cpf               
        self._8lineEdit_celular_tel.setValidator(QtGui.QIntValidator())#celular
        self._7lineEdit_data_nascimento.setInputMask("00/00/0000")#dada nascimento
        self._3lineEdit_idade.setValidator(QtGui.QIntValidator())#idade
        self._5lineEdit_numero.setValidator(QtGui.QIntValidator())#numero
    
        #cadastro cliente#####################################        
        self.Button_salva_2.clicked.connect(self.cadastro_cliente)
        self.Button_abrir_2.clicked.connect(self.ver_cidades)#ver cidades
        self.altera_clientes.clicked.connect(self.pesquisar_clientes)#altera clientes
        

        #tela clientes cadastrado##############
        self.volt_apagacliente.clicked.connect(self.apaga_clientes)#apagar cleintes

        #pagina atenidmento################################################
        #create alerta
        self.checkBox.toggled.connect(self.check_alerta)
        #data time
        #self.dateEdit.dateChanged.connect(self.data)#data
        #self.timeEdit.timeChanged.connect(self.horas)#horas
        self.pushButton_novo.clicked.connect(self.chamar_cliente_teladado)
        self.pushButton_confirma.clicked.connect(self.horas)
        self.pushButton_confirma.clicked.connect(self.data)
        self.pushButton_confirma.clicked.connect(self.tipodetecnico)
        self.pushButton_confirma.clicked.connect(self.atendimneto)
        self.pushButton_confirma.clicked.connect(self.SelectPAciente)#selecionar paciente0,
        #self.lineEdit_procuraclientes.textChanged.connect(self.pesquisar_clientes)#pesquisar clientes
        #########combox
        self.comboxprofissao_t()
        #self.combo_atendimento.activated.connect(self.atendimneto)
        #self.combo_profissao.activated.connect(self.tipodetecnico)
     ######tecla atalha pagina######$$$$$$$$$$$

        self.actionCadastro_atendimento.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.atendimento))
        self.actionCadastro_Client.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.cadastrocliente))#Cadastro cliente
        self.actionMostra_Clientes.triggered.connect(lambda: self.stackedWidget.setCurrentWidget(self.telaclientes))
        self.volt_cadastroclientes.clicked.connect(self.sistema2)#chama cadastro clientes
        self.bt_ver_clientes_2.clicked.connect(self.sistema_charma_botao_clientes)#ver clientes
        self.bt_link.clicked.connect(self.abri_zap)#chamar link whatsapp
        #PUXA DATA  ATUALLLLL#############
        self.date = QtCore.QDate.currentDate()
        self.dateEdit.setDate(self.date)
        self.timeEdit13 = QtCore.QTime.currentTime()
        self.timeEdit.setTime(self.timeEdit13) 
        #create pra chamar cliennte tela atendimento
        self.chamar_cliente_teladado()###chamar cliente
        self.chama_clientes.close()
        
    ##############fuçao teste #pra chama clientes##########################################################################
    def sistema_charma_botao_clientes(self):
        self.bt_ver_clientes_2==self.stackedWidget.setCurrentWidget(self.telaclientes)
    
    def sistema2(self):               
        self.stackedWidget.setCurrentWidget(self.cadastrocliente)
    
    
        
    def abri_zap(self):#chamar link whatsapp    
        buttonReply=QMessageBox.question(self, 'WHATSAPP LINK', "DESEJA DIRECIONAR WHATSAPP CLICKE EM HELP\n"+"\nSENAO DESEJA CLICKE EM NO", QMessageBox.No | QMessageBox.Help)
        if buttonReply==QMessageBox.Help:
            import webbrowser
            webbrowser.open(r'https://bityli.com/losoj')
        else:
            QMessageBox.about(self, "TITLE", "OBRIGADO VOLTE SEMPRE")     
    def SelectPAciente(self,):
        
        a=self.busca_cliente_atendimento.text()
        self.listWidget.addItem(f'PACIENTE: {a} ')
        self.busca_cliente_atendimento.setText("")
        self.chama_clientes.close()

    def chamar_cliente_teladado(self):
       
        self.chama_clientes.show()              
        self.ver_usuario_cliente()
        db = sqlite_db("agenda_bd.db")                   
        dados_lidos=db.pega_dados("SELECT nome FROM clientes")
        results = dados_lidos
        banco = [i[0] for i in results]
        completer = QCompleter(banco)
        self.busca_cliente_atendimento.setCompleter(completer)
    ###############################################################    
        
        

    ########combobox######################      
    def atendimneto(self):
        a=str(self.combo_atendimento.currentText())
        self.listWidget.addItem(a)  
    def tipodetecnico(self):
        text = str(self.combo_profissao.currentText())
        self.listWidget.addItem(f'Tecnico: {text} ')
       
    def comboxprofissao_t(self):#item da lista
        
        profissao=["","tecnico","analista","GERENTE"]
        lista=['offsistema.png','Agenda/icon/tecnico.png']
        self.combo_profissao.addItems(profissao)
        self.combo_atendimento.addItems(profissao)
        self.combo_profissao.setItemIcon(1, QIcon(lista[0]))#colocar icons
        self.combo_profissao.setItemIcon(2, QIcon(lista[1]))
        self.combo_profissao.setItemIcon(3, QIcon(lista[0]))
        self.combo_atendimento.setItemIcon(1, QIcon(lista[0]))
        self.combo_atendimento.setItemIcon(2, QIcon(lista[0]))
        self.combo_atendimento.setItemIcon(3, QIcon(lista[0]))         
    
    ###########combox########################
    #data time
    def data(self):#dat
        
     
        data_atual =self.dateEdit.date()
        
        self.listWidget.addItem(('Dia {0}/ Mês {1}/ Ano {2}  '.format(data_atual.day(), data_atual.month(), data_atual.year())))
     
    def horas(self):#horas  
        hora = self.timeEdit.time()                  
        self.listWidget.addItem(('Dados Cliente\n'+'Horas {0}:{1} Minutos'.format(hora.hour(),hora.minute())))
        
    #salva###############################
    def salvar_Dados(self):
        text=self.listWidget_dados.selectedItems()
        for y in text:
            print(y.text())
    def check_alerta(self,item):#alerta cliente agendado
        
        import time, sys
        bt=self.sender()
        buttonReply=QMessageBox.question(self, 'ALERTA', "CLIENTE ESPECIAL", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply==QMessageBox.Yes:        
            if bt.isChecked() == True:
                return
        else:
            print('Verdade')   
        
     
    
    #######cadastro cliente####
    def cadastro_cliente(self):
        db = sqlite_db("agenda_bd.db")
        cliente=str(self._1lineEdit_nome.text())
        idade_idade=str(self._3lineEdit_idade.text()) 
        cpf_cpf=str(self._2lineEdit_cpf.text())
        email_email=str(self._9lineEdit_email.text())
        end_endereco=str(self._4lineEdit_endereco.text())
        numer_n=str(self._5lineEdit_numero.text())
        cidade_cid=str(self._6lineEdit_cidade.text())
        bairro_bairro=str(self._lineEdit_bairro.text())
        completento_cop=str(self.lineEdit_complemento.text())
        data_nc=str(self._7lineEdit_data_nascimento.text())
        sexo_sexo = str(self.comboBox_sexo.currentText())
        tb_telefone=str(self._8lineEdit_celular_tel.text())
        estado_tb = str(self.comboBox_estados.currentText())
        if (cliente==""or idade_idade=="" or cpf_cpf=="" or email_email==""or end_endereco=="" or numer_n==""or
        cidade_cid==""or bairro_bairro==""or completento_cop==""or data_nc==""or sexo_sexo==""or tb_telefone==""or estado_tb==""):
        
            return QMessageBox.about(self, "Title", "PREENCHAR OS DADOS")
        else:
            buttonReply=QMessageBox.question(self, 'CADASTRO CLIENTE', "DESEJA CADASTRA CLIENTE", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply==QMessageBox.Yes:  
                db.adicionar("INSERT INTO  clientes (nome,idade,cpf,email,endereco,numero,cidade,bairro,complemento,data_n,sexo,telefone,estado)VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(cliente,idade_idade,cpf_cpf,email_email,end_endereco,numer_n,cidade_cid,bairro_bairro,completento_cop,data_nc,sexo_sexo,tb_telefone,estado_tb))
                QMessageBox.about(self, "Title", "USUARIO CADASTRO COM SUCESSO")
                self.ver_usuario_cliente()

    #######################################################################################################
    def ver_usuario_cliente(self):
        db = sqlite_db("agenda_bd.db")
        
        try:    
            dados_lidos=db.pega_dados("SELECT * FROM clientes")
            self.tableWidget_clientes_3.setRowCount(0)
            self.tableWidget_clientes_3.resizeColumnToContents(0)
            for linha, dados in enumerate (dados_lidos):
                self.tableWidget_clientes_3.insertRow(linha)
                for coluna_n, dados in enumerate(dados):
                    self.tableWidget_clientes_3.setItem(linha,coluna_n,QTableWidgetItem(str(dados)))
        except:
            print()
    ###################apaga clientes###########
    def apaga_clientes(self):#apaga cliente tela cadastro clientes
        buttonReply=QMessageBox.question(self, 'APAGAR CLIENTE', "DESEJA APAGA CLIENTE", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply==QMessageBox.Yes:
            try:
                db = sqlite_db("agenda_bd.db")    
                linha=self.tableWidget_clientes_3.currentRow()
                self.tableWidget_clientes_3.removeRow(linha)
                dados=db.pega_dados("SELECT id FROM clientes")
                valor_id = dados[linha][0]
                db.apaga("DELETE FROM clientes WHERE id=" + str(valor_id))
                self.ver_usuario_cliente()
            except:
                QMessageBox.about(self, "Title", "CLIENTE APAGADO COM SUCESSO")  
            
        
            
            QMessageBox.about(self, "Title", "CLIENTE APAGADO COM SUCESSO")  
            self.ver_usuario_cliente()    
    def pesquisar_clientes(self):
        pass

    def preencher_dados(self):#preencher dados telefone
        banco=['(69)','+5569','99s']
 
        completer = QCompleter(banco)
        self._8lineEdit_celular_tel.setCompleter(completer)       
        
    ####################################################################################################### 

        def openfile(self):#abri texto
            filename = QFileDialog.getOpenFileName(self)
            self.lb1.setText(filename[0]) 
    ################REFERENTECIDADES######################ESTADOS####################$$$$$

    def ver_cidades(self):
        buttonReply=QMessageBox.question(self, 'CIDADES', "DESEJA VER CIDADES", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply==QMessageBox.Yes:  
                   
            db = sqlite_db("agenda_bd.db")
            try:    
                dados_lidos=db.pega_dados("SELECT * FROM cidades")
                for linha, dados in enumerate (dados_lidos):
                    self.sistema_te.insertRow(linha)
                    for coluna_n, dados in enumerate(dados):
                        self.sistema_te.setItem(linha,coluna_n,QTableWidgetItem(str(dados)))
                        self.sistema_te.show()    
            except:
                print('error')
        if buttonReply==QMessageBox.No:
            self.sistema_te.close()    
    def ESTADOS_UF(self):#mostra os estados  
        db = sqlite_db("agenda_bd.db")   
        dados_lidos=db.pega_dados(" SELECT uf FROM estados ")
        banco = [i[0] for i in dados_lidos] 
        self.comboBox_estados.addItems(banco)
    def mostra_cidades(self):#mostra cidades 
        db = sqlite_db("agenda_bd.db")       
        dados_lidos=db.pega_dados(" SELECT cidade  FROM cidades")
        banco = [i[0] for i in dados_lidos] 
        completer = QCompleter(banco)
        self._6lineEdit_cidade.setCompleter(completer)
    def mostra_bairro(self):#mostra cidades
        db = sqlite_db("agenda_bd.db")
        dados_lidos=db.pega_dados(" SELECT bairro  FROM bairros")
        banco = [i[0] for i in dados_lidos] 
        completer = QCompleter(banco)
        self._lineEdit_bairro.setCompleter(completer) 
    def procura_cliente(self):
        b=self.linewillow2.text()
        print(b)   
    #####################################
    #create gera pdf
    def gera_pdf(self):
        row = self.tableWidget_clientes_3.currentRow()
        print(row)
        db = sqlite_db("agenda_bd.db")                   
        dados_lidos=db.pega_dados("SELECT *FROM clientes WHERE id={}".format(row))
        
        y = 0
        import time
        data_atual=time.strftime('%d-%m-%Y horas: %H:%M:%S', time.localtime())
        
        logo = ImageReader('offsistema.png')#logo                
        pdf = canvas.Canvas('{}.pdf'.format("OFF PACIENTES"))
        pdf.drawImage(logo, 400, 700,5*cm, 5*cm)#logo                
        pdf.drawString(35,724,'='*20+ 'Dados cliente  '+'='*20)
        pdf.drawString(35,750,'='*20+'OFF SISTEMA'+'='*20)
        pdf.drawString(10,5, f'Data: {data_atual}')

        pdf.drawString(30, 700, 'ID')
        pdf.drawString(30, 680, 'Nome: ')#nome
        pdf.drawString(250, 680, 'Data Nascimento : ')#NSACIMENTO
        pdf.drawString(430, 680, 'Idade: ')#idade
        pdf.drawString(30, 660, 'CPF: ')#cpf
        pdf.drawString(150, 660, 'Sexo: ')#SEXO
        pdf.drawString(240, 660, 'Email: ')#
        pdf.drawString(445, 660, 'Telefone: ')#telefone
        pdf.drawString(30, 640, 'Endereço: ')#ENDEREÇO
        pdf.drawString(270, 640, 'Nº: ')#NUMERO
        pdf.drawString(330, 640, 'Cidade: ')#CIDADE
        pdf.drawString(410, 640, 'Bairro: ')#BAIRRO
        pdf.drawString(515, 640, 'UF: ')#BAIRRO
        pdf.drawString(30, 620, 'Complemento: ')#COMPLEMENTO
        
        pdf.line(30,675,580,675)#linha cliente
        pdf.line(30,655,580,655)#enederço A telefone
        pdf.line(30,635,580,635)#linha cliente
        pdf.line(30,615,580,615)#complementos
        for i in range(0, len(dados_lidos)):
            y = y + 50
            pdf.drawString(50, 750 - y, str(dados_lidos[i][0]))#id
            pdf.drawString(75, 730 - y, str(dados_lidos[i][1]))#NOME
            pdf.drawString(350, 730 - y, str(dados_lidos[i][10]))#DATA DE NASCIMENTO
            pdf.drawString(480, 730 - y, str(dados_lidos[i][2]))#IDADE
            pdf.drawString(60, 710 - y, str(dados_lidos[i][3]))#CPF
            pdf.drawString(180, 710 - y, str(dados_lidos[i][11]))#SEXO
            pdf.drawString(275, 710 - y, str(dados_lidos[i][4]))#EMAIL
            pdf.drawString(500, 710 - y, str(dados_lidos[i][12]))#TELEFONE
            pdf.drawString(95, 690 - y, str(dados_lidos[i][5]))#ENDEREÇO###
            pdf.drawString(290, 690 - y, str(dados_lidos[i][6]))#NUMERO##3
            pdf.drawString(375, 690 - y, str(dados_lidos[i][7]))#CIDADE
            pdf.drawString(450, 690 - y, str(dados_lidos[i][8]))#BAIRRO
            pdf.drawString(540, 690 - y, str(dados_lidos[i][13]))#estado
            pdf.drawString(110, 670 - y, str(dados_lidos[i][9]))#COMPLEMENTO
            
            
            
            # background: url("D:/pytho willow/agenda/icon/LOGO FUNDO.png") no-repeat;
            pdf.save()
            QMessageBox.about(self, "PDF", "O PDF FOI GERADO COM SUCESSO")
            print('O PDF FOI GERADO COM SUCESSO')
        ###################

   
        


    

if __name__ == '__main__':
        
  

    app = QtWidgets.QApplication([])
    #window = QtWidgets.QMainWindow()
    demo = agenda()
    demo.show()
    sys.exit(app.exec_())