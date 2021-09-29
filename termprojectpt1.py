# mode-demo.py

from tkinter import *
import random
####################################
# init
####################################
# the readFile and readCsvFile are referred from https://www.cs.cmu.edu/~110/notes/notes-2d-lists.html
def readFile(path):
    # This makes a very modest attempt to deal with unicode if present
    with open(path, 'rt', encoding='ascii', errors='surrogateescape') as f:
        return f.read()
def readCsvFile(path):
    # Returns a 2d list with the data in the given csv file
    result = [ ]
    for line in readFile(path).splitlines():
        result.append(line.split(','))
    return result
def getNetIncome(path):
    # Returns a 2d list with the data in the given csv file
    result = [ ]
    for line in readFile(path).splitlines():
        result.append(line.split(','))
    return result[-1][1:] #[-1] because the net income is shown in the last row in the csv file. [1:] is to ignore the header column
    
def getListOfLastestPeriodQuantityOfProductSaleInAllCountries(path):
    result = [ ]
    for line in readFile(path).splitlines():
        result.append(line.split(','))
    listOfLastestPeriodQuantityOfProductSalesInAllCountries = result[-1][1:] #[-1] because the latest period sales are shown in the last line of the csv. [1:] is to ignore the header column
    for i in range(len(listOfLastestPeriodQuantityOfProductSalesInAllCountries)):
        listOfLastestPeriodQuantityOfProductSalesInAllCountries[i] = int(listOfLastestPeriodQuantityOfProductSalesInAllCountries[i])
    return listOfLastestPeriodQuantityOfProductSalesInAllCountries
print(getListOfLastestPeriodQuantityOfProductSaleInAllCountries("/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.historicalSales.csv"))
listOfLastestPeriodQuantityOfProductSalesInAllCountries = getListOfLastestPeriodQuantityOfProductSaleInAllCountries("/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.historicalSales.csv")

