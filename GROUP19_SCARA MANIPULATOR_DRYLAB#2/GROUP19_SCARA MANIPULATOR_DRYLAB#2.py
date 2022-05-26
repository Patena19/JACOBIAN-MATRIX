import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code

sg.theme('Darkpurple4')

# Excel read code

EXCEL_FILE = 'SCARA_RRP.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code
layout = [
    [sg.Push(), sg.Text('SCARA RRP MEXE CALCULATOR', font = ("Bookman Old Style", 15)), sg.Push()],

[sg.Text('FORWARD KINEMATICS CALCULATOR', font = ("Bookman Old Style", 12))],
    
[sg.Text('fill out the following fields:', font = ("Bookman Old Style", 10)),
sg.Push(), sg.Button('Click this before Solving Forward Kinematics', font = ("Bookman Old Style", 15), size=(35,0), button_color=('black', 'purple')), sg.Push()],
    
[sg.Text('a1 = ', font = ("Bookman Old Style", 10)),sg.InputText('50', key='a1', size=(20,10)),
    sg.Text('T1 = ',font = ("Bookman Old Style", 10)),sg.InputText('0',key='T1', size=(20,10)),
    sg.Push(), sg.Button("Jacobian Matrix (J)", font = ("Bookman Old Style", 12), size=(15,0), button_color=('black', 'yellow')),
    sg.Button('Det(J)', font = ("Bookman Old Style", 12), size=(15,0), button_color=('black', 'yellow')),
    sg.Button('Inverse of J', font = ("Bookman Old Style", 12), size=(15,0), button_color=('black', 'yellow')),
    sg.Button('Transpose of J', font = ("Bookman Old Style", 12), size=(15,0), button_color=('black', 'yellow')), sg.Push()],

[sg.Text('a2 = ', font = ("Bookman Old Style", 10)),sg.InputText('60',key='a2', size=(20,10)),
 sg.Text('T2 = ',font = ("Bookman Old Style", 10)),
 sg.InputText('0',key='T2', size=(20,10))],

[sg.Text('a3 = ', font = ("Bookman Old Style", 10)),sg.InputText('50',key='a3', size=(20,10)),
 sg.Text('d3 = ',font = ("Bookman Old Style", 10)),
 sg.InputText('0',key='d3', size=(20,10))],
[sg.Text('a4 = ', font = ("Bookman Old Style", 10)),sg.InputText('60',key='a4', size=(20,10)),
sg.Push(), sg.Push(), sg.Button('Inverse Kinematics', font = ("Bookman Old Style", 12), size=(35,0), button_color=('Black', "Green")), sg.Push()],
[sg.Text('a5 = ', font = ("Bookman Old Style", 10)),sg.InputText('50',key='a5', size=(20,10))],

[sg.Button('Solve Forward Kinematics', tooltip = 'Go firts to "Click this before Solving Forward Kinematics"!', font = ("Bookman Old Style", 12), button_color=('black', 'blue')), sg.Push(),
 sg.Push(),sg.Button('Path and Trajectory planning', font = ("Bookman Old Style", 12), size=(40,0), button_color=('black', 'blue')), sg.Push()],

[sg.Frame('Position Vector: ',[[
        sg.Text('X = ', font = ("Bookman Old Style", 10)),sg.InputText(key='X', size=(10,1)),
        sg.Text('Y = ',font = ("Bookman Old Style", 10)),sg.InputText(key='Y', size=(10,1)),
        sg.Text('Z = ',font = ("Bookman Old Style", 10)),sg.InputText(key='Z', size=(10,1))]]
    )],

[sg.Frame('H0_3 Transformation Matrix = ', [[sg.Output(size=(60,10))]]), sg.Push(),sg.Image('SCARA_RRP.gif'), sg.Push()],
[sg.Submit(font = ("Bookman Old Style", 10)),sg.Exit(font = ("Bookman Old Style", 10))]

]
    

# Windows Code
window = sg.Window('SCARA MANIPULATOR (RRP)', layout, resizable=True)

# Variable Codes for disabling Button
disable_J = window['Jacobian Matrix (J)']
disable_DetJ = window['Det(J)']
disable_IV = window['Inverse of J']
disable_TJ = window['Transpose of J']
disable_IK = window['Inverse Kinematics']
disable_PT = window['Path and Trajectory planning']


