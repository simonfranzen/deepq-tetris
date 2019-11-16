import torch

class DQNN(torch.nn.Module):

    def __init__(self, input_size, output_size):
        super().__init__()

        self.layer1 = torch.nn.Linear(in_features=input_size, out_features=32)
        self.layer2 = torch.nn.Linear(in_features=32, out_features=32)
        self.out = torch.nn.Linear(in_features=32, out_features=output_size)

    def forward(self, tensor):
        tensor = torch.nn.functional.relu(self.layer1(tensor))
        tensor = torch.nn.functional.relu(self.layer2(tensor))
        tensor = self.out(tensor)
        return tensor

