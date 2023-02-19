from keras.models import Sequential
from keras import optimizers
from keras.layers import Conv1D, BatchNormalization, MaxPooling1D, LSTM, Dense, Activation, Dropout
from keras_self_attention import SeqSelfAttention

def emo1d(trainX, trainy, args):
	n_timesteps, n_features, n_outputs = trainX.shape[1], trainX.shape[2], trainy.shape[1]

	model = Sequential(name='Emo1D')

	# LFLB1
	model.add(Conv1D(filters=64, kernel_size=3, padding='same', activation='relu', input_shape=(n_timesteps, n_features)))
	model.add(Conv1D(filters=64, kernel_size=3, padding='same', activation='relu'))
	model.add(BatchNormalization())
	model.add(Dropout(.5))
	model.add(MaxPooling1D(pool_size=2))

	# LSTM
	model.add(LSTM(args.num_fc, return_sequences=True, input_shape=(None, 26)))
	model.add(SeqSelfAttention(attention_activation='tanh'))
	model.add(LSTM(args.num_fc, return_sequences=False))

	model.add(Dense(n_outputs, activation='softmax'))
	
	opt = optimizers.Adam(learning_rate=args.learning_rate, decay=args.decay)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['categorical_accuracy'])

	return model