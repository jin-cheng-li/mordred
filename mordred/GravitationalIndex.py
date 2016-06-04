import numpy as np

from ._base import Descriptor
from ._graph_matrix import DistanceMatrix3D, AdjacencyMatrix
from ._util import atoms_to_numpy


__all__ = ('GravitationalIndex',)


class GravitationalIndex(Descriptor):
    @classmethod
    def preset(cls):
        return (
            cls(h, p)
            for p in [False, True]
            for h in [True, False]
        )

    require_3D = True

    @property
    def explicit_hydrogens(self):
        return not self._heavy

    def __str__(self):
        return 'GRAV{}{}'.format(
            '' if self._heavy else 'H',
            'p' if self._pair else '',
        )

    def as_key(self):
        return self.__class__, (self._heavy, self._pair)

    def __init__(self, heavy=True, pair=False):
        self._heavy = heavy
        self._pair = pair

    def dependencies(self):
        d = {'D': DistanceMatrix3D(self.explicit_hydrogens)}

        if self._pair:
            d['A'] = AdjacencyMatrix(self.explicit_hydrogens)

        return d

    def calculate(self, mol, conf, D, A=1.0):
        w = atoms_to_numpy(lambda a: a.GetMass(), mol)

        w = w[:, np.newaxis] * w
        np.fill_diagonal(w, 0)

        D = D.copy()
        np.fill_diagonal(D, 1)
        D[D == 0] = np.nan

        return 0.5 * np.sum(w * A / D ** 2)

    rtype = float