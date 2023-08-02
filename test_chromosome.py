from tensorflow.keras.layers import Dense, Flatten, Dropout, Conv2D, MaxPooling2D, Input, BatchNormalization
from tensorflow.keras.models import Model
from utils import smooth_curve, over_fit_score

def test_chromosome(chromosome, X, y, num_epochs):
    # hyperparameters
    conv_specs = []
    dense_specs = []

    for i in range(len(chromosome[0])):
        conv_specs.append((chromosome[0][i], chromosome[1][i], chromosome[2][i]))

    for i in range(len(chromosome[3])):
        dense_specs.append((chromosome[3][i], chromosome[4][i]))

    # architecture
    input_layer = Input(shape=(X[0].shape[0], X[0].shape[1], 1))
    x = BatchNormalization()(input_layer)

    for f, k, p in conv_specs:
        x = Conv2D(f, k, activation='relu', kernel_regularizer='l2', bias_regularizer='l2')(x)
        x = MaxPooling2D(p)(x)
        x = BatchNormalization()(x)

    x = Flatten()(x)

    for d, dr in dense_specs:
        x = Dense(d, activation='relu', kernel_regularizer='l2', bias_regularizer='l2')(x)
        x = Dropout(dr)(x)

    output = Dense(4, activation='softmax', kernel_regularizer='l2', bias_regularizer='l2')(x)

    # compile
    model = Model(inputs=input_layer, outputs=output)
    model.compile(loss=['categorical_crossentropy'],
                  optimizer="adam",
                  metrics=['accuracy'])
    # fit
    hist = model.fit(X, y,
                     batch_size=16,
                     epochs=num_epochs,
                     validation_split=0.2,
                     verbose=0)

    smooth_val_loss = min(smooth_curve(hist.history.get('val_loss'), 0.3))
    overfit_score = over_fit_score(hist.history.get('loss'), hist.history.get('val_loss'))

    return (smooth_val_loss + 0.3 * overfit_score)