from copy import deepcopy
from pathlib import Path
from enum import Enum
from typing import Callable, Optional

import ovito
from ovito.modifiers import PolyhedralTemplateMatchingModifier, ExpressionSelectionModifier, ClusterAnalysisModifier, WrapPeriodicImagesModifier, DeleteSelectedModifier


class DefectType(Enum):

    VACANCY = 1
    SELF_INTERSTITIAL = 2


def add_particles_in_clusters(num_clusters: int = 1) -> Callable:

    def wrapper(frame: int, data: ovito.data.DataCollection) -> None:

        centers_of_mass = data.tables['clusters']['Center of Mass'][...][:num_clusters]
        for center_of_mass in centers_of_mass:
            data.particles_.add_particle(center_of_mass)

    return wrapper


def select_n_closest(particle_index: int, n: int) -> Callable:

    def wrapper(frame: int, data: ovito.data.DataCollection) -> None:

        selection = data.particles_.create_property('Selection', data=None)
        finder = ovito.data.NearestNeighborFinder(n, data)

        for neigh in finder.find(particle_index):
            selection[neigh.index] = 1

    return wrapper


def add_point_defect(pipeline: ovito.pipeline.Pipeline, rmsd_cutoff: float) -> ovito.pipeline.Pipeline:

    p = deepcopy(pipeline)
    p.modifiers.append(PolyhedralTemplateMatchingModifier(rmsd_cutoff=rmsd_cutoff))
    p.modifiers.append(ExpressionSelectionModifier(expression="StructureType==0"))
    p.modifiers.append(ClusterAnalysisModifier(only_selected=True, sort_by_size=True, compute_com=True))
    p.modifiers.append(add_particles_in_clusters())
    p.modifiers.append(WrapPeriodicImagesModifier())

    return p


def new_run(input_path: Path, output_path: Path, defect: DefectType, rmsd_cutoff: float, export_kwargs: Optional[dict] = None) -> None:

    if not export_kwargs:
        export_kwargs = {
            'format': 'lammps/dump',
            'columns': [
                'Particle Identifier',
                'Particle Type',
                'Position.X',
                'Position.Y',
                'Position.Z'
            ]
        }

    pipeline = ovito.io.import_file(input_path)
    pipeline = add_point_defect(pipeline, rmsd_cutoff)

    # need to delete two particles closest to defect if self-interstitial
    if defect == DefectType.VACANCY:
        pass
    elif defect == DefectType.SELF_INTERSTITIAL:
        pipeline.modifiers.append(select_n_closest(particle_index=0, n=2))
        pipeline.modifiers.append(DeleteSelectedModifier())
    else:
        raise ValueError("invalid defect type")

    ovito.io.export_file(pipeline, output_path, multiple_frames=True, **export_kwargs)
