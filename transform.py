
import numpy as np
import matplotlib.pyplot as plt
# NO other imports are allowed

class Shape:
    '''
    DO NOT MODIFY THIS CLASS

    DO NOT ADD ANY NEW METHODS TO THIS CLASS
    '''
    def __init__(self):
        self.T_s = None
        self.T_r = None
        self.T_t = None
    
    
    def translate(self, dx, dy):
        '''
        Polygon and Circle class should use this function to calculate the translation
        '''
        self.T_t = np.array([[1, 0, dx], [0, 1, dy], [0, 0, 1]])
 

    def scale(self, sx, sy):
        '''
        Polygon and Circle class should use this function to calculate the scaling
        '''
        self.T_s = np.array([[sx, 0, 0], [0, sy, 0], [0, 0, 1]])
 
        
    def rotate(self, deg):
        '''
        Polygon and Circle class should use this function to calculate the rotation
        '''
        rad = deg*(np.pi/180)
        self.T_r = np.array([[np.cos(rad), np.sin(rad), 0],[-np.sin(rad), np.cos(rad),0], [0, 0, 1]])

        
    def plot(self, x_dim, y_dim):
        '''
        Polygon and Circle class should use this function while plotting
        x_dim and y_dim should be such that both the figures are visible inside the plot
        '''
        x_dim, y_dim = 1.2*x_dim, 1.2*y_dim
        plt.plot((-x_dim, x_dim),[0,0],'k-')
        plt.plot([0,0],(-y_dim, y_dim),'k-')
        plt.xlim(-x_dim,x_dim)
        plt.ylim(-y_dim,y_dim)
        plt.grid()
        plt.show()



class Polygon(Shape):
  
  
    
  def __init__(self, A):
    super().__init__()
    self.A=A                       
    self.prev_A=self.A              #stores the previous value of A
    
        
  
    
  def translate(self, dx, dy):
    super().translate(dx,dy)        #calls the translate method of parent class
    self.prev_A=self.A
    B=[]
    
    for i in range(len(self.A)):
      k=[]
      for j in range(3):
        m=self.T_t[j][0]*self.A[i][0] + self.T_t[j][1]*self.A[i][1] + self.T_t[j][2]*self.A[i][2]
        k.append(m)
      B.append(k)
    B=np.array(B)                   #B is an array with the updated values after translation
    self.A=B
    B=np.array(B).transpose()
    B=np.delete(B,len(B)-1,0)
    B=np.round(B,decimals=2)         #rounds upto 2 decimal places
    return B   
        

    
  def scale(self, sx, sy):
    super().scale(sx,sy)
    self.prev_A=self.A
    #Finding the co-ordinates of the centre
    m1=0
    m2=0
    n1=len(self.A)
    for i in range(n1):
      m1+=self.A[i,0]
      m2+=self.A[i,1]
    #co-ordinates of the centre
    m1=m1/n1                  
    m2=m2/n1
    k=[]
    k.append(m1)
    k.append(m2)
    k.append(1)
    
    B=[]
    for i in range(n1):
      m4=[]
      m4.extend(self.A[i])
      for i in range(3):
        m4[i]=m4[i] - k[i]
      
      
      m3=np.dot(self.T_s,m4)
      
      
      for i in range(3):
        m3[i]=m3[i] + k[i]
      B.append(m3)
    B=np.array(B)
    self.A=B
    B=np.array(B).transpose()       #Taking the transpose
    B=np.delete(B,len(B)-1,0)       #deleting the last row of 1's
    B=np.round(B,decimals=2)        #rounds upto 2 decimal places
    return B

      

        
 
    
  def rotate(self, deg, rx = 0, ry = 0):
    super().rotate(-deg)
    self.prev_A=self.A
    if rx==0 and ry==0:                       
      m2=np.dot(self.A,self.T_r)                 #matrix multiplication to get the matrix with new co-ordinates
      self.A=m2
      m2=np.array(m2).transpose()                #Taking the transpose 
      m2=np.delete(m2,len(m2)-1,0)               #deleting the last row of 1's
      m2=np.round(m2,decimals=2)                 #rounds upto 2 decimal places
      return m2

    else:
      m1=np.array([[1,0,0],[0,1,0],[-rx,-ry,1]])      
      m2=np.array([[1,0,0],[0,1,0],[rx,ry,1]])
      m3=np.dot(self.A,m1)                          #first Translation 
      m3=np.dot(m3,self.T_r)                        #Rotation
      m3=np.dot(m3,m2)                              #Reversing the effect of Translation
      self.A=m3
      m3=np.array(m3).transpose()
      m3=np.delete(m3,len(m3)-1,0)
      m3=np.round(m3,decimals=2)
      return m3

        
    

  def plot(self):
    m1_x=[]
    m1_y=[]
    m2_x=[]
    m2_y=[]
    m3=[]
    m4=[]
    for j in range(len(self.prev_A)):
      m3.append((self.prev_A[j,0],self.prev_A[j,1]))
      m4.append((self.A[j,0],self.A[j,1]))
      m1_x.append(abs(self.prev_A[j,0]))
      m1_y.append(abs(self.prev_A[j,1]))
      m2_x.append(abs(self.A[j,0]))
      m2_y.append(abs(self.A[j,1]))
    
    limit_x=max(max(m1_x), max(m2_x))             #Finding the max x-coordinate 
    limit_y=max(max(m1_y), max(m2_y))             #Finding the max y-coordinate

    fig,ax=plt.subplots()
    poly_first=plt.Polygon(m3,linestyle='--',fill=False, linewidth=1)
    ax.add_patch(poly_first)
    poly_second=plt.Polygon(m4 ,fill=False, linewidth=1)
    ax.add_patch(poly_second)
    ax.set_aspect(1)
    Shape.plot(self,limit_x,limit_y)              #calling the parent class method to plot the shapes
       