def getMaxScaleValue(L):
    maxValueInTheList = max(L)
    return (maxValueInTheList//(10**(len(str(maxValueInTheList))-1))+1)*(10**(len(str(maxValueInTheList))-1))

##Section 1: importing csv files that contains business data
    #contains 6 files from 6 countries
    ##copied from https://www.cs.cmu.edu/~110/notes/notes-2d-  lists.html#csvFiles
    #importing data from u.s. market
MktUS=readCsvFile('/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.market.us.csv')

    #importing data from german market
MktGM=readCsvFile('/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1//world1.report.market.germany.csv')

    #importing data from u.k. market
MktUK=readCsvFile('/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.market.uk.csv')

    #importing data from mexico market
MktMX=readCsvFile('/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.market.mexico.csv')

    #importing data from china market
MktCH=readCsvFile('/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.market.china.csv')

    #importing data from japan market
MktJP=readCsvFile('/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.market.japan.csv')

finance = "/Users/chaiyatatchawaldit/Desktop/15110_term_project/tp2/Part_1/world1.report.finance.csv"


##Section 2: retrieving revelant data from CSV
import copy

def retrieveFactors(A):
    #takes a country's data, return 2D-list of companies' relative price, relative quality, marketing spending share, and market share
    rows,cols,price,quality,marketing,share = len(A),len(A[0]),[],[],[],[]
    for row in range(rows):
        if A[row][0]=='Price Percentage':
            price.extend(A[row])
        if A[row][0]=='Quality':
            quality.extend(A[row])
        if A[row][0]=='Marketing Expense Share':
            marketing.extend(A[row])
        if A[row][0]=='Market Share':
            share.extend(A[row])
    return [price,quality,marketing,share]

def stripeWord(A):
    #takes matrix A, stripe off the name tag for each row
    rows,cols=len(A),len(A[0])
    result=[]
    for row in range(rows):
        L=[]
        for col in range(1,cols):
            L.append(A[row][col])
        result.append(L)
    return result
    
def take3(A):
    #select three out of five country, so that system is always consistent when doing gaussian elimination
    rows,cols,result=len(A),len(A[0]),[]
    for row in range(rows):
        L=[]
        for col in range(3):
            L.append(A[row][col])
        result.append(L)
    return result
    
def convertStringToFloat(A):
    #takes matrix A containing strings, return A containing floats
    rows, cols, result = len(A), len(A[0]),[]
    for row in range(rows):
        L=[]
        for col in range(cols):
            L.append(float(A[row][col]))
        result.append(L)
    return result

def convertShareToRelative(A,numShare):
    #take percent share and number of sharer, return percent relative to average value of all shares
    B = copy.deepcopy(A)
    rows, cols = len(B), len(B[0])
    for row in range(2,rows):
        for col in range(cols):
            B[row][col]=round(B[row][col]*numShare,2)
    return B
    
def transposeMatrix(A):
    #takes in matrix A, returns transpose matrix of A
    rows,cols,result=len(A),len(A[0]),[]
    for col in range(cols):
        L=[]
        for row in range(rows):
            L.append(A[row][col])
        result.append(L)
    return result
    
def systematize(A):
    #combine all the helper functions in this section
    #returns system of equations in matrix form
    #columns represents factors(price,quality,marketing,share)
    #rows represents companies
    retrieved = retrieveFactors(A)
    striped = stripeWord(retrieved)
    floated = convertStringToFloat(striped)
    taken3 = take3(floated)
    relatived = convertShareToRelative(taken3,5)
    return transposeMatrix(relatived)

    #creates systems of equations for each country 
systemJP=systematize(MktJP)
systemMX=systematize(MktMX)
systemCH=systematize(MktCH)
systemUK=systematize(MktUK)
systemGM=systematize(MktGM)
systemUS=systematize(MktUS)

##Section 3: Data analytics
    #finds  price, quality, and marketing coefficients for change in market share using gaussian elimination
    #edited from Optional Lecture week 8
from fractions import Fraction
import copy

    #creates a 2d-list with fraction
def make2dList(rows, cols):
    a=[]
    for row in range(rows): a.append([Fraction(0,1)]*cols)
    return a
    
    #create identity matrix with equal row and col, 1 diagonally
def makeIdentity(n):
    result = make2dList(n, n)
    for rc in range(n):
        result[rc][rc] = Fraction(1,1)
    return result

    
def printMatrix(a):
    #prints a matrix, for debugging uses only
    # For a nicer but more complex version, see    
    #http://goo.gl/eiZ42n
    print('[')
    for row in range(len(a)):
        print(' ', a[row])
    print(']')

def multiply(L, M):
    #multiplies two matrices
    a, b = len(L), len(L[0])
    b, c = len(M), len(M[0])
    result = make2dList(a, c)
    for row in range(a):
        for col in range(c):
            for rc in range(b):
                result[row][col] += L[row][rc] * M[rc][col]
    return result

def multiplyRow(L, row, k):
    # multiply the given row of matrix L by constant k
    rows = len(L) # L is n-by-n
    M = makeIdentity(rows)
    M[row][row] = k
    return multiply(M, L)
 

def addMultipleOfRow(L, rowMultiple, rowAddInto, k):
    # multiply the given row of L by k
    #rowMultiple is multplied by k, then added into rowAddInto
    #returns 
    rows = len(L) # L is n-by-n
    M = makeIdentity(rows)
    M[rowAddInto][rowMultiple] = k
    return multiply(M, L)
    
    #copying of week 8 optional lecture code ends here
    
def switchRows(A,firstRow,secondRow):
    #return matrix A with first and second row switched
    B = copy.deepcopy(A)
    temp =B[firstRow]
    B[firstRow]=B[secondRow]
    B[secondRow]=temp
    return B

def echelonForm(A):
    #takes in matrix A, a system of equation
    #A's dimension must be cols == rows+1
    #return A in echelon form
    B=copy.deepcopy(A)
    rows=len(B)
    cols=len(B[0])
    for col in range(cols-2):
        #moves down diagonally
        if B[col][col]==0:
            #switch rows with row+i
            for row in range(col,rows):
                if B[row][col]!=0:
                    B=switchRows(A,col,row)
                    break
            if B[col][col]==0:
                return "the matrix is inconsistent"
        for row in range(col+1,rows):
            #minus row2 by row1(row2/row1)
            coefficient = int(10000000*B[row][col])/int(10000000*B[col][col])
            B = addMultipleOfRow(B, col,row,-1*coefficient)
    return B

def reducedEchelonForm(A):
    #takes matrix in echelon form
    #return matrix in reduced echelon form
    B=copy.deepcopy(A)
    rows=len(B)
    #rows=3
    cols=len(B[0])
    #cols=4
    for col in range(cols-2,-1,-1):
        #col = 2,1,0
        i=cols-col-2
        #i= 0 then 1 then 2
        factor=10000000/(int(10000000*B[col][col]))
        B=multiplyRow(B, col, factor)
        for row in range(rows-2-i,-1,-1):
            #row=1,0 then 0
            B = addMultipleOfRow(B,col,row, -1*B[row][col])
    return B
    
def roundMatrix(A,digit):
    #round the matrix by 
    B = copy.deepcopy(A)
    rows, cols = len(B), len(B[0])
    for row in range(rows):
        for col in range(cols):
            B[row][col]=round(B[row][col],digit)
    return B
            
def returnFactor(A):
    #takes in reduced echelon matrix    
    #returns list of coefficients for price,quality,marketing
    result=[]
    rows=len(A)
    for row in range(rows):
        result.append(A[row][-1])
    return result

def formulize(A):
    #combine all the previous helper functions in this section
    #returns list, representing formula of each country's 
    #relative customer taste
    echelonized= echelonForm(A)
    reduced= reducedEchelonForm(echelonized)
    rounded = roundMatrix(reduced,4)
    return returnFactor(rounded)
    
    #finds the factor [price,quality,marketing] coefficients for each country
tasteJP=formulize(systemJP)
tasteMX=formulize(systemMX)
tasteCH=formulize(systemCH)
tasteUK=formulize(systemUK)
tasteGM=formulize(systemGM)
tasteUS=formulize(systemUS)

# printMatrix([tasteJP,tasteMX,tasteCH,tasteUK,tasteGM,tasteUS])

 ##Section 4:    
#after user choose a company, they will
#company's previous performance in the market also effect the market share in the future.
#customer don't percieve the quality and marketing value right away, often with a lag time.
#for quality's impact on share, 80% past value, 20% current input
#for marketing's impact on share, 50% past value, 50% current input

def getPastData(company):
    # takes an int company(1-5), 
    #return 2d-list of the company past factors(price, quality, marketing, share) of each countries
    #rows == countries, cols == factors
    result =[]
    countries=[MktJP,MktMX,MktCH,MktUK,MktGM,MktUS]
    for country in countries:
        A = retrieveFactors(country)
        B = stripeWord(A)
        C = convertStringToFloat(B)
        D = convertShareToRelative(C,5)
        rows,L=len(D),[]
        for row in range(rows):
            L.append(D[row][company-1])
        result.append(L)
    return result
   
#prc, qul,mkt == user input
def combinePastPresent(company,prc,qul,mkt):
    #takes in matrix from getPastData
    #Also takes user input for price, quality, marketing
    #returns the combined input 
    past=getPastData(company)
    rows,cols=len(past),len(past[0])
    result=[]
    for row in range(rows):
        L=[]
        L.append(prc)
        L.append(round((past[row][1]*0.8)+(0.2*qul),5))
        L.append(round((past[row][2]*0.5)+(0.5*mkt),5))
        result.append(L)
    return result

##Use this function: 
def marketPercentShare(company,prc,qul,mkt):
    #takes in 2d-list from combinePastPresent, return a list of market share of each country for the specified company.
    inputs = combinePastPresent(company,prc,qul,mkt)
    rows,result =len(inputs),[]
    factor =[tasteJP,tasteMX,tasteCH,tasteUK,tasteGM,tasteUS]
    for row in range(rows):
        price = factor[row][0]*inputs[row][0]
        quality = factor[row][1]*inputs[row][1]
        marketing =factor[row][2]*inputs[row][2]
        share = round((price + quality + marketing)/5,5)
        result.append(share)
    return result
# printMatrix(marketPercentShare(3,1,1,1))
# the init function and mode dispatcher are referred from http://www.kosbie.net/cmu/fall-16/15-112/notes/notes-animations-examples.html#modeDemo
def init(data):
    # There is only one init, not one-per-mode
    data.mode = "splashScreen"
    data.score = 0
    data.rectangleshalfSize = data.width/100
    data.rectangle1X = data.width/2
    data.rectangle1Y = data.height*(3/5+1/9)
    data.rectangle2X = data.width/2
    data.rectangle2Y = data.height*(3/5+1/9+1/11)
    data.rectangle3X = data.width/2
    data.rectangle3Y = data.height*(3/5+1/9+2/11)
    data.xPositionOfDollarSign = 0
    data.yPositionOfDollarSign = 0
    data.xPositionOfYuanSign = 0
    data.yPositionOfYuanSign = 0
    data.sizeOfDollarSign = 0
    data.sizeOfYuanSign = 0
    data.companyTableRectangleY1 = -data.height
    data.companyTableRectangleY2 = -data.height
    data.prc=1
    data.qul=1
    data.mkt=1
    
company = 0
listOfCountryNames = ["Japan", "Mexico", "China", "UK", "Germany", "US"]

####################################
# mode dispatcher
####################################

def mouseMove(event, data):
    if  (data.mode == "playGame"):
        playGameMouseMove(event,data)

def mousePressed(event, data):
    if (data.mode == "splashScreen"): splashScreenMousePressed(event, data)
    elif (data.mode == "playGame"):   playGameMousePressed(event, data)
    elif (data.mode == "company1"):       company1MousePressed(event, data)
    elif (data.mode == "company2"):       company2MousePressed(event, data)
    elif (data.mode == "company3"):       company3MousePressed(event, data)
    elif (data.mode == "company4"):       company4MousePressed(event, data)
    elif (data.mode == "company5"):       company5MousePressed(event, data)

def keyPressed(event, data):
    if (data.mode == "splashScreen"): splashScreenKeyPressed(event, data)
    elif (data.mode == "playGame"):   playGameKeyPressed(event, data)
    elif (data.mode == "company1"):       company1KeyPressed(event, data)
    elif (data.mode == "company2"):       company2KeyPressed(event, data)
    elif (data.mode == "company3"):       company3KeyPressed(event, data)
    elif (data.mode == "company4"):       company4KeyPressed(event, data)
    elif (data.mode == "company5"):       company5KeyPressed(event, data)

def timerFired(data):
    if (data.mode == "splashScreen"): splashScreenTimerFired(data)
    elif (data.mode == "playGame"):   playGameTimerFired(data)
    elif (data.mode == "company1"):       company1TimerFired(data)
    elif (data.mode == "company2"):       company2TimerFired(data)
    elif (data.mode == "company3"):       company3TimerFired(data)
    elif (data.mode == "company4"):       company4TimerFired(data)
    elif (data.mode == "company5"):       company5TimerFired(data)
    
def redrawAll(canvas, data):
    if (data.mode == "splashScreen"): splashScreenRedrawAll(canvas, data)
    elif (data.mode == "playGame"):   playGameRedrawAll(canvas, data)
    elif (data.mode == "company1"):       company1RedrawAll(canvas, data)
    elif (data.mode == "company2"):       company2RedrawAll(canvas, data)
    elif (data.mode == "company3"):       company3RedrawAll(canvas, data)
    elif (data.mode == "company4"):       company4RedrawAll(canvas, data)
    elif (data.mode == "company5"):       company5RedrawAll(canvas, data)
    
####################################
# splashScreen mode
####################################
def splashScreenMousePressed(event, data):
    pass
def splashScreenKeyPressed(event, data):
    if (event.keysym == "Return"):
        data.mode = "playGame"

def splashScreenTimerFired(data):
    data.xPositionOfDollarSign = random.randint(0,1000)
    data.yPositionOfDollarSign = random.randint(0,700)
    data.xPositionOfYuanSign = random.randint(0,1000)
    data.yPositionOfYuanSign = random.randint(0,700)
    data.sizeOfDollarSign = random.randint(30,60)
    data.sizeOfYuanSign = random.randint(20,70)
    
def splashScreenRedrawAll(canvas, data):
    #create the welcome message "Welcome to Business Game Support System!" and instruction for our program.
    canvas.create_rectangle(0,0,data.width, data.height,fill="black")
    canvas.create_text(data.xPositionOfDollarSign, data.yPositionOfDollarSign,font=("Times", data.sizeOfDollarSign, "bold"),fill="green",text="$")
    canvas.create_text(data.xPositionOfYuanSign, data.yPositionOfYuanSign,font=("Times", data.sizeOfYuanSign, "bold"),fill="red",text="¥")
    canvas.create_text(data.width/2, data.height/11,font=("Times", 30, "bold"), fill="white", text="Welcome to Business Game Support System!")
    canvas.create_text(data.width/2, data.height/5,font=("Times", 30), fill="white",text="This system summarizes the current net incomes of your company")
    canvas.create_text(data.width/2, data.height/5+data.height/5-data.height/11,font=("Times", 30),fill="white",text="and your competitors and current marketing expense in different countries.")
    canvas.create_text(data.width/2, data.height*3/7,font=("Times", 30),fill="white", text=" It also helps you predict the market shares of your company")
    canvas.create_text(data.width/2, data.height*3/7+data.height/5-data.height/11,font=("Times", 30),fill="white", text="in different countries as you change your price, quality and marketing.")
    canvas.create_text(data.width/2, data.height*3/7+2*(data.height/5-data.height/11),font=("Times", 30,"bold"),fill="white", text="Press 'ENTER' when you are ready!")
    

####################################
# company1 mode
####################################
company=1

def company1MousePressed(event, data):
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9) - data.width/100<=event.y<=data.height*(3/5+1/9) + data.width/100):
        data.rectangle1X = event.x
        data.prc = (data.rectangle1X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+1/11) - data.width/100<=event.y<=data.height*(3/5+1/9+1/11) + data.width/100):
        data.rectangle2X = event.x
        data.qul = (data.rectangle2X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+2/11) - data.width/100<=event.y<=data.height*(3/5+1/9+2/11) + data.width/100):
        data.rectangle3X = event.x
        data.mkt = (data.rectangle3X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
    
def company1KeyPressed(event, data):
    data.mode = "playGame"

def company1TimerFired(data):
    pass

def company1RedrawAll(canvas, data):
    #the create_text below creates the title
    canvas.create_text(data.width/2, data.height/11,
                           font=("Times", 30, "bold"), text="Business Game Support System")
    canvas.create_text(data.width/2, data.height/7,
                           font=("Times", 20), text="You chose Company 1. Adjust the price/quality/marketing percentage bars below")
    canvas.create_text(data.width/2, data.height/7+(data.height/7-data.height/11),
                           font=("Times", 20), text="to see the predicted marketing shares for your company! Press any key to go back.")                      
    #create title of the graph "Predicted Market Share In Each Country"
    canvas.create_text(data.width/2, data.height/7+2*(data.height/7-data.height/11),
                           font=("Times", 25, "bold"), text="Predicted Market Share In Each Country For Company 1")      
    #create horizontal gridlines for the graph
    numbersOfGridLines = 5
    for row in range(numbersOfGridLines):
        if (row < numbersOfGridLines-1):
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1),fill="light grey")
            
        else:
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1))
            heightOfTheBottomGridLine = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)     
    #create country names below horizontal axis for the graph
    numberOfCountries=len(listOfCountryNames)
    xPositionOfTheFirstCountryName = data.width/6+data.width*(5/6-1/6)/numberOfCountries/2
    distanceBetweenTheCenterOfEachCountryName = data.width*(5/6-1/6)/numberOfCountries
    for i in range(numberOfCountries):
        canvas.create_text(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName, heightOfTheBottomGridLine*31/30, text=listOfCountryNames[i])
    #create three bars
    canvas.create_line(data.width/5, data.height*(3/5+1/9), 
                            data.width*4/5, data.height*(3/5+1/9),fill="green",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+1/11), 
                            data.width*4/5, data.height*(3/5+1/9+1/11),fill="pink",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+2/11), 
                            data.width*4/5, data.height*(3/5+1/9+2/11),fill="yellow",width=10)
    #create labels for three bars, including "price" "quality" "marketing" and the range of 50% to 150%
    canvas.create_text(data.width/11, data.height*(3/5+1/9), font=("Times", 20, "bold"), text="Price")
    canvas.create_text(data.width/6, data.height*(3/5+1/9), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+1/11), font=("Times", 20, "bold"), text="Quality")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+2/11), font=("Times", 20, "bold"), text="Marketing")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="150%")
    #create three rectangular sliders initially at the middle of the bars
    canvas.create_rectangle(data.rectangle1X - data.width/100, 
                       data.rectangle1Y - data.width/100,
                       data.rectangle1X + data.width/100,
                       data.rectangle1Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle2X - data.width/100, 
                       data.rectangle2Y - data.width/100,
                       data.rectangle2X + data.width/100,
                       data.rectangle2Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle3X - data.width/100, 
                       data.rectangle3Y - data.width/100,
                       data.rectangle3X + data.width/100,
                       data.rectangle3Y + data.width/100, fill="white")
    #create vertical axis scales for the graph
    for row in range(numbersOfGridLines):
        canvas.create_text(data.width/8, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), font=("Times", 15), text=str(int(100-row*(100/(numbersOfGridLines-1)))))
        if (row == 0):
            heightOfTheMaxVerticalScale = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)
    #create "%" symbol above vertical axis
    canvas.create_text(data.width/8, heightOfTheMaxVerticalScale*10/11, font=("Times", 15), text="(%)")
    #create bar graphs
    DistanceBetweenTheHighestGridLineAndLowest = heightOfTheBottomGridLine-heightOfTheMaxVerticalScale
    barWidth = distanceBetweenTheCenterOfEachCountryName/2
    for i in range(len(marketPercentShare(company,data.prc,data.qul,data.mkt))):
        heightOfTheBar = heightOfTheBottomGridLine-marketPercentShare(company,data.prc,data.qul,data.mkt)[i]/1*DistanceBetweenTheHighestGridLineAndLowest
        canvas.create_rectangle(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName-(barWidth/2),heightOfTheBar,xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName+(barWidth/2), heightOfTheBottomGridLine,fill="blue")
    #create the current user input above the sliders
    canvas.create_text(data.rectangle1X, data.height*(3/5+1/9-1/23), font=("Times", 20), text=str(round(100*data.prc,2))+"%")
    canvas.create_text(data.rectangle2X, data.height*(3/5+1/9+1/11-1/23), font=("Times", 20), text=str(round(100*data.qul,2))+"%")
    canvas.create_text(data.rectangle3X, data.height*(3/5+1/9+2/11-1/23), font=("Times", 20), text=str(round(100*data.mkt,2))+"%")
    
