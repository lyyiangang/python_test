# 参考: https://nb.bohrium.dp.tech/detail/2247212868?utm_source=zhihu
# https://zhuanlan.zhihu.com/p/340228853
# https://github.com/lyyiangang/mshadow
# https://github.com/lyyiangang/simple-tensor/tree/main
import numpy as np

# strides[i] = dim[i+1] * dim[i + 2] * ... dim[-1]
# strides[i+1] = dim[i+2]*dim[i+3] *...*dim[-1]
# --> strides[i] = dim[i+1] *  strides[i + 1]

# class Tensor:
#     def __init__(self, arr, dims):
#         assert len(dims) >= 1
#         self.size = dims
#         self.data = arr
#         n_dims = len(dims)
#         self.strides = [None] * n_dims
#         for idx in range(n_dims - 1, -1, -1):
#             if idx == n_dims - 1:
#                 self.strides[idx] = 1
#             else:
#                 self.strides[idx] = self.size[idx + 1]  * self.strides[idx + 1]
class Tensor():
    def __init__(
        self,
        data: list, 
        size: list,
        offset: int,
    ):
        self.data = data #tensor.data
        self.size = size #tensor.size
        self.ndim = len(size) #tensor.ndim
        self.offset = offset #tensor.offset
        # strides[i] = dim[i+1] * dim[i + 2] * ... dim[-1]. dim[-1] = 1;
        # strides[i+1] = dim[i+2]*dim[i+3] *...*dim[-1]
        # --> strides[i] = dim[i+1] *  strides[i + 1]

        my_strides = [None] * self.ndim
        for idx in range(self.ndim - 1, -1, -1):
            if idx == self.ndim - 1:
                my_strides[idx] = 1
            else:
                my_strides[idx] = self.size[idx + 1] * my_strides[idx + 1]
        self.stride = my_strides
    
    def __getitem__(
        self,
        key,
    ):
        assert len(key) == self.ndim, f"The length of key must be {self.ndim}"
        offset = self.offset
        for i in range(self.ndim):
            if (key[i]>=self.size[i]):
                raise RuntimeError("index out of range")
            offset += key[i] * self.stride[i]
        return self.data[offset]
    
    # 下面的代码是为了展示这个Tensor，大家不用看
    def __str__(
        self,
    ):
        def list_to_tensor(
            lst: list, 
            size: list,
            stride: list,
            offset: int,
        ):
            if len(size) == 0:
                return lst[offset]
            else:
                tmp = []
                for i in range(size[0]):
                    new_offset = offset + stride[0] * i
                    tmp.append(list_to_tensor(lst, size[1:],stride[1:],new_offset))           
                return tmp
        result = list_to_tensor(self.data, self.size, self.stride, 0)
        str_result = list(" "+str(result))
        for ii,char in enumerate(str_result):
            if char==',' and str_result[ii-1]==']' and str_result[ii-2]==']':
                str_result.insert(ii+1,'\n  ')
            elif char==',' and str_result[ii-1]==']':
                str_result.insert(ii+1,'\n   ')
        result = ''.join(str_result)
        return result



def transpose(
    tensor: Tensor,
    dim0: int,
    dim1: int,
):
    new_tensor = Tensor(tensor.data.copy(), tensor.size.copy(), tensor.offset)
    new_tensor.size[dim0], new_tensor.size[dim1] = new_tensor.size[dim1], new_tensor.size[dim0]
    new_tensor.stride[dim0], new_tensor.stride[dim1] = new_tensor.stride[dim1], new_tensor.stride[dim0]
    return new_tensor

def permute(
    tensor: Tensor,
    dims: tuple,
):
    assert len(dims) == len(tensor.size)
    new_size = []
    new_stride = []
    for cur_dim in dims:
        new_size.append(tensor.size[cur_dim])
        new_stride.append(tensor.stride[cur_dim])
    new_tensor = Tensor(tensor.data.copy(), tensor.size.copy(), tensor.offset)
    new_tensor.size = new_size.copy()
    new_tensor.stride = new_stride.copy()
    return new_tensor

def view(
    tensor: Tensor,
    new_size: list,
):
    new_tensor = Tensor(tensor.data.copy(),new_size.copy(),tensor.offset)
    return new_tensor

def is_contiguous(tensor: Tensor):
    stride = 1
    for i in range(tensor.ndim):
        if tensor.stride[tensor.ndim-1-i] != stride:
            return False
        stride *= tensor.size[tensor.ndim-1-i]
    return True

def test():
    data = [pow(i,2) for i in list(range(24))]
    size = [2,3,4]
    tensor = Tensor(data,size,offset=0)
    print("This tensor is:\n",tensor)
    print("tensor[1,1,1]: ",tensor[1,1,1])
    print("tensor[1,2,3]: ",tensor[1,2,3])
    #-------------transpose
    data = [pow(i,2) for i in list(range(24))]
    size = [2,3,4]
    tensor = Tensor(data,size,offset=0)
    print("This tensor is:\n",tensor)
    new_tensor = transpose(tensor, 1,2)
    print("After transpose dim1 and dim2，new_tensor is:\n",new_tensor)
    #---------------permute
    import torch
    data = [pow(i,2) for i in list(range(24))]
    size = [2,3,4]
    tensor = Tensor(data,size,offset=0)
    print("This tensor is:\n",tensor)
    new_tensor = permute(tensor, (1,2,0))
    print("After permute (1,2,0)，new_tensor is:\n",new_tensor)

    torch_tensor = torch.Tensor(data).reshape(2,3,4)
    print("Torch's tensor is:\n",torch_tensor)
    torch_new_tensor = torch.permute(torch_tensor, (1,2,0))
    print("After permute (1,2,0)，torch's new_tensor is:\n",torch_new_tensor)

    #----------------view
    data = [pow(i,2) for i in list(range(24))]
    size = [2,3,4]
    tensor = Tensor(data,size,offset=0)
    print("This tensor is:\n",tensor)
    new_tensor = view(tensor,[4,3,2])
    print("After view to (4,3,2):\n",new_tensor)

    torch_tensor = torch.Tensor(data).reshape(2,3,4)
    print("Torch's tensor is:\n",torch_tensor)
    torch_new_tensor =torch_tensor.view([4,3,2])
    print("(torch)After view to (4,3,2):\n",torch_new_tensor)

    #----------------contiguous
    data = [pow(i,2) for i in list(range(24))]
    size = [2,3,4]
    tensor = Tensor(data,size,offset=0)
    contiguous = is_contiguous(tensor)
    print("Contiguous of tensor(before transpose) is: ",contiguous)
    new_tensor = transpose(tensor, 1, 2)
    contiguous = is_contiguous(new_tensor)
    print("Contiguous of tensor(after transpose) is: ",contiguous)

if __name__ == '__main__':
    test()