import os
import time
from os import listdir
from os.path import isdir, join

from PIL import Image
from mtcnn.mtcnn import MTCNN
from numpy import asarray, around
from scipy import linalg
from tensorflow import keras

def extract_face(filename, required_size=(160, 160)):
    """
    从图片文件中加载照片，并返回提取的人脸。
    :param filename: 图片文件
    :param required_size:人脸区域图片的尺寸
    :return: 人脸区域的数组形式
    """
    image = Image.open(filename)
    image = image.convert('RGB')
    pixels = asarray(image)

    # 创建一个 MTCNN 人脸检测器类，并使用它来检测加载的照片中所有的人脸。
    detector = MTCNN()

    # 结果是一个边界框列表，其中每个边界框定义了边界框的左下角，以及宽度和高度。
    results = detector.detect_faces(pixels)

    # 确定边界框的像素坐标,有时候库会返回负像素索引，可以通过取坐标的绝对值来解决这一问题。
    x1, y1, width, height = results[0].get("box")
    x1, y1 = abs(x1), abs(y1)
    x2, y2 = x1 + width, y1 + height

    # 使用这些坐标来提取人脸
    face = pixels[y1:y2, x1:x2]

    # 将这个人脸的小图像调整为所需的尺寸；
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


def img_to_encoding(images, model):
    # 这里的操作实际是对channel这一dim进行reverse，从BGR转换为RGB
    images = images[..., ::-1]
    images = around(images / 255.0, decimals=12)  # np.around是四舍五入，其中decimals是保留的小数位数,这里进行了归一化
    # https://stackoverflow.com/questions/44972565/what-is-the-difference-between-the-predict-and-predict-on-batch-methods-of-a-ker
    if images.shape[0] > 1:
        embedding = model.predict(images, batch_size=128)  # predict是对多个batch进行预测，这里的128是尝试后得出的内存能承受的最大值
    else:
        embedding = model.predict_on_batch(images)  # predict_on_batch是对单个batch进行预测
    # 报错，operands could not be broadcast together with shapes (2249,128) (2249,)，因此要加上keepdims = True
    embedding = embedding / linalg.norm(embedding, axis=1,
                                        keepdims=True)  # 注意这个项目里用的keras实现的facenet模型没有l2_norm，因此要在这里加上

    return embedding


class Dataset:
    def __init__(self, path_name, retrain=False):
        # 训练集
        self.X_train = None
        self.y_train = None
        # 测试集
        self.X_test = None
        self.y_test = None
        # 数据集加载路径
        self.path_name = path_name
        # 是否继续训练
        self.retrain = retrain

    def load_faces(self, directory, per_num=0):
        """
        提取同一目录下的所有人脸
        :param directory: 如“all-samples/train/skylar”，该目录下为skylar的个人照片
        :param per_num: 提取数据集中每人的照片数，缺省值为0， 表示读取全部图片
        :return:
        """
        faces = list()
        for filename in listdir(directory):
            path = directory + filename
            face = extract_face(path)
            faces.append(face)
            if per_num != 0 and len(faces) >= per_num:
                break

        return faces

    def load_dataset(self, directory, per_num):
        """
        提取数据集中的所有人脸数据，为每个检测到的人脸分配标签
        :param directory: 如 “all-samples/train/”、 “all-samples/test/”
        :return:
        """
        X, y = list(), list()

        if self.retrain:
            # 继续训练
            for subdir in listdir(directory):
                path = directory + subdir + '/'
                # 1. 跳过directory中非目录文件 2. 文件夹的修改时间大于5分钟的样本不进行模型训练
                if (not isdir(path)) or (time.time() - os.path.getmtime(path) > 300):
                    continue
                faces = self.load_faces(path, per_num)
                labels = [subdir for _ in range(len(faces))]
                print('>loaded %d examples for class: %s' % (len(faces), subdir))
                # store
                X.extend(faces)
                y.extend(labels)
            return asarray(X), asarray(y)

        for subdir in listdir(directory):
            path = directory + subdir + '/'
            # skip any files that might be in the dir
            if not isdir(path):
                continue
            # load all faces in the subdirectory
            faces = self.load_faces(path, per_num)
            # create labels
            labels = [subdir for _ in range(len(faces))]
            # summarize progress
            print('>loaded %d examples for class: %s' % (len(faces), subdir))
            # store
            X.extend(faces)
            y.extend(labels)
        return asarray(X), asarray(y)

    def load(self, model, per_num=0):
        """
        加载数据集
        :param model:
        :param per_num:
        :return:
        """
        train_path = join(self.path_name, "train/")
        test_path = join(self.path_name, "test/")

        if isdir(train_path):
            images, labels = self.load_dataset(train_path, per_num)
            train_embedding = img_to_encoding(images, model)
            print('X_train shape: {}, y_train shape: {}'.format(train_embedding.shape, labels.shape))
            print('train total samples: {}'.format(train_embedding.shape[0]))
            self.X_train = train_embedding
            self.y_train = labels

        if isdir(test_path) and not self.retrain:
            # 测试样本不进行重新训练
            images, labels = self.load_dataset(test_path, 0)
            test_embedding = img_to_encoding(images, model)
            print('X_test shape: {}, y_test shape: {}'.format(test_embedding.shape, labels.shape))
            print('test total samples: {}'.format(test_embedding.shape[0]))
            self.X_test = test_embedding
            self.y_test = labels


def create_model():
    model = keras.models.load_model('facenet_keras.h5')
    print('Loaded Model, inputs:{}, outputs:{}'.format(model.inputs, model.outputs))
    return model