####################################
# company2 mode
####################################
company=2

def company2MousePressed(event, data):
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9) - data.width/100<=event.y<=data.height*(3/5+1/9) + data.width/100):
        data.rectangle1X = event.x
        data.prc = (data.rectangle1X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+1/11) - data.width/100<=event.y<=data.height*(3/5+1/9+1/11) + data.width/100):
        data.rectangle2X = event.x
        data.qul = (data.rectangle2X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+2/11) - data.width/100<=event.y<=data.height*(3/5+1/9+2/11) + data.width/100):
        data.rectangle3X = event.x
        data.mkt = (data.rectangle3X - data.width/5) / (data.width*(4/5-1/5)) + 0.5

def company2KeyPressed(event, data):
    data.mode = "playGame"

def company2TimerFired(data):
    pass

def company2RedrawAll(canvas, data):
    #the create_text below creates the title
    canvas.create_text(data.width/2, data.height/11,
                           font=("Times", 30, "bold"), text="Business Game Support System")
    canvas.create_text(data.width/2, data.height/7,
                           font=("Times", 20), text="You chose Company 2. Adjust the price/quality/marketing percentage bars below")
    canvas.create_text(data.width/2, data.height/7+(data.height/7-data.height/11),
                           font=("Times", 20), text="to see the predicted marketing shares for your company! Press any key to go back.")                      
    #create title of the graph "Predicted Market Share In Each Country"
    canvas.create_text(data.width/2, data.height/7+2*(data.height/7-data.height/11),
                           font=("Times", 25, "bold"), text="Predicted Market Share In Each Country For Company 2")      
    #create horizontal gridlines for the graph
    numbersOfGridLines = 5
    for row in range(numbersOfGridLines):
        if (row < numbersOfGridLines-1):
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1),fill="light grey")
            
        else:
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1))
            heightOfTheBottomGridLine = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)     
    #create country names below horizontal axis for the graph
    numberOfCountries=len(listOfCountryNames)
    xPositionOfTheFirstCountryName = data.width/6+data.width*(5/6-1/6)/numberOfCountries/2
    distanceBetweenTheCenterOfEachCountryName = data.width*(5/6-1/6)/numberOfCountries
    for i in range(numberOfCountries):
        canvas.create_text(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName, heightOfTheBottomGridLine*31/30, text=listOfCountryNames[i])
    #create three bars
    canvas.create_line(data.width/5, data.height*(3/5+1/9), 
                            data.width*4/5, data.height*(3/5+1/9),fill="green",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+1/11), 
                            data.width*4/5, data.height*(3/5+1/9+1/11),fill="pink",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+2/11), 
                            data.width*4/5, data.height*(3/5+1/9+2/11),fill="yellow",width=10)
    #create labels for three bars, including "price" "quality" "marketing" and the range of 50% to 150%
    canvas.create_text(data.width/11, data.height*(3/5+1/9), font=("Times", 20, "bold"), text="Price")
    canvas.create_text(data.width/6, data.height*(3/5+1/9), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+1/11), font=("Times", 20, "bold"), text="Quality")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+2/11), font=("Times", 20, "bold"), text="Marketing")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="150%")
    #create three rectangular sliders initially at the middle of the bars
    canvas.create_rectangle(data.rectangle1X - data.width/100, 
                       data.rectangle1Y - data.width/100,
                       data.rectangle1X + data.width/100,
                       data.rectangle1Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle2X - data.width/100, 
                       data.rectangle2Y - data.width/100,
                       data.rectangle2X + data.width/100,
                       data.rectangle2Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle3X - data.width/100, 
                       data.rectangle3Y - data.width/100,
                       data.rectangle3X + data.width/100,
                       data.rectangle3Y + data.width/100, fill="white")
    #create vertical axis scales for the graph
    for row in range(numbersOfGridLines):
        canvas.create_text(data.width/8, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), font=("Times", 15), text=str(int(100-row*(100/(numbersOfGridLines-1)))))
        if (row == 0):
            heightOfTheMaxVerticalScale = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)
    #create "%" symbol above vertical axis
    canvas.create_text(data.width/8, heightOfTheMaxVerticalScale*10/11, font=("Times", 15), text="(%)")
    #create bar graphs
    DistanceBetweenTheHighestGridLineAndLowest = heightOfTheBottomGridLine-heightOfTheMaxVerticalScale
    barWidth = distanceBetweenTheCenterOfEachCountryName/2
    for i in range(len(marketPercentShare(company,data.prc,data.qul,data.mkt))):
        heightOfTheBar = heightOfTheBottomGridLine-marketPercentShare(company,data.prc,data.qul,data.mkt)[i]/1*DistanceBetweenTheHighestGridLineAndLowest
        canvas.create_rectangle(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName-(barWidth/2),heightOfTheBar,xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName+(barWidth/2), heightOfTheBottomGridLine,fill="blue")
    #create the current user input above the sliders
    canvas.create_text(data.rectangle1X, data.height*(3/5+1/9-1/23), font=("Times", 20), text=str(round(100*data.prc,2))+"%")
    canvas.create_text(data.rectangle2X, data.height*(3/5+1/9+1/11-1/23), font=("Times", 20), text=str(round(100*data.qul,2))+"%")
    canvas.create_text(data.rectangle3X, data.height*(3/5+1/9+2/11-1/23), font=("Times", 20), text=str(round(100*data.mkt,2))+"%")
