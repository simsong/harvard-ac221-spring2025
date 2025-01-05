#!/usr/bin/env python3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'  # or any number from 0-3

import sys
import tensorflow as tf
import tensorflow.keras
import platform

# Ensure TensorFlow uses the GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            print(gpu)
            tf.config.experimental.set_memory_growth(gpu, True)
        print("TensorFlow is using the GPU.")
    except RuntimeError as e:
        print(e)
else:
    print("TensorFlow is not using the GPU. Check your TensorFlow installation.")


if __name__ == '__main__':
    print(f"Python               {sys.version}")
    print(f"Python Platform:     {platform.platform()}")
    print(f"Tensor Flow Version: {tf.__version__}")
    print(f"Keras Version:       {tensorflow.keras.__version__}")
    print("len(tf.config.list_physical_devices('GPU')) ", len(tf.config.list_physical_devices('GPU')))
    print("tf.config.list_physical_devices('GPU')      ", tf.config.list_physical_devices('GPU'))

    # Create some tensors
    print("\nExample:")
    tf.debugging.set_log_device_placement(True)
    a = tf.constant([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
    b = tf.constant([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    c = tf.matmul(a, b)
    print(f"{a} * {b} == {c}")
