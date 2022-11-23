import tensorflow as tf
import tensorflow_datasets as tfds

# https://www.tensorflow.org/datasets/keras_example
(ds_train, ds_test), ds_info = tfds.load(
    'mnist',
    split=['train', 'test'],
    shuffle_files=True,
    as_supervised=True,
    with_info=True,
)

def normalize_img(image, label):
  """Normalizes images: `uint8` -> `float32`."""
  return tf.cast(image, tf.float32) / 255., label

ds_train = ds_train.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_train = ds_train.cache()
ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
ds_train = ds_train.batch(128)
ds_train = ds_train.prefetch(tf.data.AUTOTUNE)

ds_test = ds_test.map(
    normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
ds_test = ds_test.cache()
ds_test = ds_test.batch(128)
ds_test = ds_test.prefetch(tf.data.AUTOTUNE)

# https://en.wikipedia.org/wiki/LeNet
# https://towardsdatascience.com/convolutional-neural-network-champions-part-1-lenet-5-7a8d6eb98df6
# tanh? original paper is sigmoid!
model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(filters=6, kernel_size=(5,5), padding='same', activation='tanh', input_shape=(28, 28, 1)),
  tf.keras.layers.MaxPool2D(strides=2),
  tf.keras.layers.Conv2D(filters=16, kernel_size=(5,5), padding='same', activation='tanh'),
  tf.keras.layers.MaxPool2D(strides=2),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(120, activation='tanh'),
  tf.keras.layers.Dense(84, activation='tanh'),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.SGD(0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
)

model.fit(
    ds_train,
    epochs=60,
    validation_data=ds_test,
)