####################################
# company3 mode
####################################
company=3

def company3MousePressed(event, data):
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9) - data.width/100<=event.y<=data.height*(3/5+1/9) + data.width/100):
        data.rectangle1X = event.x
        data.prc = (data.rectangle1X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+1/11) - data.width/100<=event.y<=data.height*(3/5+1/9+1/11) + data.width/100):
        data.rectangle2X = event.x
        data.qul = (data.rectangle2X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+2/11) - data.width/100<=event.y<=data.height*(3/5+1/9+2/11) + data.width/100):
        data.rectangle3X = event.x
        data.mkt = (data.rectangle3X - data.width/5) / (data.width*(4/5-1/5)) + 0.5

def company3KeyPressed(event, data):
    data.mode = "playGame"

def company3TimerFired(data):
    pass

def company3RedrawAll(canvas, data):
    #the create_text below creates the title
    canvas.create_text(data.width/2, data.height/11,
                           font=("Times", 30, "bold"), text="Business Game Support System")
    canvas.create_text(data.width/2, data.height/7,
                           font=("Times", 20), text="You chose Company 3. Adjust the price/quality/marketing percentage bars below")
    canvas.create_text(data.width/2, data.height/7+(data.height/7-data.height/11),
                           font=("Times", 20), text="to see the predicted marketing shares for your company! Press any key to go back.")                      
    #create title of the graph "Predicted Market Share In Each Country"
    canvas.create_text(data.width/2, data.height/7+2*(data.height/7-data.height/11),
                           font=("Times", 25, "bold"), text="Predicted Market Share In Each Country For Company 3")      
    #create horizontal gridlines for the graph
    numbersOfGridLines = 5
    for row in range(numbersOfGridLines):
        if (row < numbersOfGridLines-1):
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1),fill="light grey")
            
        else:
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1))
            heightOfTheBottomGridLine = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)     
    #create country names below horizontal axis for the graph
    numberOfCountries=len(listOfCountryNames)
    xPositionOfTheFirstCountryName = data.width/6+data.width*(5/6-1/6)/numberOfCountries/2
    distanceBetweenTheCenterOfEachCountryName = data.width*(5/6-1/6)/numberOfCountries
    for i in range(numberOfCountries):
        canvas.create_text(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName, heightOfTheBottomGridLine*31/30, text=listOfCountryNames[i])
    #create three bars
    canvas.create_line(data.width/5, data.height*(3/5+1/9), 
                            data.width*4/5, data.height*(3/5+1/9),fill="green",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+1/11), 
                            data.width*4/5, data.height*(3/5+1/9+1/11),fill="pink",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+2/11), 
                            data.width*4/5, data.height*(3/5+1/9+2/11),fill="yellow",width=10)
    #create labels for three bars, including "price" "quality" "marketing" and the range of 50% to 150%
    canvas.create_text(data.width/11, data.height*(3/5+1/9), font=("Times", 20, "bold"), text="Price")
    canvas.create_text(data.width/6, data.height*(3/5+1/9), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+1/11), font=("Times", 20, "bold"), text="Quality")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+2/11), font=("Times", 20, "bold"), text="Marketing")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="150%")
    #create three rectangular sliders initially at the middle of the bars
    canvas.create_rectangle(data.rectangle1X - data.width/100, 
                       data.rectangle1Y - data.width/100,
                       data.rectangle1X + data.width/100,
                       data.rectangle1Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle2X - data.width/100, 
                       data.rectangle2Y - data.width/100,
                       data.rectangle2X + data.width/100,
                       data.rectangle2Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle3X - data.width/100, 
                       data.rectangle3Y - data.width/100,
                       data.rectangle3X + data.width/100,
                       data.rectangle3Y + data.width/100, fill="white")
    #create vertical axis scales for the graph
    for row in range(numbersOfGridLines):
        canvas.create_text(data.width/8, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), font=("Times", 15), text=str(int(100-row*(100/(numbersOfGridLines-1)))))
        if (row == 0):
            heightOfTheMaxVerticalScale = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)
    #create "%" symbol above vertical axis
    canvas.create_text(data.width/8, heightOfTheMaxVerticalScale*10/11, font=("Times", 15), text="(%)")
    #create bar graphs
    DistanceBetweenTheHighestGridLineAndLowest = heightOfTheBottomGridLine-heightOfTheMaxVerticalScale
    barWidth = distanceBetweenTheCenterOfEachCountryName/2
    for i in range(len(marketPercentShare(company,data.prc,data.qul,data.mkt))):
        heightOfTheBar = heightOfTheBottomGridLine-marketPercentShare(company,data.prc,data.qul,data.mkt)[i]/1*DistanceBetweenTheHighestGridLineAndLowest
        canvas.create_rectangle(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName-(barWidth/2),heightOfTheBar,xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName+(barWidth/2), heightOfTheBottomGridLine,fill="blue")
    #create the current user input above the sliders
    canvas.create_text(data.rectangle1X, data.height*(3/5+1/9-1/23), font=("Times", 20), text=str(round(100*data.prc,2))+"%")
    canvas.create_text(data.rectangle2X, data.height*(3/5+1/9+1/11-1/23), font=("Times", 20), text=str(round(100*data.qul,2))+"%")
    canvas.create_text(data.rectangle3X, data.height*(3/5+1/9+2/11-1/23), font=("Times", 20), text=str(round(100*data.mkt,2))+"%")
    