class Circle(Shape):


  def __init__(self, x=0, y=0, radius=5):
    super().__init__()
    self.x=x
    self.y=y
    self.radius=radius                    
    self.prev_x=self.x                          #stores the previous value of x
    self.prev_y=self.y                          #stores the previous value of y
    self.prev_radius=self.radius                #stores the previous value of radius

    
  def translate(self, dx, dy):
    super().translate(dx,dy)
    self.prev_x=self.x                          #Assigns the values of previous transformation to x,y and radius
    self.prev_y=self.y
    self.prev_radius=self.radius
    m1=[]
    m1.append(self.x)
    m1.append(self.y)
    m1.append(1)
    m1=np.array(m1)
    m1=np.dot(self.T_t,m1)
    self.x,self.y=m1[0],m1[1]
    m1=np.round(m1,decimals=2)
    rounded_radius=round(self.radius,2)
    tuple1=(m1[0],m1[1],rounded_radius)
    return tuple1
        
  def scale(self, sx):
    self.prev_x=self.x
    self.prev_y=self.y
    self.prev_radius=self.radius
    self.radius*=sx                           #Scales the radius to get the new radius
    rounded_radius=round(self.radius,2)
    rounded_x=round(self.x,2)
    rounded_y=round(self.y,2)
    tuple1=(rounded_x,rounded_y,rounded_radius)
    return tuple1
        
    
  def rotate(self, deg, rx = 0, ry = 0):
    super().rotate(deg)
    self.prev_x=self.x
    self.prev_y=self.y
    self.prev_radius=self.radius
    self.x = self.x - rx                      #translation
    self.y = self.y - ry
    m1 = np.dot(self.T_r,[self.x,self.y,1])   #rotation
    m1[0]+=rx                                 #reversing the translation
    m1[1]+=ry
    self.x,self.y=m1[0],m1[1]
    m1=np.round(m1,decimals=2)
    rounded_radius=round(self.radius,2)
    tuple1=(m1[0],m1[1],rounded_radius)
    return tuple1
    
        
        
 
    
  def plot(self):
    m1=plt.Circle((self.prev_x,self.prev_y),self.prev_radius,fill=False,linestyle='--')
    fig=plt.figure()
    ax=fig.add_subplot(1,1,1)
    ax.add_patch(m1)
    m2=plt.Circle((self.x,self.y),self.radius,fill=False)
    ax.add_patch(m2)
    ax.set_aspect(1)
    x_limit=max(self.radius + abs(self.x), self.prev_radius + abs(self.prev_x))            #Finds the X-limit
    y_limit=max(self.radius + abs(self.y), self.prev_radius + abs(self.prev_y))            #Finds the Y-limit
    Shape.plot(self,x_limit,y_limit)

        
        

