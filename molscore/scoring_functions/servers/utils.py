import os
from typing import Union, List, Dict, Any
import numpy as np
from rdkit.Chem import AllChem as Chem
from rdkit.Chem import rdMolDescriptors, rdmolops, DataStructs
from rdkit.Chem.Pharm2D import Generate, Gobbi_Pharm2D
from rdkit.Avalon import pyAvalonTools

def get_mol(mol: Union[str, Chem.rdchem.Mol]):
    """
    Get RDkit mol
    :param mol:
    :return: RDKit Mol
    """
    if isinstance(mol, str):
        mol = Chem.MolFromSmiles(mol)
    elif isinstance(mol, Chem.rdchem.Mol):
        pass
    else:
        raise TypeError("Molecule is not a string (SMILES) or rdkit.mol")

    if not mol:
        mol = None

    return mol


def read_mol(mol_path: os.PathLike, i=0):
    if mol_path.endswith('.mol2') or mol_path.endswith('.mol'):
        mol = Chem.MolFromMolFile(mol_path, sanitize=False, strictParsing=False)

    elif mol_path.endswith('.sdf'):
        suppl = Chem.ForwardSDMolSupplier(mol_path, sanitize=False)
        for i, mol in enumerate(suppl):
            if i == i:
                break

    elif mol_path.endswith('.pdb'):
        mol = Chem.MolFromPDBFile(mol_path, sanitize=False)

    else:
        raise TypeError(f"Cannot read molecule, unknown input file type: {mol_path}")
    
    return mol


