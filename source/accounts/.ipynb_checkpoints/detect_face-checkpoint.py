
# face detection with mtcnn on a photograph
from matplotlib import pyplot
from mtcnn import MTCNN


def detect_face(img):
    pixels = pyplot.imread(img)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    print(faces)
    return len(faces)