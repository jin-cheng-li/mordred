import rdkit.Chem.GraphDescriptors as RDKit

from ._base import Descriptor
from ._graph_matrix import DistanceMatrix


__all__ = ('BertzCT',)


class BertzCT(Descriptor):
    r"""Bertz CT descriptor(rdkit wrapper)."""
    __slots__ = ()
    explicit_hydrogens = False

    @classmethod
    def preset(cls):
        yield cls()

    def __str__(self):
        return self.__class__.__name__

    def as_key(self):
        return self.__class__, ()

    def dependencies(self):
        return {'D': DistanceMatrix(self.explicit_hydrogens)}

    def calculate(self, D):
        return float(RDKit.BertzCT(self.mol, dMat=D))

    rtype = float