####################################
# company4 mode
####################################
company=4

def company4MousePressed(event, data):
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9) - data.width/100<=event.y<=data.height*(3/5+1/9) + data.width/100):
        data.rectangle1X = event.x
        data.prc = (data.rectangle1X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+1/11) - data.width/100<=event.y<=data.height*(3/5+1/9+1/11) + data.width/100):
        data.rectangle2X = event.x
        data.qul = (data.rectangle2X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+2/11) - data.width/100<=event.y<=data.height*(3/5+1/9+2/11) + data.width/100):
        data.rectangle3X = event.x
        data.mkt = (data.rectangle3X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
def company4KeyPressed(event, data):
    data.mode = "playGame"

def company4TimerFired(data):
    pass

def company4RedrawAll(canvas, data):
    #the create_text below creates the title
    canvas.create_text(data.width/2, data.height/11,
                           font=("Times", 30, "bold"), text="Business Game Support System")
    canvas.create_text(data.width/2, data.height/7,
                           font=("Times", 20), text="You chose Company 4. Adjust the price/quality/marketing percentage bars below")
    canvas.create_text(data.width/2, data.height/7+(data.height/7-data.height/11),
                           font=("Times", 20), text="to see the predicted marketing shares for your company! Press any key to go back.")                      
    #create title of the graph "Predicted Market Share In Each Country"
    canvas.create_text(data.width/2, data.height/7+2*(data.height/7-data.height/11),
                           font=("Times", 25, "bold"), text="Predicted Market Share In Each Country For Company 4")      
    #create horizontal gridlines for the graph
    numbersOfGridLines = 5
    for row in range(numbersOfGridLines):
        if (row < numbersOfGridLines-1):
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1),fill="light grey")
            
        else:
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1))
            heightOfTheBottomGridLine = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)     
    #create country names below horizontal axis for the graph
    numberOfCountries=len(listOfCountryNames)
    xPositionOfTheFirstCountryName = data.width/6+data.width*(5/6-1/6)/numberOfCountries/2
    distanceBetweenTheCenterOfEachCountryName = data.width*(5/6-1/6)/numberOfCountries
    for i in range(numberOfCountries):
        canvas.create_text(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName, heightOfTheBottomGridLine*31/30, text=listOfCountryNames[i])
    #create three bars
    canvas.create_line(data.width/5, data.height*(3/5+1/9), 
                            data.width*4/5, data.height*(3/5+1/9),fill="green",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+1/11), 
                            data.width*4/5, data.height*(3/5+1/9+1/11),fill="pink",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+2/11), 
                            data.width*4/5, data.height*(3/5+1/9+2/11),fill="yellow",width=10)
    #create labels for three bars, including "price" "quality" "marketing" and the range of 50% to 150%
    canvas.create_text(data.width/11, data.height*(3/5+1/9), font=("Times", 20, "bold"), text="Price")
    canvas.create_text(data.width/6, data.height*(3/5+1/9), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+1/11), font=("Times", 20, "bold"), text="Quality")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+2/11), font=("Times", 20, "bold"), text="Marketing")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="150%")
    #create three rectangular sliders initially at the middle of the bars
    canvas.create_rectangle(data.rectangle1X - data.width/100, 
                       data.rectangle1Y - data.width/100,
                       data.rectangle1X + data.width/100,
                       data.rectangle1Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle2X - data.width/100, 
                       data.rectangle2Y - data.width/100,
                       data.rectangle2X + data.width/100,
                       data.rectangle2Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle3X - data.width/100, 
                       data.rectangle3Y - data.width/100,
                       data.rectangle3X + data.width/100,
                       data.rectangle3Y + data.width/100, fill="white")
    #create vertical axis scales for the graph
    for row in range(numbersOfGridLines):
        canvas.create_text(data.width/8, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), font=("Times", 15), text=str(int(100-row*(100/(numbersOfGridLines-1)))))
        if (row == 0):
            heightOfTheMaxVerticalScale = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)
    #create "%" symbol above vertical axis
    canvas.create_text(data.width/8, heightOfTheMaxVerticalScale*10/11, font=("Times", 15), text="(%)")
    #create bar graphs
    DistanceBetweenTheHighestGridLineAndLowest = heightOfTheBottomGridLine-heightOfTheMaxVerticalScale
    barWidth = distanceBetweenTheCenterOfEachCountryName/2
    for i in range(len(marketPercentShare(company,data.prc,data.qul,data.mkt))):
        heightOfTheBar = heightOfTheBottomGridLine-marketPercentShare(company,data.prc,data.qul,data.mkt)[i]/1*DistanceBetweenTheHighestGridLineAndLowest
        canvas.create_rectangle(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName-(barWidth/2),heightOfTheBar,xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName+(barWidth/2), heightOfTheBottomGridLine,fill="blue")
    #create the current user input above the sliders
    canvas.create_text(data.rectangle1X, data.height*(3/5+1/9-1/23), font=("Times", 20), text=str(round(100*data.prc,2))+"%")
    canvas.create_text(data.rectangle2X, data.height*(3/5+1/9+1/11-1/23), font=("Times", 20), text=str(round(100*data.qul,2))+"%")
    canvas.create_text(data.rectangle3X, data.height*(3/5+1/9+2/11-1/23), font=("Times", 20), text=str(round(100*data.mkt,2))+"%")
        
