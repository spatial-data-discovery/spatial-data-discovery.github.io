#!/usr/bin/env python
# coding: utf-8
# Last edit: 09/15/2021
# This script runs a ResNet50 model on images of plants to determine if they are flowering
    # I placed a small subset of the data called "image_data_sample" as a walkthrough for this script
    # The data contains images and corresponding labels of flowering or not flowering
    # Place it in the WD and do not mess with it

print('IMPORTANT NOTE: BEFORE YOU START YOU NEED TO DOWNLOAD THE INPUT DATA')
print('The 2.5mb of data can be downloaded via google drive using this link: https://drive.google.com/drive/folders/108Wvq_hYFe1TYKxrhTdvTpVLXrJcgtl-?usp=sharing')
verif_of_data = input('Have you downloaded the data and put in your working directory, y or n?')
if (verif_of_data == 'n') | (verif_of_data == 'no'):
    print('Please download the data using the given link')
else: 
    print('Alright! Running script')
    

    ## Required Packages
    from tensorflow.keras.layers import Conv2D, Flatten, Dense, MaxPool2D, BatchNormalization, GlobalAveragePooling2D
    from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
    from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
    from tensorflow.keras.applications.resnet50 import ResNet50
    from tensorflow.keras.preprocessing import image
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.models import Model
    import matplotlib.pyplot as plt
    import numpy as np
    import tensorflow as tf
    import time
    import ssl
    import smtplib
    import pandas as pd
    import seaborn as sn
    import os



    ## Email setup to alert you of model completion and output info
    # For this to work you may need to change your setting 'less secure app access' to ON
    # I made a junk email for this specifically and suggest you do the same
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    email = input('Enter the email that will send and receive the email (you email yourself): ')
    sender_email = email  # Enter your address
    receiver_email = email  # Enter receiver address
    password = input("Type your password and press enter: ")


    ## Setting up input data for model
    print('Setting up input data for model')
    model_name = input('Type model name here: ')

    HEIGHT__height = 500
    WEIGHT__weight = 300


    train_batch = int(input('Training batch size: '))
    val_batch = int(input('Validation batch size: '))


    training_dir = './resnet50_flowering_image_data_sample/training'
    validation_dir = './resnet50_flowering_image_data_sample/validation'
    testing_dir = './resnet50_flowering_image_data_sample/testing'


    train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input) # can put data augmentations in here

    # Maybe put class mode = binary
    train_generator = train_datagen.flow_from_directory(
        training_dir,
        target_size = (HEIGHT__height, WEIGHT__weight),
        batch_size= train_batch
        # 256
    )


    valid_generator = train_datagen.flow_from_directory(
        validation_dir,
        target_size = (HEIGHT__height, WEIGHT__weight),
        batch_size = val_batch
        #64
    )


    test_generator = train_datagen.flow_from_directory(
        testing_dir,
        target_size = (HEIGHT__height, WEIGHT__weight),
        batch_size = 1
    )


    x,y = test_generator.next()
    x.shape


    ## Establishing model
    print('Establishing model')
    base_model = ResNet50(include_top=False, weights = None)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation = 'relu')(x)
    predictions =Dense(train_generator.num_classes, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)


    for layer in base_model.layers:
        layer.trainable=True


    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


    ## Running model
    print('Running model')
    start = time.time()

    num_epochs = int(input('number of epochs: '))
    history = model.fit(train_generator, epochs=num_epochs, validation_data = valid_generator)

    end = time.time()
    minutes = int((end-start)/60)

    print('This program took ' + str(minutes) + ' minutes to run')
    print('It took ' + str(minutes/num_epochs) + ' minutes per epoch')


    test_loss, test_acc = model.evaluate(test_generator, verbose=2)


    test_acc = str(test_acc)[:6]


    ## Getting the validation scores
    val_acc = history.history['accuracy']
    val_acc = str(val_acc[0])[:6]

    model.save(model_name)

    ## Sending message
    message = """Subject: Hi there! I finished running {model_name}.

    It had a final validation score of {val_score}

    It had a final testing score of {test_score}

    This program took {time_min} minutes to run

    It took {min_per_epoch} minutes per epoch

    Reminder of model hyperparamters:
    Number of epochs = {epoch}
    Training batch size = {tbs}
    Validation batch size = {vbs}

    This message is sent from Python.""".format(model_name = model_name,
                                                time_min = minutes,
                                                min_per_epoch = minutes/num_epochs,
                                               val_score = val_acc,
                                               test_score = test_acc,
                                               epoch = num_epochs,
                                               tbs = train_batch,
                                               vbs = val_batch)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)




    ## Pretty sure this works if do more than 1 epoch - retreives and plots the loss and accuracy for each epoch
    print('Producing plots detailing model performance')
    if num_epochs > 1:

        acc=history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss=history.history['loss']
        val_loss = history.history['val_loss']

        epoch_range = list(range(1, num_epochs +1, 1))

        plt.plot(epoch_range, acc, 'b', label = "Training Accuracy")
        plt.plot(epoch_range, val_acc, 'r', label = "Val Accuracy")
        plt.yscale('linear')
        plt.title('Training and Validation accuracy')
        plt.legend()
        plt.figure()


        plt.plot(epoch_range, loss, 'b', label = "Training Loss")
        plt.plot(epoch_range, val_loss, 'r', label = "Validation Loss")
        plt.yscale('linear')
        plt.title('Training and Valdiation loss')
        plt.legend()
        plt.figure()


    ## Heatmap to check how well model did for each class. Can be used in different way to see how it did for certain species
    model = tf.keras.models.load_model(model_name)
    filesnames= test_generator.filenames
    nb_samples=len(test_generator)

    y_prob=[]
    y_act=[]
    test_generator.reset()
    for _ in range(nb_samples):
        X_test, Y_test = test_generator.next()
        y_prob.append(model.predict(X_test))
        y_act.append(Y_test)

    predicted_class = [list(train_generator.class_indices.keys())[i.argmax()] for i in y_prob]
    actual_class = [list(train_generator.class_indices.keys())[i.argmax()] for i in y_act]


    out_df = pd.DataFrame(np.vstack([predicted_class, actual_class]).T,columns=['predicted_class','actual_class'])
    confusion_matrix = pd.crosstab(out_df['actual_class'], out_df['predicted_class'],
                                   rownames=['Actual'], colnames=['Predicted'])

    sn.heatmap(confusion_matrix, cmap='Blues', annot=True, fmt='d')
    plt.show()
    print('test accuracy : {}'.format((np.diagonal(confusion_matrix).sum()/confusion_matrix.sum()*100)))
