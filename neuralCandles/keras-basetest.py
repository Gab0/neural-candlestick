import os
os.environ["THEANO_FLAGS"] = "device=cpu,force_device=false"#,floatX=float32"

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout

model = Sequential()

model.add(Dense(5, input_dim=5))

print("Done.")
