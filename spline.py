# https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.BSpline.html#scipy.interpolate.BSpline
# https://ww2.mathworks.cn/help/curvefit/bspline.html

import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import BSpline
from scipy.interpolate import make_lsq_spline
from scipy.interpolate import make_interp_spline

def B(x, k, i, t):

   if k == 0:

      return 1.0 if t[i] <= x < t[i+1] else 0.0

   if t[i+k] == t[i]:

      c1 = 0.0

   else:

      c1 = (x - t[i])/(t[i+k] - t[i]) * B(x, k-1, i, t)

   if t[i+k+1] == t[i+1]:

      c2 = 0.0

   else:

      c2 = (t[i+k+1] - x)/(t[i+k+1] - t[i+1]) * B(x, k-1, i+1, t)

   return c1 + c2

def naive_bspline(x, t, c, k):
   n = len(t) - k - 1 # picewise curve 个数。
   assert (n >= k+1) and (len(c) >= n)
   return sum(c[i] * B(x, k, i, t) for i in range(n))


def compare_naive_spline():
    k = 2 # B-spline degree
    t = [0, 1, 2, 3, 4, 5, 6] # knot. spline deg = knot -1
    c = [-1, 2, 0, -1] # spline coeffients, 每个picewise_curve的系数， len(c) == n == len(t) -k -1
    spl = BSpline(t, c, k)
    # should equal
    print(spl(2.5), naive_bspline(2.5, t, c, k))


    fig, ax = plt.subplots()

    xx = np.linspace(1.5, 4.5, 50)

    ax.plot(xx, [naive_bspline(x, t, c ,k) for x in xx], 'r-', lw=3, label='naive')

    ax.plot(xx, spl(xx), 'b-', lw=4, alpha=0.7, label='BSpline')

    ax.grid(True)

    ax.legend(loc='best')

    plt.show()

def fit_spline():
    import numpy as np

    import matplotlib.pyplot as plt

    rng = np.random.default_rng()

    x = np.linspace(-3, 3, 50)

    y = np.exp(-x**2) + 0.1 * rng.standard_normal(50)

    t = [-1, 0, 1]
    k = 2
    t = np.r_[(x[0],)*(k+1), t, (x[-1],)*(k+1)]
    print(t)
    # 最小二乘拟合样条，不过输入点
    spl = make_lsq_spline(x, y, t, k)

    # 样条差值，过输入点。
    spl_i = make_interp_spline(x, y)
    xs = np.linspace(-3, 3, 100)

    plt.plot(x, y, 'ro', ms=5)

    plt.plot(xs, spl(xs), 'g-', lw=3, label='LSQ spline')

    plt.plot(xs, spl_i(xs), 'b-', lw=3, alpha=0.7, label='interp spline')

    plt.legend(loc='best')

    plt.show()

# compare_naive_spline()
fit_spline()