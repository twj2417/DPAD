from io import load_data,is_file_normal
from ..preprocess.process import split_data_into_module
from ..correction.process import module_correction,single_correction
from ..coincidence.process import coincidence_with_time_window
from srf.io.listmode import save_h5
from ..auxiliary import hadd_by_row

class DPAD():
    def __init__(self,task_config):
        self.task = self._make_task(task_config)

    def _make_task(self,config):
        num_file = config['num_file']
        num_module = config['scanner']['num_block']
        relation_moduleid = np.array(config['module_relation'])
        relation_crystalid = np.array(config['crystal_relation'])
        const = config['const']
        search_range = config['search_range']
        block_grid = np.array(config['block_grid'])
        time_window = config['time_window']
        energy_window = np.array(config['energy_window'])
        file_path = config['input_path']
        out_path = config['output_path']
        coordinate = []
        for i in range(num_file):
            file_name = file_path+i+'.dat'
            if is_file_normal(file_name):
                input_data = np.array(load_data(file_name))
                module_data = split_data_into_module(input_data,num_module)
                corrected_module_data = module_correction(module_data,num_module,relation_moduleid,relation_crystalid)
                corrected_single_data = single_correction(corrected_module_data,num_module,const,search_range,block_grid)
                coincidence_data = coincidence_with_time_window(corrected_single_data,time_window)
                coordinate.append(coincidence_data)
        coordinate = hadd_by_row(coordinate)
        output = {'fst':coordinate[:,:3],'snd':coordinate[:,3:6],
                  'weight':np.ones_like(coordinate[:,0]),
                  'tof':np.ones_like(coordinate[:,0])}
        save_h5(out_path,output)
                        