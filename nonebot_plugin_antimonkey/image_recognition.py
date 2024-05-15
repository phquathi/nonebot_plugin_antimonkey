import tensorflow as tf
from keras.src.applications import imagenet_utils
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import decode_predictions
import numpy as np
import cv2

# MobileNetV2模型
model = MobileNetV2(weights="imagenet")


def check_image(image: np.ndarray) -> bool:
    """
    检查图像中是否有猴子。
    :param image: OpenCV图像数组。
    :return: 如果图像中有猴子，返回True；否则返回False。
    """
    # 调整图像大小为模型所需的尺寸
    image = cv2.resize(image, (224, 224))

    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    predictions = model.predict(image)
    results = imagenet_utils.decode_predictions(predictions)

    monkey_labels = {
        "guenon", "guenon monkey",
        "patas", "hussar monkey", "Erythrocebus patas",
        "baboon",
        "macaque",
        "langur",
        "colobus", "colobus monkey",
        "proboscis monkey", "Nasalis larvatus",
        "marmoset",
        "capuchin", "ringtail", "Cebus capucinus",
        "howler monkey", "howler",
        "titi", "titi monkey",
        "spider monkey", "Ateles geoffroyi",
        "squirrel monkey", "Saimiri sciureus"
    }

    for _, label, probability in results[0]:
        if label in monkey_labels and probability > 0.1:  # 阈值
            print(f"({probability:.2f})")
            return True
    print(f"({probability:.2f})")
    return False

# if __name__ == "__main__":
#     test_image_path = 'monkey_test.jpg'
#
#
#     test_image = cv2.imread(test_image_path)
#
#
#     if test_image is not None:
#         result = check_image(test_image)
#         if result:
#             print("检测到猴子!")
#         else:
#             print("未检测到猴子。")
#     else:
#         print("无法读取测试图片。")
