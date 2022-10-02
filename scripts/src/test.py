import numpy
import pandas

x = numpy.array([[5,4],[7,2],[9,1],[6,3]])
diff = numpy.append(x[:,-1][1:] - x[:,-1][:-1], 0)
diff = [[i] for i in diff]
print(diff)
print(x.shape)
diff = numpy.append(x, diff, axis=1)
print(diff)
1/0
print(x[:,1][1:] - x[:,1][:-1])
print(int(x[1:] - x[:-1]))
1/0
print(numpy.diff(x))
y = numpy.diff(x, axis=0) / x[:,1:] * 100

print(y)

df = pandas.DataFrame(columns=["A", "B", "C"], data=[
    {"A": 1, "B": 3, "C": 7},
    {"A": 5, "B": 4, "C": 5},
    {"A": 6, "B": 2, "C": 1},
    {"A": 8, "B": 2, "C": 1},
    {"A": 6, "B": 2, "C": 1},
    {"A": 7, "B": 2, "C": 1}
])

df["diff_A"] = df["A"].pct_change(periods=4)
df["diff_B"] = df["B"].pct_change()
df["diff_C"] = df["C"].pct_change()
print(df)
