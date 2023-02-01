import os
from molscore.tests.mock_generator import MockGenerator

test_files = {
    'GlideDock_grid': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'DRD2_6CM4_grid.zip'),
    'DRD2_receptor': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'DRD2_6CM4p_rec.pdb'),
    'DRD2_receptor_pdbqt': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'DRD2_6CM4p_rec.pdbqt'),
    'DRD2_ref_ligand': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'DRD2_risperidone.sdf')
}