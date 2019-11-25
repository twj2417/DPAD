import click
import json
from .api import DPAD,Config
from dxl.core.debug import enter_debug
import srfnef as nef
# from srf.external.stir.function import get_scanner

enter_debug()

@click.command()
@click.option('--config','-c',type=click.Path(exists=True))
def dpad(config):
    with open(config, 'r') as fin:
        task_config = json.load(fin)
        dp_config = Config(task_config['input']['num_file'],task_config['input']['path_file'],task_config['correction']['relationship_blockid'],
                task_config['correction']['relationship_crystalid'],task_config['correction']['time_period'],task_config['correction']['search_range'],
                task_config['correction']['energy_window'],task_config['correction']['time_window'],task_config['output']['path_file'])
        block = nef.Block(task_config['scanner']['block']['size'],task_config['scanner']['block']['grid'])
        scanner = nef.PetEcatScanner(task_config['scanner']['ring']['inner_radius'],task_config['scanner']['ring']['outer_radius'],
                        task_config['scanner']['ring']['nb_rings'],task_config['scanner']['ring']['nb_blocks_per_ring'],
                        task_config['scanner']['ring']['gap'],block)
    DPAD(dp_config,scanner)