####################################
# company5 mode
####################################
company=5

def company5MousePressed(event, data):
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9) - data.width/100<=event.y<=data.height*(3/5+1/9) + data.width/100):
        data.rectangle1X = event.x
        data.prc = (data.rectangle1X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+1/11) - data.width/100<=event.y<=data.height*(3/5+1/9+1/11) + data.width/100):
        data.rectangle2X = event.x
        data.qul = (data.rectangle2X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
        
    if (data.width/5<=event.x<=data.width*4/5 and data.height*(3/5+1/9+2/11) - data.width/100<=event.y<=data.height*(3/5+1/9+2/11) + data.width/100):
        data.rectangle3X = event.x
        data.mkt = (data.rectangle3X - data.width/5) / (data.width*(4/5-1/5)) + 0.5
def company5KeyPressed(event, data):
    data.mode = "playGame"

def company5TimerFired(data):
    pass

def company5RedrawAll(canvas, data):
    #the create_text below creates the title
    canvas.create_text(data.width/2, data.height/11,
                           font=("Times", 30, "bold"), text="Business Game Support System")
    canvas.create_text(data.width/2, data.height/7,
                           font=("Times", 20), text="You chose Company 5. Adjust the price/quality/marketing percentage bars below")
    canvas.create_text(data.width/2, data.height/7+(data.height/7-data.height/11),
                           font=("Times", 20), text="to see the predicted marketing shares for your company! Press any key to go back.")                      
    #create title of the graph "Predicted Market Share In Each Country"
    canvas.create_text(data.width/2, data.height/7+2*(data.height/7-data.height/11),
                           font=("Times", 25, "bold"), text="Predicted Market Share In Each Country For Company 5")      
    #create horizontal gridlines for the graph
    numbersOfGridLines = 5
    for row in range(numbersOfGridLines):
        if (row < numbersOfGridLines-1):
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1),fill="light grey")
            
        else:
            canvas.create_line(data.width/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1))
            heightOfTheBottomGridLine = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)     
    #create country names below horizontal axis for the graph
    numberOfCountries=len(listOfCountryNames)
    xPositionOfTheFirstCountryName = data.width/6+data.width*(5/6-1/6)/numberOfCountries/2
    distanceBetweenTheCenterOfEachCountryName = data.width*(5/6-1/6)/numberOfCountries
    for i in range(numberOfCountries):
        canvas.create_text(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName, heightOfTheBottomGridLine*31/30, text=listOfCountryNames[i])
    #create three bars
    canvas.create_line(data.width/5, data.height*(3/5+1/9), 
                            data.width*4/5, data.height*(3/5+1/9),fill="green",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+1/11), 
                            data.width*4/5, data.height*(3/5+1/9+1/11),fill="pink",width=10)
    canvas.create_line(data.width/5, data.height*(3/5+1/9+2/11), 
                            data.width*4/5, data.height*(3/5+1/9+2/11),fill="yellow",width=10)
    #create labels for three bars, including "price" "quality" "marketing" and the range of 50% to 150%
    canvas.create_text(data.width/11, data.height*(3/5+1/9), font=("Times", 20, "bold"), text="Price")
    canvas.create_text(data.width/6, data.height*(3/5+1/9), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+1/11), font=("Times", 20, "bold"), text="Quality")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+1/11), font=("Times", 20), text="150%")
    canvas.create_text(data.width/11, data.height*(3/5+1/9+2/11), font=("Times", 20, "bold"), text="Marketing")
    canvas.create_text(data.width/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="50%")
    canvas.create_text(data.width*5/6, data.height*(3/5+1/9+2/11), font=("Times", 20), text="150%")
    #create three rectangular sliders initially at the middle of the bars
    canvas.create_rectangle(data.rectangle1X - data.width/100, 
                       data.rectangle1Y - data.width/100,
                       data.rectangle1X + data.width/100,
                       data.rectangle1Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle2X - data.width/100, 
                       data.rectangle2Y - data.width/100,
                       data.rectangle2X + data.width/100,
                       data.rectangle2Y + data.width/100, fill="white")
    canvas.create_rectangle(data.rectangle3X - data.width/100, 
                       data.rectangle3Y - data.width/100,
                       data.rectangle3X + data.width/100,
                       data.rectangle3Y + data.width/100, fill="white")
    #create vertical axis scales for the graph
    for row in range(numbersOfGridLines):
        canvas.create_text(data.width/8, data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1), font=("Times", 15), text=str(int(100-row*(100/(numbersOfGridLines-1)))))
        if (row == 0):
            heightOfTheMaxVerticalScale = data.height/4+(data.height*3/5- data.height/5)/(numbersOfGridLines+1)*(row+1)
    #create "%" symbol above vertical axis
    canvas.create_text(data.width/8, heightOfTheMaxVerticalScale*10/11, font=("Times", 15), text="(%)")
    #create bar graphs
    DistanceBetweenTheHighestGridLineAndLowest = heightOfTheBottomGridLine-heightOfTheMaxVerticalScale
    barWidth = distanceBetweenTheCenterOfEachCountryName/2
    for i in range(len(marketPercentShare(company,data.prc,data.qul,data.mkt))):
        heightOfTheBar = heightOfTheBottomGridLine-marketPercentShare(company,data.prc,data.qul,data.mkt)[i]/1*DistanceBetweenTheHighestGridLineAndLowest
        canvas.create_rectangle(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName-(barWidth/2),heightOfTheBar,xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName+(barWidth/2), heightOfTheBottomGridLine,fill="blue")
    #create the current user input above the sliders
    canvas.create_text(data.rectangle1X, data.height*(3/5+1/9-1/23), font=("Times", 20), text=str(round(100*data.prc,2))+"%")
    canvas.create_text(data.rectangle2X, data.height*(3/5+1/9+1/11-1/23), font=("Times", 20), text=str(round(100*data.qul,2))+"%")
    canvas.create_text(data.rectangle3X, data.height*(3/5+1/9+2/11-1/23), font=("Times", 20), text=str(round(100*data.mkt,2))+"%")

