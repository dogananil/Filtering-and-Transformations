#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 00:14:00 2018

@author: anildogan
"""
import sys
from PyQt5.QtWidgets import QMainWindow,QMessageBox, QApplication, QWidget, QAction, QGroupBox, QFileDialog, QLabel, QVBoxLayout, QGridLayout, QHBoxLayout,QFrame, QSplitter,QSizePolicy
from PyQt5.QtGui import  QPixmap,QImage
from PyQt5.QtCore import  Qt
import cv2
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math
from scipy.misc import imsave
class App(QMainWindow):
    
    def __init__(self):
        super(App,self).__init__()
        
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
    
        self.inputBox = QGroupBox('Input')
        inputLayout = QVBoxLayout()
        self.inputBox.setLayout(inputLayout)
        
        self.layout = QGridLayout()
        self.layout.addWidget(self.inputBox, 0, 0)
        
        self.window.setLayout(self.layout)
        
        self.image = None
        self.temp = None
        self.temp2 = None
        self.tmp_im = None
        self.imagepad = None
        self.pad = None
        self.filtered = None
        self.saveImage = None
        self.figure = Figure()
        self.figure2 = Figure()
        self.figure3 = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas3 = FigureCanvas(self.figure3)
        self.lookupRed = np.zeros((256,1))
        self.lookupGreen = np.zeros((256,1))
        self.lookupBlue = np.zeros((256,1))
        self.eq = None
        self.qImg = None
        self.qImg2 = None
        self.qImgResult = None
        self.pixmap01 = None
        self.pixmap_image = None
       
        self.createActions()
        self.createMenu()
        ##self.createToolBar()
        
        self.setWindowTitle("Histogram")
        self.showMaximized()
        self.show()
        
        
    def createActions(self):
        
######## FILE MENU PART ######################################################
        self.openAct = QAction(' &Open',self)
        self.openAct.triggered.connect(self.openI)
        self.saveAct = QAction(' &Save', self)
        self.saveAct.triggered.connect(self.save)
        self.exitAct = QAction(' &Exit', self)
        self.exitAct.triggered.connect(self.exit)
        
######## FILTER MENU PART ######################################################   
        ####Average Menu#######
        self.athreex = QAction(' &3x3',self)
        self.athreex.triggered.connect(lambda:self.averageFilters(3))
        self.afivex = QAction (' &5x5',self)
        self.afivex.triggered.connect(lambda:self.averageFilters(5))
        self.asevenx = QAction(' &7x7',self)
        self.asevenx.triggered.connect(lambda:self.averageFilters(7))
        self.aninex = QAction(' &9x9',self)
        self.aninex.triggered.connect(lambda:self.averageFilters(9))
        self.aelevenx = QAction(' &11x11',self)
        self.aelevenx.triggered.connect(lambda:self.averageFilters(11))
        self.athirteenx = QAction(' &13x13',self)
        self.athirteenx.triggered.connect(lambda:self.averageFilters(13))
        self.afifteenx = QAction(' &15x15',self)
        self.afifteenx.triggered.connect(lambda:self.averageFilters(15))
        ####Gaussian Menu######
        self.gthreex = QAction(' &3x3',self)
        self.gthreex.triggered.connect(lambda:self.gaussianFilters(3))
        self.gfivex = QAction (' &5x5',self)
        self.gfivex.triggered.connect(lambda:self.gaussianFilters(5))
        self.gsevenx = QAction(' &7x7',self)
        self.gsevenx.triggered.connect(lambda:self.gaussianFilters(7))
        self.gninex = QAction(' &9x9',self)
        self.gninex.triggered.connect(lambda:self.gaussianFilters(9))
        self.gelevenx = QAction(' &11x11',self)
        self.gelevenx.triggered.connect(lambda:self.gaussianFilters(11))
        self.gthirteenx = QAction(' &13x13',self)
        self.gthirteenx.triggered.connect(lambda:self.gaussianFilters(13))
        self.gfifteenx = QAction(' &15x15',self)
        self.gfifteenx.triggered.connect(lambda:self.gaussianFilters(15))
        ####Median Menu########
        self.mthreex = QAction(' &3x3',self)
        self.mthreex.triggered.connect(lambda:self.medianFilters(3))
        self.mfivex = QAction (' &5x5',self)
        self.mfivex.triggered.connect(lambda:self.medianFilters(5))
        self.msevenx = QAction(' &7x7',self)
        self.msevenx.triggered.connect(lambda:self.medianFilters(7))
        self.mninex = QAction(' &9x9',self)
        self.mninex.triggered.connect(lambda:self.medianFilters(9))
        self.melevenx = QAction(' &11x11',self)
        self.melevenx.triggered.connect(lambda:self.medianFilters(11))
        self.mthirteenx = QAction(' &13x13',self)
        self.mthirteenx.triggered.connect(lambda:self.medianFilters(13))
        self.mfifteenx = QAction(' &15x15',self)
        self.mfifteenx.triggered.connect(lambda:self.medianFilters(15))

######## GEOMETRİC TRANSFORMS MENU PART ######################################## 
        ####Rotate Menu#######
        self.rotateRight = QAction(' &Rotate 10 Degree Right',self)
        self.rotateRight.triggered.connect(self.rotRight)
        self.rotateLeft = QAction(' &Rotate 10 Degree Left',self)
        ####Scale Menu########
        self.twice = QAction(' &2x',self)
        self.half = QAction(' &1/2x',self)
        ####Translate Menu####
        self.right = QAction(' &Right',self)
        self.left = QAction(' &Left',self)
    
    def createMenu(self):
        self.mainMenu = self.menuBar()
######## FILE MENU PART ######################################################
        self.fileMenu = self.mainMenu.addMenu('File')
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.exitAct)
 ######## FILTER MENU PART ######################################################        
        self.filterMenu = self.mainMenu.addMenu('Filters')
        ####Average Menu#######
        self.averageMenu = self.filterMenu.addMenu('Average Filters')
        self.averageMenu.addAction(self.athreex)
        self.averageMenu.addAction(self.afivex)
        self.averageMenu.addAction(self.asevenx)
        self.averageMenu.addAction(self.aninex)
        self.averageMenu.addAction(self.aelevenx)
        self.averageMenu.addAction(self.athirteenx)
        self.averageMenu.addAction(self.afifteenx)
        ####Gaussian Menu#######        
        self.gauMenu = self.filterMenu.addMenu('Gaussian Filters')
        self.gauMenu.addAction(self.gthreex)
        self.gauMenu.addAction(self.gfivex)
        self.gauMenu.addAction(self.gsevenx)
        self.gauMenu.addAction(self.gninex)
        self.gauMenu.addAction(self.gelevenx)
        self.gauMenu.addAction(self.gthirteenx)
        self.gauMenu.addAction(self.gfifteenx)
        ####Median Menu#########
        self.mediMenu = self.filterMenu.addMenu('Median Filters')
        self.mediMenu.addAction(self.mthreex)
        self.mediMenu.addAction(self.mfivex)
        self.mediMenu.addAction(self.msevenx)
        self.mediMenu.addAction(self.mninex)
        self.mediMenu.addAction(self.melevenx)
        self.mediMenu.addAction(self.mthirteenx)
        self.mediMenu.addAction(self.mfifteenx)
 ######## GEOMETRİC TRANSFORMS MENU PART ########################################        
        self.geoMenu = self.mainMenu.addMenu('Geometric Transforms')
        ####Rotate Menu#######
        self.rotateMenu = self.geoMenu.addMenu('Rotate')
        self.rotateMenu.addAction(self.rotateRight)
        self.rotateMenu.addAction(self.rotateLeft)
        ####Scale Menu########
        self.scaleMenu = self.geoMenu.addMenu('Scale')
        self.scaleMenu.addAction(self.twice)
        self.scaleMenu.addAction(self.half)
        ####Translate Menu####
        self.translateMenu = self.geoMenu.addMenu('Translate')
        self.translateMenu.addAction(self.right)
        self.translateMenu.addAction(self.left)
    def rotLeft(self):
        
        h,w,dim = self.image.shape
        bytesPerLine = 3 * w
        angle = -1*np.pi/2
        hipo = int(math.sqrt(h*h +w*w))
        row = hipo - h  + 2
        col = hipo - w  + 2
        self.imagepad = np.zeros((h+row,col+w,dim),dtype=int)
        self.pad = np.zeros((h+row,col+w,dim),dtype=int)
        print("imagepad shape",self.imagepad.shape)
        print("image shape",self.image.shape)
        print("row =",row)
        print("col =",col)
        print("h =",h)
        print("w =",w)
        ##self.image = imresize(self.image,[h+row,col+w]),
        self.imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w),:]=self.image
        #self.pad = np.pad(self.image,(int(row/2),int(col/2)),'constant')
        #self.pad[:, padlen
        self.image[0:100,0:100]=[255,255,255]
        self.temp = self.image
        print(self.temp.shape)
        print(self.temp.data)
        print("#########################")
        print(self.imagepad.data)
        #print(self.imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w)])
        ##imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w),:]=255
        ##print("imagepad ve image", imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w)][1] )
        centerx = int(self.imagepad.shape[0]/2)
        centery = int(self.imagepad.shape[1]/2)
        center_of_image = np.asarray([centery,centerx])
        
        imagerot = np.zeros(self.imagepad.shape)
        ##for c in range(0,3):
        j=0
        k=0
        for j in range(0,h):
            xvalue = j - centerx
            for k in range(0,w):
                yvalue = k - centery
                y = int(round((xvalue*np.cos(angle) + yvalue*np.sin(angle))) + centerx)
                x = int(round((-xvalue*np.sin(angle) + yvalue*np.cos(angle))) + centery)
                #.if(x>=1 and y>=1 and x<=imagepad.shape[0] and y<= imagepad.shape[1]):
                    ##print("j ve k",j,k)
                    ##print("x ve y",x,y)
                    #imagepad[x-1,y-1,:] = self.image[j,k,:]
                    ##imagepad[x-1,y-1,:]=255
                    ##print("imagepad ve image",imagepad[x-1,y-1,:],self.image[j,k,:])
                ##rot_mat = np.asarray([[np.cos(angle),np.sin(angle)],[-1*np.sin(angle),np.cos(angle)]])
                ##coord = np.matmul(rot_mat,np.asarray([k-centerx,j-centery]))
                ##coord+= center_of_image
                #if(coord[0]>=1 and coord[1]>=1 and coord[0]<=imagepad.shape[1] and coord[1]<= imagepad.shape[2]):
                 #   imagerot[j,k,:]= imagepad[coord[0],coord[1],:]
                  #  print("Anıll")
                ##self.temp[coord[0].astype(int),coord[1].astype(int),c]=self.image[j,k,c]
        
        ##print("temp data",self.temp[coord[0].astype(int)][coord[1].astype(int)].data)
        ##self.temp=self.image
        #self.rotRight = QImage(self.temp.data,self.temp.shape[1],self.temp.shape[0],3*self.temp.shape[1],QImage.Format_RGB888).rgbSwapped()
        self.rotLeft = QImage(self.imagepad.data,self.imagepad.shape[1],self.imagepad.shape[0],3*self.imagepad.shape[1],QImage.Format_RGB888).rgbSwapped()
        ##self.rotRight = QImage(imagerot.data,imagepad.shape[0],imagepad.shape[1],3*imagepad.shape[1],QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.rotLeft))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.inputBox.layout().addWidget(self.imageLabel)
    def rotRight(self):
        
        h,w,dim = self.image.shape
        bytesPerLine = 3 * w
        angle = np.pi/2
        hipo = int(math.sqrt(h*h +w*w))
        row = hipo - h  + 2
        col = hipo - w  + 2
        self.imagepad = np.zeros((h+row,col+w,dim),dtype=int)
        self.pad = np.zeros((h+row,col+w,dim),dtype=int)
        print("imagepad shape",self.imagepad.shape)
        print("image shape",self.image.shape)
        print("row =",row)
        print("col =",col)
        print("h =",h)
        print("w =",w)
        ##self.image = imresize(self.image,[h+row,col+w]),
        self.imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w),:]=self.image
        #self.pad = np.pad(self.image,(int(row/2),int(col/2)),'constant')
        #self.pad[:, padlen
        self.image[0:100,0:100]=[255,255,255]
        self.temp = self.image
        print(self.temp.shape)
        print(self.temp.data)
        print("#########################")
        print(self.imagepad.data)
        #print(self.imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w)])
        ##imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w),:]=255
        ##print("imagepad ve image", imagepad[int(row/2):(int(row/2)+h),int(col/2):(int(col/2)+w)][1] )
        centerx = int(self.imagepad.shape[0]/2)
        centery = int(self.imagepad.shape[1]/2)
        center_of_image = np.asarray([centery,centerx])
        
        imagerot = np.zeros(self.imagepad.shape)
        ##for c in range(0,3):
        j=0
        k=0
        for j in range(0,h):
            xvalue = j - centerx
            for k in range(0,w):
                yvalue = k - centery
                y = int(round((xvalue*np.cos(angle) + yvalue*np.sin(angle))) + centerx)
                x = int(round((-xvalue*np.sin(angle) + yvalue*np.cos(angle))) + centery)
                #.if(x>=1 and y>=1 and x<=imagepad.shape[0] and y<= imagepad.shape[1]):
                    ##print("j ve k",j,k)
                    ##print("x ve y",x,y)
                    #imagepad[x-1,y-1,:] = self.image[j,k,:]
                    ##imagepad[x-1,y-1,:]=255
                    ##print("imagepad ve image",imagepad[x-1,y-1,:],self.image[j,k,:])
                ##rot_mat = np.asarray([[np.cos(angle),np.sin(angle)],[-1*np.sin(angle),np.cos(angle)]])
                ##coord = np.matmul(rot_mat,np.asarray([k-centerx,j-centery]))
                ##coord+= center_of_image
                #if(coord[0]>=1 and coord[1]>=1 and coord[0]<=imagepad.shape[1] and coord[1]<= imagepad.shape[2]):
                 #   imagerot[j,k,:]= imagepad[coord[0],coord[1],:]
                  #  print("Anıll")
                ##self.temp[coord[0].astype(int),coord[1].astype(int),c]=self.image[j,k,c]
        
        ##print("temp data",self.temp[coord[0].astype(int)][coord[1].astype(int)].data)
        ##self.temp=self.image
        #self.rotRight = QImage(self.temp.data,self.temp.shape[1],self.temp.shape[0],3*self.temp.shape[1],QImage.Format_RGB888).rgbSwapped()
        self.rotRight = QImage(self.imagepad.data,self.imagepad.shape[1],self.imagepad.shape[0],3*self.imagepad.shape[1],QImage.Format_RGB888).rgbSwapped()
        ##self.rotRight = QImage(imagerot.data,imagepad.shape[0],imagepad.shape[1],3*imagepad.shape[1],QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.rotRight))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.inputBox.layout().addWidget(self.imageLabel)
    def medianFilters(self,matrix):
        h,w,dim=self.image.shape
 
        filt=matrix
        summaryR = np.zeros((matrix*matrix),dtype=int)
        summaryB = np.zeros((matrix*matrix),dtype=int)
        summaryG = np.zeros((matrix*matrix),dtype=int)
        print(self.image.shape)
        self.filtered =self.image
        x= int(filt/2)
        k=0
        for i in range(0,h):
            for j in range(0,w):
                if(i>=x and j>=x and i<=h-1-x and j<=w-1-x):
                    for a in range(0,filt):
                        for b in range(0,filt):
                            summaryR[k]= self.image[i-x+b][j-x+a][2]
                            summaryG[k]= self.image[i-x+b][j-x+a][1]
                            summaryB[k]= self.image[i-x+b][j-x+a][0]
                            k = k+1
                    summaryR.sort()
                    summaryG.sort()
                    summaryB.sort()
                    self.filtered[i][j][2]= summaryR[len(summaryR)//2]
                    self.filtered[i][j][1]= summaryG[len(summaryG)//2]
                    self.filtered[i][j][0]= summaryB[len(summaryB)//2]
                    summaryR = np.zeros((matrix*matrix),dtype=int)
                    summaryB = np.zeros((matrix*matrix),dtype=int)
                    summaryG = np.zeros((matrix*matrix),dtype=int)
                    k = 0
                else:
                    for a in range(0,filt):
                        for b in range(0,filt):
                            if(i-x+b<0 or i-x+b>h-1 or j-x+a<0 or j-x+a>w-1):
                               summaryR[k] = 0
                               summaryG[k] = 0
                               summaryB[k] = 0
                               k=k+1
                            else:
                                summaryR[k]= self.image[i-x+b][j-x+a][2]
                                summaryG[k]= self.image[i-x+b][j-x+a][1]
                                summaryB[k]= self.image[i-x+b][j-x+a][0]
                                k = k + 1          
                    summaryR.sort()
                    summaryG.sort()
                    summaryB.sort()
                    self.filtered[i][j][2]= summaryR[len(summaryR)//2]
                    self.filtered[i][j][1]= summaryG[len(summaryG)//2]
                    self.filtered[i][j][0]= summaryB[len(summaryB)//2]
                    summaryR = np.zeros((matrix*matrix),dtype=int)
                    summaryB = np.zeros((matrix*matrix),dtype=int)
                    summaryG = np.zeros((matrix*matrix),dtype=int)
                    k=0

        self.temp = QImage(self.filtered.data,self.filtered.shape[1],self.filtered.shape[0],3*self.filtered.shape[1],QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.temp))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.inputBox.layout().addWidget(self.imageLabel)
    def averageFilters(self,matrix):
        h,w,dim=self.image.shape
 
        filt=matrix
        summary = np.zeros(3)
        print(self.image.shape)
        self.filtered =self.image
        x= int(filt/2)
        for i in range(0,h):
            for j in range(0,w):
                if(i>=x and j>=x and i<=h-1-x and j<=w-1-x):
                    for a in range(0,filt):
                        for b in range(0,filt):
                            summary= summary + self.image[i-x+b][j-x+a]
                    self.filtered[i][j]= summary/(filt*filt)
                    summary = np.zeros(3)
                else:
                    for a in range(0,filt):
                        for b in range(0,filt):
                            if(i-x+b<0 or i-x+b>h-1 or j-x+a<0 or j-x+a>w-1):
                                x = x
                            else:
                                summary= summary + self.image[i-x+b][j-x+a]
                                
                    self.filtered[i][j] = summary/(filt*filt)
                    summary = [0,0,0]

        self.temp = QImage(self.filtered.data,self.filtered.shape[1],self.filtered.shape[0],3*self.filtered.shape[1],QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.temp))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.inputBox.layout().addWidget(self.imageLabel)
    def gaussianFilters(self,matrix):
        h,w,dim=self.image.shape
        s = 1
        firstx = 1/(2*math.pi*s)
        sums = 0
        filt=matrix
        summary = np.zeros(3)
        print(self.image.shape)
        self.filtered =self.image
        x= int(filt/2)
        for i in range(0,h):
            for j in range(0,w):
                if(i>=x and j>=x and i<=h-1-x and j<=w-1-x):
                    for a in range(0,filt):
                        for b in range(0,filt):
                            sums = sums + firstx*math.exp(-1*((-x+b)*(-x+b)+(-x+a)*(-x+a))/(2*s))
                            summary= summary + self.image[i-x+b][j-x+a]*(firstx*math.exp(-1*((-x+b)*(-x+b)+(-x+a)*(-x+a))/(2*s)))
                    self.filtered[i][j]= summary/sums
                    summary = np.zeros(3)
                    sums = 0
                else:
                    for a in range(0,filt):
                        for b in range(0,filt):
                            if(i-x+b<0 or i-x+b>h-1 or j-x+a<0 or j-x+a>w-1):
                                x = x
                            else:
                                sums = sums + firstx*math.exp(-1*(((-x+b)*(-x+b)+(-x+a)*(-x+a))/(2*s)))
                                summary= summary + self.image[i-x+b][j-x+a]*(firstx*math.exp((-1)*((-x+b)*(-x+b)+(-x+a)*(-x+a))/(2*s)))
                                
                    self.filtered[i][j] = summary/sums
                    summary = np.zeros(3)
                    sums = 0

        self.temp = QImage(self.filtered.data,self.filtered.shape[1],self.filtered.shape[0],3*self.filtered.shape[1],QImage.Format_RGB888).rgbSwapped()
        self.imageLabel.setPixmap(QPixmap.fromImage(self.temp))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.inputBox.layout().addWidget(self.imageLabel)

    def openI(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open Input', '.')
        if fileName:
            self.image = cv2.imread(fileName)
            heightI,widthI,channelsI = self.image.shape
            bytesPerLine = 3 * widthI
            if not self.image.data:
                QMessageBox.information(self, "Image Viewer",
                        "Cannot load %s." % fileName)
                return
            
        self.qImg = QImage(self.image.data,widthI,heightI,bytesPerLine,QImage.Format_RGB888).rgbSwapped()
        
        self.imageLabel = QLabel('image')
        self.imageLabel.setPixmap(QPixmap.fromImage(self.qImg))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        
        self.inputBox.layout().addWidget(self.imageLabel)
               
    
    def save(self):
        print("yazıyorumm")
        cv2.imwrite('saveImage.png',self.temp)
    
    def exit(self):
        sys.exit()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())