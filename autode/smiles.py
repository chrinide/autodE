from rdkit import Chem
import rdkit.Chem.Descriptors
from rdkit.Chem import AllChem
from autode.log import logger
from autode.geom import are_coords_reasonable
from autode.exceptions import RDKitFailed
from autode.exceptions import BondsInSMILESAndGraphDontMatch
from autode.mol_graphs import make_graph
from autode.conformers.conf_gen import get_simanl_atoms
from autode.conformers.conformers import get_atoms_from_rdkit_mol_object
from autode.smiles_parser import SmilesParser


def calc_multiplicity(molecule, n_radical_electrons):
    """Calculate the spin multiplicity 2S + 1 where S is the number of unpaired electrons

    Arguments:
        molecule (autode.molecule.Molecule):
        n_radical_electrons (int):

    Returns:
        int: multiplicity of the molecule
    """

    if molecule.mult == 1 and n_radical_electrons == 0:
        return 1

    if molecule.mult == 1 and n_radical_electrons == 1:
        # Cannot have multiplicity = 1 and 1 radical electrons – override default multiplicity
        return 2

    if molecule.mult == 1 and n_radical_electrons > 1:
        logger.warning('Diradicals by default singlets. Set mol.mult if it\'s any different')
        return 1

    return molecule.mult


def init_organic_smiles(molecule, smiles):
    """
    Initialise a molecule from a SMILES string, set the charge, multiplicity (if it's not already specified) and the 3D
    geometry using RDKit

    Arguments:
        molecule (autode.molecule.Molecule):
        smiles (str): SMILES string
    """

    try:
        molecule.rdkit_mol_obj = Chem.MolFromSmiles(smiles)
        molecule.rdkit_mol_obj = Chem.AddHs(molecule.rdkit_mol_obj)
    except RuntimeError:
        raise RDKitFailed

    molecule.charge = Chem.GetFormalCharge(molecule.rdkit_mol_obj)
    molecule.mult = calc_multiplicity(molecule, rdkit.Chem.Descriptors.NumRadicalElectrons(molecule.rdkit_mol_obj))
    bonds = [(bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()) for bond in molecule.rdkit_mol_obj.GetBonds()]

    # Generate a single 3D structure using RDKit's ETKDG conformer generation algorithm
    AllChem.EmbedMultipleConfs(molecule.rdkit_mol_obj, numConfs=1, params=AllChem.ETKDGv2())
    molecule.set_atoms(atoms=get_atoms_from_rdkit_mol_object(molecule.rdkit_mol_obj, conf_id=0))

    if not are_coords_reasonable(coords=molecule.get_coordinates()):
        logger.warning('RDKit conformer was not reasonable')
        molecule.rdkit_conf_gen_is_fine = False

        make_graph(molecule, bond_list=bonds)
        molecule.set_atoms(atoms=get_simanl_atoms(molecule))

    # Ensure the SMILES string and the 3D structure have the same bonds
    make_graph(molecule)

    if len(molecule.rdkit_mol_obj.GetBonds()) != molecule.graph.number_of_edges():
        logger.error('Bonds and graph do no match')

    return None


def init_smiles(molecule, smiles):
    """
    Initialise a molecule from a SMILES string

    Arguments:
        molecule (autode.molecule.Molecule):
        smiles (str): SMILES string
    """

    # Assume that the RDKit conformer generation algorithm is not okay for metals
    molecule.rdkit_conf_gen_is_fine = False

    parser = SmilesParser()
    parser.parse_smiles(smiles)

    molecule.charge = parser.charge
    molecule.mult = calc_multiplicity(molecule=molecule, n_radical_electrons=parser.n_radical_electrons)

    molecule.set_atoms(atoms=parser.atoms)

    make_graph(molecule, bond_list=parser.bonds, ignore_invalid_valancies=False)
    molecule.set_atoms(atoms=get_simanl_atoms(molecule))

    # Ensure the SMILES string and the 3D structure have the same bonds
    make_graph(molecule, ignore_invalid_valancies=False)

    if len(parser.bonds) != molecule.graph.number_of_edges():
        logger.error('Bonds and graph do no match')

    return None
