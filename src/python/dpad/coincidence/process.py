from .base import Coincidence_events
from ..correction.actual2theroy import Single_event

def coincidence_with_time_window(data:Single_event,time_window)->Coincidence_events:
    diff_time = data.time[1:] - data.time[:(data.size-1)]
    index = np.where(diff_time<time_window)[0]
    coincidence_events = []
    if (data.blockid[index[0]]!=data.blockid[index[0]+1]):
        coincidence_events.append(np.array([data.blockid[index[0]],data.crystalid[index[0]],data.energy[index[0]]
                                            data.blockid[index[0]+1],data.crystalid[index[0]+1],data.energy[index[0]+1]))
    for i in range(1,index.size):
        if abs(data.blockid[index[i]]-data.blockid[index[i]+1])>1 and index[i]!=index[i-1]+1:
            coincidence_events.append(np.array([data.blockid[index[i]],data.crystalid[index[i]],data.energy[index[i]]
                                            data.blockid[index[i]+1],data.crystalid[index[i]+1],data.energy[index[i]+1]))
    events = np.array(coincidence_events)
    return Coincidence_events(time_window,events[:,0],events[:,1],events[:,2],events[:,3],events[:,4],events[:,5])


