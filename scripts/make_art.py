#
# make_art.py
#
# LAST EDIT: 2020-10-11
#
# This script uses the DeepDream model in TensorFlow to create a stylized work of art from pictures provided to it.
#
# Tips: You will potentially need to install a few libraries to run the code, including TensorFlow (please see the import statements).
# Running the code in a Python notebook on an online server will allow the final results to display without needing further edits to the code.
# It will also probably take awhile to run, so I recommend using Google Colaboratory and selecting Google's GPU runtime to make it process a little more quickly.
#
# Thanks, and have fun making art!

import tensorflow as tf

import numpy as np

import matplotlib as mpl

import IPython.display as display
import PIL.Image

from tensorflow.keras.preprocessing import image

import argparse

# Comment out the following lines if running in Google Colab or other online notebook server.
parse = argparse.ArgumentParser(description="Uses TensorFlow neural networks to enhance the patterns detected in a picture and create artwork.")
argument = parse.parse_args()


url = 'https://neologisms.blogs.wm.edu/files/2016/04/sunken-garden-at-william-and-mary-jerry-gammon.jpg'


# Download an image and read it into a NumPy array.
def download(url, max_dim=None):
    name = url.split('/')[-1]
    image_path = tf.keras.utils.get_file(name, origin=url)
    img = PIL.Image.open(image_path)
    if max_dim:
        img.thumbnail((max_dim, max_dim))
    return np.array(img)


# Normalize an image
def deprocess(img):
    img = 255 * (img + 1.0) / 2.0
    return tf.cast(img, tf.uint8)


# Display an image
def show(img):
    display.display(PIL.Image.fromarray(np.array(img)))


# Downsizing the image makes it easier to work with.
original_img = download(url, max_dim=500)
show(original_img)
display.display(display.HTML(
    'Image cc-by: <a "href=data:image/png;base64,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>Von.grzanka</a>'))

base_model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')

# Maximize the activations of these layers
names = ['mixed3', 'mixed5']
layers = [base_model.get_layer(name).output for name in names]

# Create the feature extraction model
dream_model = tf.keras.Model(inputs=base_model.input, outputs=layers)


def calc_loss(img, model):
    # Pass forward the image through the model to retrieve the activations.
    # Converts the image into a batch of size 1.
    img_batch = tf.expand_dims(img, axis=0)
    layer_activations = model(img_batch)
    if len(layer_activations) == 1:
        layer_activations = [layer_activations]

    losses = []
    for act in layer_activations:
        loss = tf.math.reduce_mean(act)
        losses.append(loss)

    return tf.reduce_sum(losses)


class DeepDream(tf.Module):
    def __init__(self, model):
        self.model = model

    @tf.function(
        input_signature=(
                tf.TensorSpec(shape=[None, None, 3], dtype=tf.float32),
                tf.TensorSpec(shape=[], dtype=tf.int32),
                tf.TensorSpec(shape=[], dtype=tf.float32),)
    )
    def __call__(self, img, steps, step_size):
        print("Tracing")
        loss = tf.constant(0.0)
        for n in tf.range(steps):
            with tf.GradientTape() as tape:
                # This needs gradients relative to `img`
                # `GradientTape` only watches `tf.Variable`s by default
                tape.watch(img)
                loss = calc_loss(img, self.model)

            # Calculate the gradient of the loss with respect to the pixels of the input image.
            gradients = tape.gradient(loss, img)

            # Normalize the gradients.
            gradients /= tf.math.reduce_std(gradients) + 1e-8

            # In gradient ascent, the "loss" is maximized so that the input image increasingly "excites" the layers.
            # You can update the image by directly adding the gradients (because they're the same shape!)
            img = img + gradients * step_size
            img = tf.clip_by_value(img, -1, 1)

        return loss, img


deepdream = DeepDream(dream_model)


def run_deep_dream_simple(img, steps=100, step_size=0.01):
    # Convert from uint8 to the range expected by the model.
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    img = tf.convert_to_tensor(img)
    step_size = tf.convert_to_tensor(step_size)
    steps_remaining = steps
    step = 0
    while steps_remaining:
        if steps_remaining > 100:
            run_steps = tf.constant(100)
        else:
            run_steps = tf.constant(steps_remaining)
        steps_remaining -= run_steps
        step += run_steps

        loss, img = deepdream(img, run_steps, tf.constant(step_size))

        display.clear_output(wait=True)
        show(deprocess(img))
        print("Step {}, loss {}".format(step, loss))

    result = deprocess(img)
    display.clear_output(wait=True)
    show(result)

    return result


dream_img = run_deep_dream_simple(img=original_img, steps=100, step_size=0.01)