while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    
    if event == 'Click this before Solving Forward Kinematics' :
        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=True)
        disable_IV.update(disabled=True)
        disable_TJ.update(disabled=True)
        disable_IK.update(disabled=True)
        disable_PT.update(disabled=True)
        
    
    if event == 'Solve Forward Kinematics':
        
        # Forward Kinematic Codes
      
        # link lengths in cm
        a1 = float(values['a1'])
        a2 = float(values['a2'])
        a3 = float(values['a3'])
        a4 = float(values['a4'])
        a5 = float(values['a5'])

        # Joint Variable (Thetas in degrees & dinstance in cm)
        T1 = float(values['T1'])
        T2 = float(values['T2'])
        d3 = float(values['d3'])

        T1 = (T1)/180.0*np.pi  # Theta 1 in radian
        T2 = (T2)/180.0*np.pi  # Theta 2 in radian

        DHPT = [
            [float(T1),(0.0/180.0)*np.pi, float(a2), float(a1)],
            [float(T2),(180.0/180.0)*np.pi, float(a4), float(a3)],
            [0, 0, 0, float(a5)+float(d3)]]

        # D-H Notation Formula for HTM
        i = 0
        H0_1 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1]]

        i = 1
        H1_2 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1]]

        i = 2
        H2_3 = [
            [np.cos(DHPT[i][0]), -np.sin(DHPT[i][0])*np.cos(DHPT[i][1]), np.sin(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.cos(DHPT[i][0])],
            [np.sin(DHPT[i][0]), np.cos(DHPT[i][0])*np.cos(DHPT[i][1]), -np.cos(DHPT[i][0])*np.sin(DHPT[i][1]), DHPT[i][2]*np.sin(DHPT[i][0])],
            [0, np.sin(DHPT[i][1]), np.cos(DHPT[i][1]), DHPT[i][3]],
            [0, 0, 0, 1]]

        # Transformation Matrices from base to end-effector
        #print("HO_1 = ")
        #print(np.matrix(H0_1))
        #print("H1_2 = ")
        #print(np.matrix(H1_2))
        #print("H2_3 = ")
        #print(np.matrix(H2_3))

        # Dot Product of H0_3 = HO_1*H1_2*H2_3
        H0_1 = np.matrix(H0_1)
        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)

        # Transformation Matrix of the Manipulator
        print("H0_3 = ")
        print(np.matrix(H0_3))

        # Position Vector X Y Z

        X0_3 = H0_3[0,3]
        print("X = ", X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ", Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ", Z0_3)
        
        disable_J.update(disabled=False)
        disable_IK.update(disabled=False)
        disable_PT.update(disabled=False)
        

    if event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data Saved!')
        
    if event == "Jacobian Matrix (J)":
        
        try:
            H0_3 = np.matrix(H0_3)

        except:
            H0_3 = -1
            sg.popup('Warning!')
            sg.popup('Restart the GUI then go first to"Go firts to "Click this before Solving Forward Kinematics"!')
            break

        Z_1 = [[0],[0],[1]] # The [0,0,1] vector
        d0_3 = H0_3[0:3,3:]
        
        # Row 1 - 3, Column 1
        
        R0_0 = [[1,0,0],[0,1,0],[0,0,1]]
        J1a = np.dot(R0_0,Z_1)

        
        J1 = [[(J1a[1,0]*d0_3[2,0])-(J1a[2,0]*d0_3[1,0])],
        [(J1a[2,0]*d0_3[0,0])-(J1a[0,0]*d0_3[2,0])],
        [(J1a[0,0]*d0_3[1,0])-(J1a[1,0]*d0_3[0,0])]]
        
        #print(np.matrix(R0_0))
        #print(np.matrix(J1a))
        #print(np.matrix(J1))

        # Row 1 - 3, Column 2
        R0_1a = np.dot(H0_1,1)
        R0_1 = R0_1a[0:3,0:3]
        d0_1 = R0_1a[0:3,3:]
        J2a = (np.dot(R0_1,Z_1))
        J2b = (np.subtract(d0_3,d0_1))

        J2 = [[(J2a[1,0]*J2b[2,0])-(J2a[2,0]*J2b[1,0])],
        [(J2a[2,0]*J2b[0,0])-(J2a[0,0]*J2b[2,0])],
        [(J2a[0,0]*J2b[1,0])-(J2a[1,0]*J2b[0,0])]]
        print(np.matrix(J2))
        
        

        # Row 1 - 3, Column 3
        R0_2 = H0_2[0:3,0:3]
        J3 = np.dot(R0_2,Z_1)
        #print(np.matrix(J3))

        J3a = [[0],[0],[0]]

        # Concatenate
        JM1 = np.concatenate((J1,J2,J3),1)
        # print(JM1)
        
        JM2 = np.concatenate((J1a,J2a,J3a),1)
        # print(JM2)
        
        J = np.concatenate((JM1,JM2),0)
        sg.popup("J = ", J)
        
        DJ = np.linalg.det(JM1)
        if DJ == 0:
            disable_IV.update(disabled=True)
            sg.popup('Warning: This is Non-Invertible')
            
        elif DJ != 0.00000:
            disable_IV.update(disabled=False)
            
        disable_J.update(disabled=True)
        disable_DetJ.update(disabled=False)
        disable_TJ.update(disabled=False)
        
        
    if event == "Det(J)":
        # Determinant
        
        try:
            JM1 = np.concatenate((J1,J2,J3),1)

        except:
            JM_1 = -1
            sg.popup('Warning!')
            sg.popup('Restart the GUI then go first to"Go firts to "Click this before Solving Forward Kinematics"!')
            break
            
        DJ = np.linalg.det(JM1)
        print("DJ = ")
        print(DJ)
        sg.popup('D(J) =' "%.4f" % DJ), 
        
        if DJ == 0:
            disable_IV.update(disabled=True)
            sg.popup('Warning: This is Non-Invertible')
            
       
        
    if event == 'Inverse of J':
        # Inverse Velocity
        
        try:
            JM1 = np.concatenate((J1,J2,J3),1)

        except:
            JM_1 = -1
            sg.popup('Warning!')
            sg.popup('Restart the GUI then go first to"Go firts to "Click this before Solving Forward Kinematics"!')
            break
        IV = np.linalg.inv(JM1)
        sg.popup('IV =', IV)
        #sg.popup('Warning: This is Non-Invertible')
        
        
    if event == 'Transpose of J' :
        # Transpose of J
        try:
            JM1 = np.concatenate((J1,J2,J3),1)

        except:
            JM_1 = -1
            sg.popup('Warning!')
            sg.popup('Restart the GUI then go first to"Go firts to "Click this before Solving Forward Kinematics"!')
            break
        TJ = np.transpose(JM1)
        print("TJ = ")
        print(TJ)
        sg.popup('T(J)=', TJ)
        
        
    
        
                  
window.close()
