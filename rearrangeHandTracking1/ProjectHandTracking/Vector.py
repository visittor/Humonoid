import math
class Vector():

    class __vectorCreate():
        x = 0
        y = 0
        def __init__(self,p1,p2):
            self.x =p1[0]-p2[0]
            self.y = p1[1]-p2[1]
            self.length = math.sqrt((self.x*self.x)+(self.y*self.y))
        def normalize(self):
            x = self.x / math.sqrt(self.length)
            y = self.y / math.sqrt(self.length)
            return Vector.__vetorCreate(x,y)

    def __init__(self):
        pass

    def dotproduct(self,vec1,vec2):
        dot = (vec1.x*vec2.x)+(vec1.y*vec2.y)
        return dot

    def cosAngle(self,vec1,vec2):
        dot = self.dotproduct(vec1,vec2)
        cos = (dot) / (vec1.length * vec2.length)
        return cos

    def findAngle(self,pt1,pt2,pt3):
        vec1 = self.__vectorCreate(pt1,pt2)
        vec2 = self.__vectorCreate(pt3,pt2)
        cosAngle = self.cosAngle(vec1,vec2)
        return cosAngle

    def findLenght(self,pt1,pt2):
        vec = self.__vectorCreate(pt1,pt2)
        return vec.length

    def creatVector(self,pt1,pt2):
        vec = self.__vectorCreate(pt1,pt2)
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
    v1 = Vector.vetorCreate(10,10)
    v2 = Vector.vetorCreate(10,0)
    angle = v2.cosAngle(v1,v2)
    v3 = v2.normalize()
    print v3.x,v3.y,v3.length,angle