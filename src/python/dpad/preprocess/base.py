# from doufo import dataclass,List


class Carriage_data:
    def __init__(self,data):
        self.data = data

    @property
    def data_shape(self):
        return int(self.data.shape[0])

    @property
    def num_frame(self):
        return self.data[self.data_shape-1,1]

    @property
    def carriage_id(self):
        return self.data[self.data_shape-1,2]

    def extract_effective_data(self):
        return self.data[:self.num_frame,:]
   
    # def extract_effective_data(self):
    #     effective_data = self.data[:self.num_frame,:]
    #     check_bit = effective_data[:,3]
    #     d_value = check_bit[1:]+check_bit[:check_bit.size-1]
    #     index1 = np.where(d_value==284)[0]
    #     np.delete(effective_data,index1)
    #     index2 = np.where(d_value==286)[0]
    #     return np.delete(effective_data,index2+1)


# class Train_data:
#     def __init__(self,headstock,data:List[Carriage_data],carriage_tail,carriage_tail):
#         self.headstock = headstock
#         self.data = data
#         self.tail = tail

#     @property
#     def train_id(self):
#         return headstock

#     @property
#     def 



