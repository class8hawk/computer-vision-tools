import io
import numpy as np
import onnx
import onnxruntime
import cv2


from torch import nn
import torch.utils.model_zoo as model_zoo
import torch.onnx
import torch.nn as nn
import torch.nn.init as init

from model.LPRNet import build_lprnet
from data.load_data import CHARS



model_name='weights/LPRNet__iteration_2000.pth'
batch_size = 1

lprnet = build_lprnet(lpr_max_len=8, phase=False, class_num=len(CHARS), dropout_rate=0.5)
#device = t    device = torch.device("cuda:0" if args.cuda else "cpu")
device = torch.device("cpu")
lprnet.to(device)

lprnet.load_state_dict(torch.load(model_name))

lprnet.eval()
images = np.array([])
img = cv2.imread("onnx2caffe/test.jpg")
print(img)

img = img.astype('float32')
img -= 127.5
img *= 0.0078125
img = np.transpose(img, (2, 0, 1))
img = img.reshape(batch_size, 3, 24, 94)



x = torch.from_numpy(img)
#x = torch.randn(batch_size, 3,24,94, requires_grad=True)
#x = torch.randn(batch_size, 3,24,94, requires_grad=True)


print(" ")
print(x)
torch_out = lprnet(x)

#print(lprnet.features[0])

print(torch_out)
print(torch_out.shape)

torch.onnx.export(lprnet,               # model being run
                  x,                         # model input (or a tuple for multiple inputs)
                  "lprnet.onnx",   # where to save the model (can be a file or file-like object)
                  export_params=True,        # store the trained parameter weights inside the model file
                  input_names = ['input'],   # the model's input names
                  output_names = ['output'], # the model's output names
                 )


onnx_model = onnx.load("lprnet.onnx")
onnx.checker.check_model(onnx_model)

ort_session = onnxruntime.InferenceSession("lprnet.onnx")

def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

# compute ONNX Runtime output prediction

ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(x)}

ort_outs = ort_session.run(None, ort_inputs)
print(ort_outs)
print(len(ort_outs[0][0]),len(ort_outs[0][0][0]))
# compare ONNX Runtime and PyTorch results
np.testing.assert_allclose(to_numpy(torch_out), ort_outs[0], rtol=1e-03, atol=1e-05)
'''
print("Exported model has been tested with ONNXRuntime, and the result looks good!")
'''





