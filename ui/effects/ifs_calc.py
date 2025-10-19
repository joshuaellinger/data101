import numpy as np
from typing import List

class IFSTransform:
    def __init__(self, name: str, parameters: List):
        self.name = name

        self.original = parameters
        n = len(parameters)

        lines = np.zeros((n,8))
        for i, p in enumerate(parameters):
            lines[i, 0:4] = np.reshape(p[0], shape=(4,))   # stretch 
            lines[i, 4:6] = p[1]      # shift
            lines[i, 6]   = p[2]      # rotation
            lines[i, 7]   = p[3]      # probability
        self.parameters = lines
    
        p = lines[:,7]        
        self.probabilities = p / p.sum()

        self.stretch = [ np.reshape(lines[i, 0:4], shape=(2,2)) for i in range(n) ]
        self.shift = [ self.parameters[i, 4:6] for i in range(n) ]
  
        self.theta = lines[:, 6].T
        self.rotation = [ np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]]) for t in lines[:,6] ] 


    def select_line(self) -> int:
        # Select random set based on probability set
        n = len(self.probabilities)
        return (np.random.choice(n, 1, p=self.probabilities))[0]

    def calculate(self, pt: np.array, k: int) -> np.ndarray:
        # returns a point projected using affine transformation

        theta = self.theta[k]
        stretch = self.stretch[k]
        shift = self.shift[k]
        rotation = self.rotation[k]

        pt = np.add(np.matmul(rotation, np.matmul(stretch, pt)), shift.transpose())
        return pt.transpose()


# ========================== Predefined Transformations =======================
# Predefined Transformations: [MATRIX as [[A,B],[C,D]], SHIFTS as [X,Y], ROTATION ,PROBABILITY]
na = np.array

# Fern
barnsleyTransform = [
    [na([[0,0],[0,0.16]]),na([0,0]),0,0.01],
    [na([[0.85,0.04],[0-0.04,0.85]]),na([0,1.6]),0,0.85],
    [na([[0.2,0-0.26],[0.23,0.22]]),na([0,1.6]),0,0.07],
    [na([[0-0.15,0.28],[0.26,0.24]]),na([0,0.44]),0,0.07]
]
# Rose
roseLikeTransform = [
    [na([[0,0],[0,0.16]]),na([0,0]),0,0.01],
    [na([[0.85,0.04],[0-0.04,0.85]]),na([0,1.6]),45,0.85],
    [na([[0.2,0-0.26],[0.23,0.22]]),na([0,1.6]),3,0.10],
    [na([[0-0.15,0.28],[0.26,0.24]]),na([0,0.44]),0,0.04]
]
# Galaxy
nsnTransform = [
    [na([[0,0],[0,0.16]]),na([0,0]),0,0.01],
    [na([[0.85,0.04],[0-0.04,0.85]]),na([0,1.6]),60,0.85],
    [na([[0.2,0-0.26],[0.23,0.22]]),na([0,1.6]),5,0.10],
    [na([[0-0.15,0.28],[0.26,0.24]]),na([0,0.44]),0,0.04]
]
# Serenpenski Triangle
triangle = [
    [na([[0.5,0],[0,0.5]]),na([0,0]),0,0.33],
    [na([[0.5,0],[0,0.5]]),na([0.5,0]),0,0.33],
    [na([[0.5,0.0],[0.0,0.5]]),na([0.25,0.433]),0,0.34]
]
# Golden Dragon
goldenDragon = [
    [na([[0.62367,0-0.40337],[0.40337,0.62367]]),na([0,0]),0,0.5],
    [na([[0-0.37633,0-0.40337],[0.40337,0-0.37633]]),na([0.5,0]),0,0.5]
]
# Golden Dragon Variant Branch
branch=[
    [na([[0.62327,0-0.40337],[0.40337,0.62327]]),na([0,0]),32.8938,0.5],
    [na([[0-0.37633,0-0.40337],[0.40337,0-0.37633]]),na([1,0]),133.014178,0.5]
]
# Binary Tree
symetricBinaryTree = [
    [na([[0.7,0],[0,0.7]]),na([0,1]),9,0.33],
    [na([[0.7,0],[0,0.7]]),na([0,1]),0-9,0.33],
    [na([[1,0],[0,1]]),na([0,0]),0,0.34]
]
# Pentadentrite
pentadentrite=[
    [na([[0.341,0-0.071],[0.071,0.341]]),na([0,0]),0,0.17],
    [na([[0.038,0-0.346],[0.346,0.038]]),na([0.341,0.071]),0,0.17],
    [na([[0.341,0-0.071],[0.071,0.341]]),na([0.379,0.418]),0,0.17],
    [na([[0-0.234,0.258],[0-0.258,0-0.234]]),na([0.720,0.489]),0,0.17],
    [na([[0.173,0.302],[0-0.302,0.173]]),na([0.486,0.231]),0,0.16],
    [na([[0.341,0-0.071],[0.071,0.341]]),na([0.659,0-0.071]),0,0.16]
]
# Koch Curve
koch=[
    [na([[0.3,0],[0,0.3]]),na([0,0]),0,0.25],
    [na([[0.16,0-0.23],[0.23,0.16]]),na([0.3,0]),0,0.25],
    [na([[0.16,0.23],[0-0.23,0.16]]),na([0.5,0.23]),0,0.25],
    [na([[0.3,0],[0,0.3]]),na([0.6,0]),0,0.25]
]
# Make predefined easier
allIFS = {}
allIFS["barnsley"] = barnsleyTransform
allIFS["fern"] = barnsleyTransform
allIFS["rose"] = roseLikeTransform
allIFS["nsn"] = nsnTransform
allIFS["triangle"] = triangle
allIFS["goldendragon"] = goldenDragon
allIFS["tree"]= symetricBinaryTree
allIFS["branch"]=branch
allIFS["penta"]=pentadentrite
allIFS["koch"]=koch