if __name__ == "__main__":
  
  
  x=int(input('Enter 1 if u want to see the plots after every transformation or press 0: '))
  F=int(input('\nEnter the number of test cases: '))
  f=0
  while f<F:

    if x==1:
      
      y=int(input('\nEnter 1 for circle or 0 for polygon: '))
      if y == 1 :
        z=list(map(float,input('\nEnter the co-ordinates of centre and the radius of circle(space separated): ').split()))
        tuple2=(z[0],z[1],z[2])
        tuple3=tuple2
        circle=Circle(z[0],z[1],z[2])          #insantiating Circle
        
        Q= int(input('\nEnter the number of queries: '))
        print('\n1) R deg (rx) (ry)')
        print('2) T dx (dy)')
        print('3) S sx (sy)')
        print('4) P')
        q=0
        while q<Q:
          query_input=list(map(str,input('\nEnter the query for the circle (space separated): ').split()))
          
          if query_input[0]=='T':
            tuple3=tuple2
            if len(query_input)==2:

              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.translate(float(query_input[1]),float(query_input[1]))    #calls translate method from class Circle
              for i in tuple2:
                print(i,end=' ' )
              print()
              circle.plot()
            else:
              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.translate(float(query_input[1]),float(query_input[2]))     #calls translate method from class Circle
              for i in tuple2:
                print(i,end=' ' )
              print()
              circle.plot()                                                            #calls plot method from class Circle
          
          elif query_input[0]=='S':
            tuple3=tuple2
            for i in tuple2:
              print(i,end=' ' )
            print()
            tuple2=circle.scale(float(query_input[1]))                                  #calls scale method from class Circle
            for i in tuple2:
              print(i,end=' ' )
            print()
            circle.plot()
          
          elif query_input[0]=='R':
            tuple3=tuple2
            if len(query_input)==2:

              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.rotate(float(query_input[1]))                               #calls rotate method from class Circle
              for i in tuple2:
                print(i,end=' ' )
              print()
              circle.plot()
            else:
              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.rotate(float(query_input[1]),float(query_input[2]),float(query_input[3]))   #calls rotate method from class Circle
              for i in tuple2:
                print(i,end=' ' )
              print()
              circle.plot()
          
          elif query_input[0]=='P':
            for i in tuple3:
              print(i,end=' ' )
            print()
            for i in tuple2:
              print(i,end=' ' )
            print()
            circle.plot()
            

          q=q+1  

          
      elif y == 0 :
        while True:

            n=int(input('\nEnter the numer of sides of the polygon: '))
            if n>=3:
              j=0
              k=[]
              
          
              while j<n:
                r=list(map(float,input('\nEnter the co-ordinates of the polygon (space separated): ').split()))
                r.append(1)
                k.append(r)
                j=j+1
          
              A=np.array(k)
              k2=A.transpose()
              k2=np.delete(k2,len(k2)-1,0)
              k3=k2
              poly=Polygon(A)
              Q= int(input('\nEnter the number of queries: '))
              print('\n1) R deg (rx) (ry)')
              print('2) T dx (dy)')
              print('3) S sx (sy)')
              print('4) P')
              q=0
              while q<Q:
                query_input=list(map(str,input('\nEnter the query for the polygon (space separated): ').split()))

                if query_input[0]=='T':
                  k3=k2
                  if len(query_input)==2:
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()

                    k2=poly.translate(float(query_input[1]),float(query_input[1]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    poly.plot()
                  else:
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    k2=poly.translate(float(query_input[1]),float(query_input[2]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    poly.plot()
          
                elif query_input[0]=='S':
                  k3=k2
                  if len(query_input)==2:
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    k2=poly.scale(float(query_input[1]),float(query_input[1]))
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    poly.plot()
                  else:
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    k2=poly.scale(float(query_input[1]),float(query_input[2]))
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    poly.plot()
          
                elif query_input[0]=='R':
                  k3=k2
                  if len(query_input)==2:

                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    k2=poly.rotate(float(query_input[1]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    poly.plot()
                  else:
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    k2=poly.rotate(float(query_input[1]),float(query_input[2]),float(query_input[3]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    poly.plot()
                elif query_input[0]=='P':
                  for i in k3:
                    for j in i:
                      print(j,end=' ')
                  print()
                  
                  for i in k2:
                    for j in i:
                      print(j,end=' ')
                  print()
                  poly.plot()
                  
              q=q+1


              break
            
            else:
              print('\nInvalid input for number of side of polygon')
          

      

    
  
    elif x==0:

      y=int(input('\nEnter 1 for circle or 0 for polygon: '))
      if y == 1 :
        z=list(map(float,input('\nEnter the co-ordinates of centre and the radius of circle(space separated): ').split()))
        tuple2=(z[0],z[1],z[2])
        circle=Circle(z[0],z[1],z[2])
        
        Q= int(input('\nEnter the number of queries: '))
        print('\n1) R deg (rx) (ry)')
        print('2) T dx (dy)')
        print('3) S sx (sy)')
        print('4) P')
        q=0
        while q<Q:
          query_input=list(map(str,input('\nEnter the query for the circle (space separated): ').split()))
          
          if query_input[0]=='T':
            tuple3=tuple2
            if len(query_input)==2:

              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.translate(float(query_input[1]),float(query_input[1]))
              for i in tuple2:
                print(i,end=' ' )
              print()
              
            else:
              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.translate(float(query_input[1]),float(query_input[2]))
              for i in tuple2:
                print(i,end=' ' )
              print()
              
          
          elif query_input[0]=='S':
            tuple3=tuple2
            for i in tuple2:
              print(i,end=' ' )
            print()
            tuple2=circle.scale(float(query_input[1]))
            for i in tuple2:
              print(i,end=' ' )
            print()
            
          
          elif query_input[0]=='R':
            tuple3=tuple2
            if len(query_input)==2:

              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.rotate(float(query_input[1]))
              for i in tuple2:
                print(i,end=' ' )
              print()
              
            else:
              for i in tuple2:
                print(i,end=' ' )
              print()
              tuple2=circle.rotate(float(query_input[1]),float(query_input[2]),float(query_input[3]))
              for i in tuple2:
                print(i,end=' ' )
              print()
              
          elif query_input[0]=='P':
            for i in tuple3:
              print(i,end=' ' )
            print()
            for i in tuple2:
              print(i,end=' ' )
            print()
            circle.plot()

          q=q+1  

          
      elif y == 0 :
        while True:

            n=int(input('\nEnter the numer of sides of the polygon: '))
            if n>=3:
              j=0
              k=[]
              
          
              while j<n:
                r=list(map(float,input('\nEnter the co-ordinates of the polygon (space separated): ').split()))
                r.append(1)
                k.append(r)
                j=j+1
          
              A=np.array(k)
              k2=A.transpose()
              k2=np.delete(k2,len(k2)-1,0)
              k3=k2
              poly=Polygon(A)
              Q= int(input('\nEnter the number of queries: '))
              print('\n1) R deg (rx) (ry)')
              print('2) T dx (dy)')
              print('3) S sx (sy)')
              print('4) P')
              q=0
              while q<Q:
                query_input=list(map(str,input('\nEnter the query for the polygon (space separated): ').split()))

                if query_input[0]=='T':
                  k3=k2
                  if len(query_input)==2:
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()

                    k2=poly.translate(float(query_input[1]),float(query_input[1]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    
                  else:
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    k2=poly.translate(float(query_input[1]),float(query_input[2]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    
          
                elif query_input[0]=='S':
                  k3=k2
                  if len(query_input)==2:
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    k2=poly.scale(float(query_input[1]),float(query_input[1]))
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    
                  else:
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    k2=poly.scale(float(query_input[1]),float(query_input[2]))
                    for i in k2:
                        for j in i:
                          print(j,end=' ')
                    print()
                    
          
                elif query_input[0]=='R':
                  k3=k2
                  if len(query_input)==2:

                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    k2=poly.rotate(float(query_input[1]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    
                  else:
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    k2=poly.rotate(float(query_input[1]),float(query_input[2]),float(query_input[3]))
                    for i in k2:
                      for j in i:
                        print(j,end=' ')
                    print()
                    
                elif query_input[0]=='P':
                  for i in k3:
                    for j in i:
                      print(j,end=' ')
                  print()
                  
                  for i in k2:
                    for b in i:
                      print(b,end=' ')
                  print()
                  poly.plot()

                q=q+1


              break
            
            else:
              print('\nInvalid input for number of side of polygon')
          

      

    f+=1

