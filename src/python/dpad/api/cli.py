import click
import json
import .api import DPAD,Config
from dxl.core.debug import enter_debug
from srf.external.stir.function import get_scanner

enter_debug()

@click.group()
@click.option('--config','-c',type=click.Path(exists=True))
def dpad(config):
    with open(config, 'r') as fin:
        task_config = json.load(fin)
        dp_config = Config(task_config['input']['num_file'],task_config['input']['path_file'],task_config['correction']['relationship_blockid'],
                task_config['correction']['relationship_crystalid'],task_config['correction']['time_period'],task_config['correction']['search_range'],
                task_config['correction']['energy_window'],task_config['correction']['time_window'],task_config['output']['path_file'])
        scanner = get_scanner(task_config['scanner'])
    DPAD(dp_config,scanner)


