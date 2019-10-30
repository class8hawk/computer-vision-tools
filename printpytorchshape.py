from model.LPRNet import build_lprnet
from torchsummary import summary
from data.load_data import CHARS
import torch


lprnet = build_lprnet(lpr_max_len=8, phase=False, class_num=len(CHARS), dropout_rate=0.5)
#device = t    device = torch.device("cuda:0" if args.cuda else "cpu")
device = torch.device("cuda:0")
lprnet.to(device)

summary(lprnet,(3,24,94))