class Fingerprints:
    """
    Class to organise Fingerprint generation
    """

    @staticmethod
    def get(mol: Union[str, Chem.rdchem.Mol], name: str, nBits: int, asarray: bool = False):
        """
        Get fp by str instead of method
        :param mol: RDKit mol or Smiles
        :param name: Name of FP [ECFP4, ECFP4c, FCFP4, FCFP4c, ECFP6, ECFP6c, FCFP6, FCFP6c, Avalon, MACCSkeys, AP, hashAP, hashTT, RDK5, RDK6, RDK7, PHCO]
        :param nBits: Number of bits
        :return:
        """
        mol = get_mol(mol)
        generator = getattr(Fingerprints, name, None)

        if generator is None:
            raise KeyError(f"\'{name}\' not recognised as a valid fingerprint")

        if mol is not None:
            return generator(mol, nBits, asarray)

    # Circular fingerprints
    @staticmethod
    def ECFP4(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=nBits))
        else:
            return rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=nBits)

    @staticmethod
    def ECFP4c(mol, nBits, asarray):
        if asarray:
            fp = rdMolDescriptors.GetMorganFingerprint(mol, radius=2, useCounts=True)
            nfp = np.zeros((1, nBits), np.int32)
            for idx, v in fp.GetNonzeroElements().items():
                nidx = idx % nBits
                nfp[0, nidx] += int(v)
            return nfp.reshape(-1)
        else:
            return rdMolDescriptors.GetMorganFingerprint(mol, radius=2, useCounts=True)

    @staticmethod
    def FCFP4(mol, nBits, asarray):
        if asarray:
            np.asarray(rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=nBits, useFeatures=True))
        else:
            return rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=nBits, useFeatures=True)

    @staticmethod
    def FCFP4c(mol, nBits, asarray):
        if asarray:
            fp = rdMolDescriptors.GetMorganFingerprint(mol, radius=2, useCounts=True, useFeatures=True)
            nfp = np.zeros((1, nBits), np.int32)
            for idx, v in fp.GetNonzeroElements().items():
                nidx = idx % nBits
                nfp[0, nidx] += int(v)
            return nfp.reshape(-1)
        else:
            return rdMolDescriptors.GetMorganFingerprint(mol, radius=2, useCounts=True, useFeatures=True)

    @staticmethod
    def ECFP6(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=nBits))
        else:
            return rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=nBits)

    @staticmethod
    def ECFP6c(mol, nBits, asarray):
        if asarray:
            fp = rdMolDescriptors.GetMorganFingerprint(mol, radius=3, useCounts=True)
            nfp = np.zeros((1, nBits), np.int32)
            for idx, v in fp.GetNonzeroElements().items():
                nidx = idx % nBits
                nfp[0, nidx] += int(v)
            return nfp.reshape(-1)
        else:
            return rdMolDescriptors.GetMorganFingerprint(mol, radius=3, useCounts=True)

    @staticmethod
    def FCFP6(mol, nBits, asarray):
        if asarray:
            np.asarray(rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=nBits, useFeatures=True))
        else:
            return rdMolDescriptors.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=nBits, useFeatures=True)

    @staticmethod
    def FCFP6c(mol, nBits, asarray):
        if asarray:
            fp = rdMolDescriptors.GetMorganFingerprint(mol, radius=3, useCounts=True, useFeatures=True)
            nfp = np.zeros((1, nBits), np.int32)
            for idx, v in fp.GetNonzeroElements().items():
                nidx = idx % nBits
                nfp[0, nidx] += int(v)
            return nfp.reshape(-1)
        else:
            return rdMolDescriptors.GetMorganFingerprint(mol, radius=3, useCounts=True, useFeatures=True)

    # Substructure fingerprints
    @staticmethod
    def Avalon(mol, nBits, asarray):
        if asarray:
            return np.asarray(pyAvalonTools.GetAvalonFP(mol, nBits=nBits))
        else:
            return pyAvalonTools.GetAvalonFP(mol, nBits=nBits)

    @staticmethod
    def MACCSkeys(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdMolDescriptors.GetMACCSKeysFingerprint(mol))
        else:
            return rdMolDescriptors.GetMACCSKeysFingerprint(mol)

    # Path-based fingerprints
    @staticmethod
    def AP(mol, nBits, asarray):
        if asarray:
            fp = rdMolDescriptors.GetAtomPairFingerprint(mol, maxLength=10)
            nfp = np.zeros((1, nBits), np.int32)
            for idx, v in fp.GetNonzeroElements().items():
                nidx = idx % nBits
                nfp[0, nidx] += int(v)
            return nfp.reshape(-1)
        else:
            return rdMolDescriptors.GetAtomPairFingerprint(mol, maxLength=10)

    @staticmethod
    def hashAP(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdMolDescriptors.GetHashedAtomPairFingerprintAsBitVect(mol, nBits=nBits))
        else:
            return rdMolDescriptors.GetHashedAtomPairFingerprintAsBitVect(mol, nBits=nBits)

    @staticmethod
    def hashTT(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdMolDescriptors.GetHashedTopologicalTorsionFingerprintAsBitVect(mol, nBits=nBits))
        else:
            return rdMolDescriptors.GetHashedTopologicalTorsionFingerprintAsBitVect(mol, nBits=nBits)

    @staticmethod
    def RDK5(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdmolops.RDKFingerprint(mol, maxPath=5, fpSize=nBits, nBitsPerHash=2))
        else:
            return rdmolops.RDKFingerprint(mol, maxPath=5, fpSize=nBits, nBitsPerHash=2)

    @staticmethod
    def RDK6(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdmolops.RDKFingerprint(mol, maxPath=6, fpSize=nBits, nBitsPerHash=2))
        else:
            return rdmolops.RDKFingerprint(mol, maxPath=6, fpSize=nBits, nBitsPerHash=2)

    @staticmethod
    def RDK7(mol, nBits, asarray):
        if asarray:
            return np.asarray(rdmolops.RDKFingerprint(mol, maxPath=7, fpSize=nBits, nBitsPerHash=2))
        else:
            return rdmolops.RDKFingerprint(mol, maxPath=7, fpSize=nBits, nBitsPerHash=2)

    # Pharmacophore-based
    @staticmethod
    def PHCO(mol, nBits, asarray):
        if asarray:
            return np.asarray(Generate.Gen2DFingerprint(mol, Gobbi_Pharm2D.factory))
        else:
            return Generate.Gen2DFingerprint(mol, Gobbi_Pharm2D.factory)