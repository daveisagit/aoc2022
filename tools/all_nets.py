import pickle



# all_nets = nets_of_size(10)
# with open(f"all_nets_10", "wb+") as f:
#     pickle.dump(all_nets, f)
from tools.nominoes import cube_net, draw_net

with open(f"all_nets_10", "rb") as f:
    all_nets = pickle.load(f)

net = all_nets[99]
cub = cube_net(net)
draw_net(net)
draw_net(cub)

