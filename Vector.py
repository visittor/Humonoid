import math

class Vector():

    # class point():
    #     def __init__(self,x,y):
    #         self.x= x
    #         self.y = y
    #
    #     def __getitem__(self, item):
    #         if type(item) == int or type(item) == float:
    #             if item == 0:
    #                 return self.x
    #             elif item == 1:
    #                 return self.y
    class matrix():

        def __init__(self,size,member=[]):
            '''size[0] is Row size[1] is collumn '''
            self.size = (size[0],size[1])
            self.data = []
            # print self.size
            for i in member:
                self.data.append(float(i))
            while len(self.data) < size[0]*size[1]:
                self.data.append(0.0)

        def multiplyRow(self,value,Row):
            for i in range (1,self.size[1]+1):
                # print 'mul',self.RowCol2Index((Row, i)), (Row, i)
                self.data[self.RowCol2Index((Row,i))] *= float(value)

        def addRow2Row(self,Row1,Row2,mulRow1 = 1,mulRow2 = 1):
            for j in range (1,self.size[1]+1):
                # print self.RowCol2Index((Row1,j)), (Row1,j)
                self.data[self.RowCol2Index((Row1,j))] *= mulRow1
                self.data[self.RowCol2Index((Row1, j))] += self.data[self.RowCol2Index((Row2, j))]*mulRow2



        def Indx2RowCol(self, indx):
            i = int(int(indx) / int(self.size[1])) + 1
            j = indx % self.size[1] + 1
            return (i, j)

        def RowCol2Index(self, RowCol):
            index = (RowCol[0] - 1) * self.size[1] + RowCol[1] - 1
            return index



    class line():
        def __init__(self,p1,p2):
            self.startPoint = Vector.vectorCreate(p1,(0,0))
            self.vectorEquation(p1,p2)

        def vectorEquation(self,p1,p2):
            self.vector = Vector.vectorCreate(p1,p2)
            self.vector = self.vector.normalize()

    class vectorCreate():
        x = 0
        y = 0
        def __init__(self,p1,p2):
            self.x =float(p1[0]-p2[0])
            self.y = float(p1[1]-p2[1])
            self.point1 = (p1[0],p1[1])
            self.point2 = (p2[0],p2[1])
            self.length = math.sqrt((self.x*self.x)+(self.y*self.y))
        def __add__(self, other):
            x = self.x + other.x
            y = self.y + other.y
            # obj =  Vector.vectorCreate((x,y),(0,0))
            return  Vector.vectorCreate((x,y),(0,0))

        def __sub__(self, other):
            x = self.x - other.x
            y = self.y - other.y
            return Vector.vectorCreate((x,y),(0,0))

        def __mul__(self,other):
            if type(other) == int or  type(other) == float:
                x = self.x*other
                y = self.y*other
                return Vector.vectorCreate((x,y),(0,0))
            dot = (self.x * other.x) + (self.y * other.y)
            return dot

        def __str__(self):
            text = '{:}i + {:}j'.format(self.x,self.y)
            return text

        def normalize(self):
            x = float(self.x / (self.length))
            y = float(self.y / (self.length))
            # print 'X:',x,'Y:',y,'vec.x:',vec.x,'vec.length:',vec.length
            return Vector.vectorCreate((x, y), (0, 0))



    def __init__(self):
        pass

    def equaSolv(self, coff, cont):
        print 'coff= ', coff.data
        print 'cont= ', cont.data
        if coff.size[0] != coff.size[1] or cont.size[0] != coff.size[0] or cont.size[1] != 1:
            print 'error'
            return

        for i in range(1, coff.size[1] + 1):
            print 'coff= ', coff.data
            print 'cont= ', cont.data
            if coff.data[coff.RowCol2Index((i, i))] == 0:
                for k in range(1,coff.size[1] + 1):
                    if coff.data[coff.RowCol2Index((k,i))] != 0:
                        multi = 1/ (coff.data[coff.RowCol2Index((k, i))])
                        coff.addRow2Row(i, k, mulRow2=multi)
                        cont.addRow2Row(i, k, mulRow2=multi)
                        print 'Add row {} with row {} * {}'.format(i, k, multi)
                        break

            else:
                multi = 1 / coff.data[coff.RowCol2Index((i, i))]
                coff.multiplyRow(float(multi), i)
                cont.multiplyRow(float(multi), i)
                print 'multi Row {} by {}'.format(i, multi)

            for j in range(1, coff.size[1] + 1):
                print 'coff= ', coff.data
                print 'cont= ', cont.data
                if i == j :
                    pass
                    # if  coff.data[coff.RowCol2Index((j, i))]==1:
                    #     pass
                    #
                    # else:
                    #     if coff.data[coff.RowCol2Index((j, i))] == 0:
                    #         multi = (-1) * (coff.data[coff.RowCol2Index((j, i))] / coff.data[coff.RowCol2Index((i, i))])
                    #
                    #     else:
                    #         multi = 1 / coff.data[coff.RowCol2Index((j, i))]
                    #         coff.multiplyRow(float(multi), i)
                    #         cont.multiplyRow(float(multi), i)
                    #         print 'multi Row {} by {}'.format(i,multi)

                else:
                    if coff.data[coff.RowCol2Index((j, i))] == 0:
                        pass
                    else:
                        multi = (-1)*(coff.data[coff.RowCol2Index((j, i))]/ coff.data[coff.RowCol2Index((i, i))])
                        # print multi
                        coff.addRow2Row(j,i,mulRow2=multi)
                        cont.addRow2Row(j,i,mulRow2=multi)
                        print 'Add row {} with row {} * {}'.format(j,i,multi)

        for i in range(1,coff.size[1]+1):
            print 'coff= ', coff.data
            print 'cont= ', cont.data
            multi = 1/coff.data[coff.RowCol2Index((i,i))]
            coff.multiplyRow(float(multi),i)
            cont.multiplyRow(float(multi),i)
            print 'multi Row {} by {}'.format(i, multi)

        print 'coff= ', coff.data
        print 'cont= ', cont.data
        return cont

    def intersect(self,line1,line2):
        coff = [line1.vector.x, -line2.vector.x, line1.vector.y, -line2.vector.y]
        cont = [line2.startPoint.x - line1.startPoint.x, line2.startPoint.y - line1.startPoint.y]
        print 'coff',coff,line2.startPoint.x,line1.startPoint.x
        coff = self.matrix((2, 2), coff)
        cont = self.matrix((2, 1), cont)
        self.equaSolv(coff, cont)
        t4line1 = cont.data[0]
        print 'start',line1.startPoint,line1.vector*t4line1
        pointIntersect = line1.startPoint + line1.vector* t4line1
        print pointIntersect
        return pointIntersect

    def dotproduct(self,vec1,vec2):
        dot = (vec1.x*vec2.x)+(vec1.y*vec2.y)
        return dot

    def cosAngle(self,vec1,vec2):
        # dot = self.dotproduct(vec1,vec2)
        dot = vec1*vec2
        cos = (dot) / (vec1.length * vec2.length)
        return cos

    def findAngle(self,pt1,pt2,pt3):
        vec1 = self.vectorCreate(pt1,pt2)
        vec2 = self.vectorCreate(pt3,pt2)
        cosAngle = self.cosAngle(vec1,vec2)
        return cosAngle

    def findLenght(self,pt1,pt2):
        vec = self.vectorCreate(pt1,pt2)
        return vec.length

    def creatVector(self,pt1,pt2):
        vec = self.vectorCreate(pt1,pt2)
        return vec