####################################
# playGame mode
####################################
numberOfCompanies = 5
def playGameMouseMove(event, data):
    print(data.x,data.y)
    rows=5
    yPositionOfTheGridLineAboveCompany1 = (data.height*3/7-data.height/6)/(numberOfCompanies+1)+data.height/6
    if (data.width/6<x<data.width/2 and yPositionOfTheGridLineAboveCompany1<y<data.height*3/7): 
        company = int((y-yPositionOfTheGridLineAboveCompany1)//((data.height*3/7-yPositionOfTheGridLineAboveCompany1)/numberOfCompanies)+1)
        print(company)
        if (company == 1):
            data.companyTableRectangleY1 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(0+1)
            data.companyTableRectangleY2 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(1+1)
        if (company == 2):
            data.companyTableRectangleY1 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(1+1)
            data.companyTableRectangleY2 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(2+1)
        if (company == 3):
            data.companyTableRectangleY1 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(2+1)
            data.companyTableRectangleY2 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(3+1)
        if (company == 4):
            data.companyTableRectangleY1 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(3+1)
            data.companyTableRectangleY2 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(4+1)
        if (company == 5):
            data.companyTableRectangleY1 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(4+1)
            data.companyTableRectangleY2 = data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(5+1)
def playGameMousePressed(event, data):
    rows=5
    yPositionOfTheGridLineAboveCompany1 = (data.height*3/7-data.height/6)/(numberOfCompanies+1)+data.height/6
    if (data.width/6<event.x<data.width/2 and yPositionOfTheGridLineAboveCompany1<event.y<data.height*3/7): 
        company = int((event.y-yPositionOfTheGridLineAboveCompany1)//((data.height*3/7-yPositionOfTheGridLineAboveCompany1)/numberOfCompanies)+1)
        if (company == 1):
            data.mode = "company1"
            
        if (company == 2):
            data.mode = "company2"
            
        if (company == 3):
            data.mode = "company3"
            
        if (company == 4):
            data.mode = "company4"
            
        if (company == 5):
            data.mode = "company5"
                
        
def playGameMouseReleased(event, data):
    pass
    
def playGameKeyPressed(event, data):
    pass

def playGameTimerFired(data):
    pass

def playGameRedrawAll(canvas, data):
    canvas.create_rectangle(data.width/6, data.height/6, 
                            data.width*5/6, data.height*3/7)
    canvas.create_line(data.width/2, data.height/6, 
                            data.width/2, data.height*3/7)
    #For loop below makes rows for the table (number of rows depends on the number of companies)
    rows=5
    for row in range(rows):
        canvas.create_line(data.width/6, data.height/6+(data.height*3/7- data.height/6)/(rows+1)*(row+1), 
                            data.width*5/6, data.height/6+(data.height*3/7-data.height/6)/(rows+1)*(row+1))
    #the create_text below creates the title
    canvas.create_text(data.width/2, data.height/11,
                           font=("Times", 30, "bold"), text="Business Game Support System")
    #create the headers "Company" and "Net Income ($)"
    canvas.create_text(data.width/6+(data.width/2-data.width/6)/2, data.height/6+1/2*(data.height*3/7- data.height/6)/(rows+1),
                           font=("Times", 20), text="Company")
    canvas.create_text(data.width/2+(data.width/2-data.width/6)/2, data.height/6+1/2*(data.height*3/7- data.height/6)/(rows+1),
                           font=("Times", 20), text="Net Income ($)")
        #the for loop below lists compant 1-5
    for row in range(rows):
        canvas.create_text(data.width/6+(data.width/2-data.width/6)/2, data.height/6+((data.height*3/7- data.height/6)/(rows+1)*(row+1))+1/2*(data.height*3/7- data.height/6)/(rows+1),
                           font=("Times", 20), text="Company " + str(row+1))
        canvas.create_text(data.width/2+(data.width/2-data.width/6)/2, data.height/6+((data.height*3/7- data.height/6)/(rows+1)*(row+1))+1/2*(data.height*3/7- data.height/6)/(rows+1),
                           font=("Times", 20), text=str(getNetIncome(finance)[row]))
    #create title of the graph "Total Sales In Each Country Last Period"
    canvas.create_text(data.width/2, data.height/2,
                           font=("Times", 20), text="Total Sales In Each Country Last Period")
    #create horizontal gridlines for the graph
    numbersOfGridLines = 5
    for row in range(numbersOfGridLines):
        if (row < numbersOfGridLines-1):
            canvas.create_line(data.width/6, data.height*3.8/7+(data.height- data.height*3.8/7)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height*3.8/7+(data.height- data.height*3.8/7)/(numbersOfGridLines+1)*(row+1),fill="light grey")
            
        else:
            canvas.create_line(data.width/6, data.height*3.8/7+(data.height- data.height*3.8/7)/(numbersOfGridLines+1)*(row+1), 
                            data.width*5/6, data.height*3.8/7+(data.height- data.height*3.8/7)/(numbersOfGridLines+1)*(row+1))
            heightOfTheBottomGridLine = data.height*3.8/7+(data.height- data.height*3.8/7)/(numbersOfGridLines+1)*(row+1)
    #create vertical axis scales for the graph
    for row in range(numbersOfGridLines):
        canvas.create_text(data.width/8, data.height*3.8/7+(data.height- data.height*3.8/7)/(numbersOfGridLines+1)*(row+1), font=("Times", 15), text=str(int(getMaxScaleValue(listOfLastestPeriodQuantityOfProductSalesInAllCountries)-row*(getMaxScaleValue(listOfLastestPeriodQuantityOfProductSalesInAllCountries)/(numbersOfGridLines-1)))))
        if (row == 0):
            heightOfTheMaxVerticalScale = data.height*3.8/7+(data.height- data.height*3.8/7)/(numbersOfGridLines+1)*(row+1)
    #create the "(units)" symbol above vertical axis
    canvas.create_text(data.width/8, heightOfTheMaxVerticalScale*10/11, font=("Times", 15), text="(units)")
    #create country names below horizontal axis for the graph
    numberOfCountries=len(listOfCountryNames)
    xPositionOfTheFirstCountryName = data.width/6+data.width*(5/6-1/6)/numberOfCountries/2
    distanceBetweenTheCenterOfEachCountryName = data.width*(5/6-1/6)/numberOfCountries
    for i in range(numberOfCountries):
        canvas.create_text(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName, heightOfTheBottomGridLine*31/30, text=listOfCountryNames[i])
    #create bar graphs
    DistanceBetweenTheHighestGridLineAndLowest = heightOfTheBottomGridLine-heightOfTheMaxVerticalScale
    barWidth = distanceBetweenTheCenterOfEachCountryName/2
    for i in range(len(listOfLastestPeriodQuantityOfProductSalesInAllCountries)):
        heightOfTheBar = heightOfTheBottomGridLine-listOfLastestPeriodQuantityOfProductSalesInAllCountries[i]/getMaxScaleValue(listOfLastestPeriodQuantityOfProductSalesInAllCountries)*DistanceBetweenTheHighestGridLineAndLowest
        canvas.create_rectangle(xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName-(barWidth/2),heightOfTheBar,xPositionOfTheFirstCountryName+i*distanceBetweenTheCenterOfEachCountryName+(barWidth/2), heightOfTheBottomGridLine,fill="blue")
        
    #create the rectangle that creates the button effect when moving the mouse on the company
    canvas.create_rectangle(data.width/6, data.companyTableRectangleY1, data.width/2, data.companyTableRectangleY2, fill = "purple")

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1200, 700)