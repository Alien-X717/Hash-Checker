import gui,hashlib,os
from PyQt5 import QtWidgets
BLOCK_SIZE=65536

class HashChk(gui.Ui_MainWindow):
    
    def __init__(self, *args, **kwargs):
        super(gui.Ui_MainWindow, self).__init__(*args, **kwargs)
        self.file_chosed=None
        
    def logic(self):
        self.file_choser.clicked.connect(self.file_opener)
        self.check.clicked.connect(self.checkHash)
        self.check.setDisabled(True)
    
    def file_opener(self):
        self.file_chosed = QtWidgets.QFileDialog.getOpenFileName()[0]
        if self.file_chosed:
            filenm = self.file_chosed.split("/")[-1]
            self.file_choser.setText(filenm)
            self.file_size = os.stat(self.file_chosed).st_size
            self.status.setText("size: "+str(int(self.file_size)/1024)+" KB")
            self.check.setEnabled(True)
            
    def checkHash(self): 
        if self.file_chosed !=None:
            hashtypes = [
                {'method':hashlib.md5(),'label':self.md5,'inpVal':self.md5_ip,'result':self.md5result},
                {'method':hashlib.sha1(),'label':self.sha1,'inpVal':self.sha1_ip,'result':self.sha1result},
                {'method':hashlib.sha224(),'label':self.sha224,'inpVal':self.sha224_ip,'result':self.sha224result},
                {'method':hashlib.sha256(),'label':self.sha256,'inpVal':self.sha256_ip,'result':self.sha256result},
                {'method':hashlib.sha384(),'label':self.sha384,'inpVal':self.sha384_ip,'result':self.sha384result},
                {'method':hashlib.sha512(),'label':self.sha512,'inpVal':self.sha512_ip,'result':self.sha512result},
            ]
            for hash in hashtypes:
                hash['label'].setText('')
                hash['result'].setText('')
 
            prct_gain = (BLOCK_SIZE*100)/self.file_size
            self.status.setText("Calculating")
            with open(self.file_chosed,'rb') as file:
                 
                percent = 0
                file.seek(0,0)
                while True:
                    seg= file.read(BLOCK_SIZE)
                    if not seg:
                        break
                    hashtypes[0]['method'].update(seg)
                    hashtypes[1]['method'].update(seg)
                    hashtypes[2]['method'].update(seg)
                    hashtypes[3]['method'].update(seg)
                    hashtypes[4]['method'].update(seg)
                    hashtypes[5]['method'].update(seg)
                    percent +=prct_gain
                    self.progress.setValue(percent)
                file.close()
            
            for hashType in hashtypes:
                calc_hash = str(hashType['method'].hexdigest()).upper()
                hashType['label'].setText(calc_hash)
                inp_val = str(hashType['inpVal'].text()).upper()
                if len(inp_val)>0:
                    if inp_val == calc_hash:  
                        hashType['result'].setText(u'\u2705' + "Correct")
                    else:
                        hashType['result'].setText(u'\u274C' + "In-Correct")
                    
            self.status.setText("Completed")
        else:
            pass        
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = HashChk()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.logic()
    sys.exit(app.exec_())