class circleCalculator(Vector):
    class __circle(Vector):
        R = 0
        Center = 0
        Pts = []
        def __init__(self,pt1,pt2,pt3,Center = False):
            if Center:
                self.Center = pt1
                self.R = pt2
                self.Pts = None
            else:
                self.Center,self.R = self.findCicle(pt1,pt2,pt3)
                self.Pts = [pt1,pt2,pt3]
        def findCenterPoint(self,p1,p2,p3):
            middlePoint1 = ((float(p1[0])+float(p2[0]))/2,(float(p1[1])+float(p2[1]))/2)
            middlePoint2 = ((p3[0]+p2[0])/2,(p3[1]+p2[1])/2)
            eq1 = [0,0,0] # mx+c = ny
            eq2 = [0,0,0] # mx+c = ny
            if p1[1]-p2[1] == 0.0:
                eq1[2] = 0.0
                eq1[0] = 1.0
                eq1[1] = -middlePoint1[0]
            else:
                eq1[0] =(-1*(float(p2[0])-float(p1[0])))/(float(p2[1])-float(p1[1]))
                eq1[1] = (middlePoint1[1]-eq1[0]*middlePoint1[0])
                eq1[2] = 1.0
            if p2[1]-p3[1] == 0.0:
                eq2[2] = 0.0
                eq2[0] = 1.0
                eq2[1] = -middlePoint2[0]
            else:
                eq2[0] =(-1*(float(p2[0])-float(p3[0])))/(float(p2[1])-float(p3[1]))
                eq2[1] = (middlePoint2[1]-eq2[0]*middlePoint2[0])
                eq2[2] = 1.0
            x = (eq2[1]*eq1[2]-eq1[1]*eq2[2])/(eq1[0]*eq2[2]-eq2[0]*eq1[2])
            y = (x*eq2[0]+eq2[1])
            # print eq1,eq2
            return (x,y)

        def findRadius(self,p1,p2,p3):
            center = self.findCenterPoint(p1,p2,p3)
            radius = math.sqrt(((p1[0] - center[0]) ** 2) + ((p1[1] - center[1]) ** 2))
            return (center,radius)

        def findCicle(self,p1,p2,p3):
            if p3 is not None:
                return self.findRadius(p1,p2,p3)
            elif p3 is None:
                center = ((p1[0]+p2[0])/2,(p1[1]+p2[1])/2)
                radius = self.findLenght(p1,p2)/2
                return (center,radius)
    def __init__(self):
        pass
    def findMinCircle(self,Points):
        found = False
        if Points is None:
            return None
        while len(Points)>2:
            circles = []
            for ptIndx in range(0,len(Points)):
                circle = self.__circle(Points[ptIndx],Points[(ptIndx+1)%len(Points)],Points[(ptIndx+2)%len(Points)])
                circles.append((circle,(ptIndx+1)%len(Points)))
            circles = sorted(circles,key=lambda x:x[0].R)
            C = circles[0]
            Pts = C[0].Pts
            angle = self.findAngle(Pts[0],Pts[1],Pts[2])
            if angle<0:
                Points.pop(C[1])

            elif angle>=0:
                found = True
                break
        if found == True:
            MinCircle = C[0]
            return MinCircle
        elif len(Points)==2:
            MinCircle = self.__circle(Points[0],Points[1],None)

            return MinCircle
        else:
            return None
    def circleCreate(self,center,R):
        if center is not None or R is not None:
            circle =self.__circle(center,R,None,Center=True)
            return circle
        else:
            return None

if __name__ == "__main__":
    vector = Vector()
    v1 = vector.vectorCreate((10,10),(9,9))
    v2 = vector.vectorCreate((10,0),(9,0))
    v3 = v2+v1
    # angle = v2.cosAngle(v1,v2)
    # v3 = v2.normalize()
    print v3.x, v1.x , v2.y
    c = [7,1,5,4,8,5,9,7,2,70,6,6,4,7,8,9]
    v = [1,2,2,2]
    coff = vector.matrix((4,4),c)
    cont = vector.matrix((4,1),v)
    vector.equaSolv(coff,cont)