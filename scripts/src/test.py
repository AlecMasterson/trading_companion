import numpy
import pandas

df = pandas.DataFrame({
    "A": [i for i in range(4)],
    "B": [i*-2 for i in range(4)],
    "C": [pow(i, 2) for i in range(4)]
})
print(df)

values: numpy.ndarray = df.values

print(values[-3:, :])
