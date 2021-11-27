import matplotlib.pyplot as plt
import numpy as np


def test_solve():
    import numpy as np
    A = np.array([[1, 2],
                  [4, 6],
                  [3, 4]], np.float32)
    u, s, vh = np.linalg.svd(A, full_matrices=True)
    # u[:, :2] @ np.diag(s) @ vh == A
    assert np.allclose(A, np.dot(u[:, :2] * s, vh))
    print(u.shape, s.shape, vh.shape)
    A_plus = vh.T @ np.diag(1/s) @ u[:, :2].T  # Pseudoinverse of A
    assert np.allclose(A_plus @ A, np.eye(2), atol=1e-5)


if __name__ == '__main__':
    test_solve()