for n in allIFS:
    allIFS[n] = IFSTransform(n, allIFS[n])

# =============================================================================

def get_ifs_transform_by_name(name: str) -> IFSTransform:
    return allIFS[name]

# Iterated Function System
def compute_ifs(numPoints: int, transformations: IFSTransform, initialPoint=np.array([1,1])) -> np.ndarray:

    points = np.zeros((numPoints+1, 2))
    points[0,:] = initialPoint

    n = len(transformations.parameters)

    pt = initialPoint.copy()
    for i in range(0, numPoints):

        # Select a transform line based on probability
        k = transformations.select_line()
        #k = i % n

        # Calculate the next point
        pt = transformations.calculate(pt, k) 
    
        points[i+1,:] = pt

    return points

def points_to_index(points: np.ndarray, input_scale, output_dims):
    b_w, s_w = input_scale[0], 1.0/(input_scale[1] - input_scale[0])
    b_h, s_h = input_scale[2], 1.0/(input_scale[3] - input_scale[2])

    w, h = output_dims
    x_idx = np.clip(((points[:,0] - b_w) * s_w * w).astype(np.int32), 0, w-1)
    y_idx = np.clip(((points[:,1] - b_h) * s_h * h).astype(np.int32), 0, h-1)
    return x_idx, y_idx     


# ---------

# Affine Transformation: R(Sx) + m    R Rotation matrix S stretch x vector m shift
def affine(x,theta=0,stretch= np.array([[1,1],[1,1]]) ,shift=np.array([0,0])):
    R = np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    return np.add(np.matmul(R,np.matmul(stretch,x)), shift.transpose())

def ifs(pointsQuantity,transformations,initialPoint=np.array([1,1]),pIndex=3,tIndex=2,sIndex=0,shiftIndex=1,):
    
    allXCord = [initialPoint.item(0),]
    allYCord = [initialPoint.item(1),]

    nextPoint = initialPoint.copy()

    # Sum Probabilities of Transforms
    allProbabilities = []
    for m in transformations:
        allProbabilities.append(m[pIndex])

    n = len(allProbabilities)

    #Run the calculation
    for i in range(0,pointsQuantity):
    
        # Select random set based on probability set
        k = (np.random.choice(len(transformations), 1, p=allProbabilities))[0]
        #k = i % n

        trans = transformations[k]
        
        # Calculate the next point
        nextPoint = (affine(nextPoint,theta=trans[tIndex],stretch=trans[sIndex],shift=trans[shiftIndex])).transpose()
    
        # Store the Cords.
        allXCord.append(nextPoint.item(0))
        allYCord.append(nextPoint.item(1))

    return allXCord, allYCord

def test_original():
    t = get_ifs_transform_by_name("rose")
    
    #x,y = ifs(5, t.original)
    #print(f"x: {x[0:5]}")    
    #print(f"y: {y[0:5]}")

    print("======================")
    pts = compute_ifs(50_000, t)
    a,b = pts[:,0].min(), pts[:,0].max()
    print("x range", a, b)
    a,b = pts[:,1].min(), pts[:,1].max()
    print("y range", a, b)

if __name__ == "__main__":
    test_original()