from xml.etree import cElementTree
import numpy as np
import cv2
import dlib

FOREHEADINDEX = [75,76,68,69,70,71,80,72,73,79,74]
SCALE = {1:1.0848,2:1.4927}

predictor_path = 'assets/shape_predictor_81_face_landmarks.dat'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)


def get_lmk(img):
    if isinstance(img,str):
        img = cv2.imread(img)
    
    dets = detector(img, 0)
    for k, d in enumerate(dets):
        shape = predictor(img, d)
        lmks = np.array([[p.x, p.y] for p in shape.parts()])
    return lmks

def convert_lmk(lmks):
    new_lmks = lmks.copy()
    center = new_lmks[30]
    new_lmks[:18] = 1.25 * new_lmks[:18] - 0.25 * center
    return new_lmks

def add_edge(lmks,h,w):
    lmks = add_lmks_face_outside_edge(lmks,2,SCALE)
    level_scale_3 = get_add_bbox_points_scale(lmks,[w,h])
    lmks = add_circle_points(lmks,level_scale_3)
    return lmks
def add_lmks_face_outside_edge(lmks, level, s):
    '''
    args
        lmks: float (k,2) {lmks+forehead}
        level: int 1|2
        s: dict int->float {1:s1,2:s2}
    ret
        lmks: float (k+t*(k-106),2)
    '''
    lmks_faceedge = lmks[0:18]
    lmks_forhead = lmks[FOREHEADINDEX]
    center = lmks[30]
    if level >= 1:
        add_face_edge = (lmks_faceedge-center)*s[1] + center
        add_forhead = (lmks_forhead-center)*s[1] + center
        lmks = np.concatenate((lmks,add_face_edge,add_forhead), axis=0)
    if level >= 2:
        add_face_edge = (lmks_faceedge-center)*s[2] + center
        add_forhead = (lmks_forhead-center)*s[2] + center
        lmks = np.concatenate((lmks,add_face_edge,add_forhead), axis=0)

    return lmks


def add_circle_points(lmks, scale):
    center = lmks[30]
    xiaba = lmks[8]
    scale = max(scale,10)
    extend_xiaba = (xiaba-center)*scale + center

    n = 12
    per_rad = 2*np.pi/n
    edge_lmks = []
    for i in range(n):
        edge_lmks.append(rotate_rad(center, extend_xiaba[np.newaxis,:], per_rad*i)[0])

    lmks = list(lmks)
    lmks = lmks + edge_lmks
    return np.array(lmks)

def rotate_rad(begp, points, rad):
    '''
    args
        begp: (2,) {xy}
        points: (k,2) {xy}
        rad: float
    ret
        points: float (k,2) {xy}
    '''
    rotated_mat = np.array([[np.cos(rad),-np.sin(rad)],[np.sin(rad),np.cos(rad)]])
    rotated_xy = np.matmul(rotated_mat,(points-begp).T).T+begp
    return rotated_xy

def get_add_bbox_points_scale(lmks, size):
    box = add_bbox_points([],size)
   

    max_dist = max([calc_dist(lmks[30], k) for k in box])
     
    
    dist = calc_dist(lmks[30], lmks[8])
    return 2*max_dist/dist

def add_bbox_points(lmks, size):
    lmks = list(lmks)
    w,h = size
    lmks.append([0,0])
    lmks.append([0,h])
    lmks.append([w,0])
    lmks.append([w,h])
    return np.array(lmks)

def calc_dist(begp, endp):
    '''
    args
        begp,endp: (k,) {xy}
    ret
        dist: float
    '''
    import pdb
    
    return (((endp-begp)**2).sum())**0.5

def getTriangleList(lmks):
    '''
    This function runs very slow, it should run for one time, and save the result into bvt_link/baby_const.py

    args
        lmks: (k,2)
    ret
        tri_set: (t,3) {ix}
    '''
    lmks = lmks - lmks.min() + 1 # make sure no negative numbers
    imgsize = int(lmks.max()+50) # make sure no outside points
    imgsize = (imgsize,imgsize)

    subdiv = cv2.Subdiv2D((0,0,imgsize[0],imgsize[1]))
    for p in lmks:
        subdiv.insert((int(p[0]),int(p[1])))

    triangleList = subdiv.getTriangleList()

    lmks_int = lmks.astype(np.int32)
    del_triangles = []
    for tri in triangleList:
        ps = []
        ps.append((tri[0],tri[1]))
        ps.append((tri[2],tri[3]))
        ps.append((tri[4],tri[5]))
        p1 = [i for i,p in enumerate(lmks_int) if ps[0][0]==p[0] and ps[0][1]==p[1]][0]
        p2 = [i for i,p in enumerate(lmks_int) if ps[1][0]==p[0] and ps[1][1]==p[1]][0]
        p3 = [i for i,p in enumerate(lmks_int) if ps[2][0]==p[0] and ps[2][1]==p[1]][0]
        del_triangles.append((p1,p2,p3))

    del_triangles = np.array(del_triangles, dtype=np.int32)

    return del_triangles

def draw_triset(img,lmks,triangles):
    
    img = cv2.resize(img,None,fx=4,fy=4)
    h,w,_ = img.shape
   
   
    lmks = lmks.astype(np.int32) * 4
    tri_set = np.array(triangles, dtype=np.int32)
    
    lmks_min = np.minimum(np.min(lmks,0),np.array([0,0])) 
    lmks_max = np.maximum(np.max(lmks,0)+1,np.array([w,h]))
    lmks = lmks - lmks_min
    new_img = np.zeros((lmks_max[1]-lmks_min[1],lmks_max[0]-lmks_min[0],3), dtype=np.uint8)
    new_img[-lmks_min[1]:-lmks_min[1]+h,-lmks_min[0]:-lmks_min[0]+w] = img
    color = [255,0,0]

    for tri in tri_set:
        i1,i2,i3 = tri
        cv2.line(new_img, tuple(lmks[i1]), tuple(lmks[i2]), color, 1)
        cv2.line(new_img, tuple(lmks[i1]), tuple(lmks[i3]), color, 1)
        cv2.line(new_img, tuple(lmks[i2]), tuple(lmks[i3]), color, 1)
    
    for i in range(len(lmks)):
        cv2.putText(new_img,str(i),(int(lmks[i][0]),int(lmks[i][1]-5)),cv2.FONT_HERSHEY_COMPLEX,0.75, (0, 255, 0), 2)
    return new_img