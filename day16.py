""" Day 16 in the AoC house - Elephants and valves
time taken :
leaderboard

"""
from time import time

from anytree import AnyNode, AsciiStyle, RenderTree

from tools.common import file_to_list
from tools.graphing import dijkstra, powerset

stm = time()

lines = file_to_list("day16.txt")


class ValveNode(AnyNode):
    @property
    def name_amount(self):
        return f"{self.v} {self.cummulative_amount_released}"


class Valve:

    def __init__(self, name, rate, leads_to):
        self.name = name
        self.rate = int(rate)
        self.leads_to = {nxt: 1 for nxt in leads_to}
        self.targets = {}

    def __repr__(self):
        return f"{self.name}"


def parse_input():
    vs = {}
    for line in lines:
        v = line[6:8]
        r = line.split("=")
        r = r[1].split(";")[0]
        dst = line.split(",")
        dst[0] = dst[0][-2:]
        dst = [v.strip() for v in dst]
        vc = Valve(v, r, dst)
        vs[v] = vc
    return vs


def build_graph():
    """return a graph of all the valves"""
    graph = {}
    for valve in valves.values():
        graph[valve.name] = valve.leads_to
    return graph


def determine_targeted_valves():
    """ The target valves are the ones with > 0 rate, assess their distances from each other (inc AA)
    using dijkstra store them as a sub-graph in targets
    """
    for valve in non_zero_valves_and_AA:
        distances = dijkstra(valve_graph, valve.name)
        for target_key, distance in distances.items():
            if target_key in non_zero_valve_keys:
                valve.targets[target_key] = distance


valves = parse_input()
non_zero_valves = [v for v in valves.values() if v.rate > 0]
non_zero_valves_and_AA = [v for v in valves.values() if v.rate > 0]
non_zero_valves_and_AA.append(valves["AA"])
non_zero_valve_keys = [v.name for v in valves.values() if v.rate > 0]
valve_graph = build_graph()
determine_targeted_valves()

etm = time()
elapsed_time = etm - stm
print(f"Preparation - Execution time: {elapsed_time:0.4}s")


# we want to build a tree of paths/routes spanning the targets
# we can stop if we go over the allotted time period
# and discover the total amount released indicated on the leaf nodes
def add_child(current_node: ValveNode, allotted_time=30, subset=None):
    if subset is None:
        subset = set(non_zero_valve_keys)
    done = [node.valve.name for node in current_node.ancestors]  # the keys already seen
    for target_key, distance in current_node.valve.targets.items():
        if target_key not in done and target_key != current_node.valve.name and target_key in subset:
            valve = valves[target_key]
            time_switched_on = current_node.time_switched_on + distance + 1
            will_run_for = allotted_time - time_switched_on
            if will_run_for > 0:
                amount_released = valve.rate * will_run_for
                new_node = ValveNode(
                    valve=valve,
                    parent=current_node,
                    time_switched_on=time_switched_on,
                    cummulative_amount_released=current_node.cummulative_amount_released + amount_released
                )
                add_child(new_node, allotted_time=allotted_time, subset=subset)


root = ValveNode(valve=valves["AA"], time_switched_on=0, cummulative_amount_released=0)
add_child(root)
# print(RenderTree(root, style=AsciiStyle()).by_attr("name_amount"))
part_a = max([leaf.cummulative_amount_released for leaf in root.leaves])
# for part B it will be useful to know the optimal amount for any given set of targets
# best_amounts = {}
# for leaf in root.leaves:
#     valves_on_path = tuple(sorted([node.valve.name for node in leaf.ancestors if node.valve.name != "AA"]))
#     best_amount = best_amounts.get(valves_on_path, 0)
#     if leaf.cummulative_amount_released > best_amount:
#         best_amounts[valves_on_path] = leaf.cummulative_amount_released
print(f"A: {part_a}")

etm = time()
elapsed_time = etm - stm
print(f"Part A - Execution time: {elapsed_time:0.4}s")

#
# Part B
#
# create a power set of all the targets, but we only need up to half
# the other valve turner will take the compliment

all_valves_set = set(non_zero_valve_keys)
power_set = list(powerset(all_valves_set))
print(f"Size of power set: {len(power_set)}")
power_set = [s for s in power_set if len(s) <= len(all_valves_set) // 2]
print(f"Split 50/50: {len(power_set)}")

cnt = 0
res = []
for my_subset in power_set:
    cnt += 1
    if cnt % 100 == 0:
        etm = time()
        elapsed_time = etm - stm
        print(f"Progress: {cnt} time: {elapsed_time / 60} mins")

    my_subset = set(my_subset)
    e_subset = all_valves_set.difference(my_subset)  # the compliment

    my_root = ValveNode(valve=valves["AA"], time_switched_on=0, cummulative_amount_released=0)
    e_root = ValveNode(valve=valves["AA"], time_switched_on=0, cummulative_amount_released=0)

    add_child(my_root, subset=my_subset, allotted_time=26)
    add_child(e_root, subset=e_subset, allotted_time=26)

    my_max = max([leaf.cummulative_amount_released for leaf in my_root.leaves])
    e_max = max([leaf.cummulative_amount_released for leaf in e_root.leaves])
    the_max = my_max + e_max
    res.append(the_max)

part_b = max(res)
etm = time()
elapsed_time = etm - stm
print(f"Part B - Execution time: {elapsed_time / 60} mins")
print(f"B: {part_b}")

"""
Preparation - Execution time: 0.002995s
A: 1857
Part A - Execution time: 2.948s
Size of power set: 32768
Split 50/50: 16384
Progress: 100 time: 0.5919326464335124 mins
Progress: 200 time: 1.0060734709103902 mins
Progress: 300 time: 1.2840348760286966 mins
Progress: 400 time: 1.5955976009368897 mins
Progress: 500 time: 1.8951424876848857 mins
Progress: 600 time: 2.129690690835317 mins
Progress: 700 time: 2.3865097045898436 mins
Progress: 800 time: 2.6461474974950154 mins
Progress: 900 time: 2.8799284021059672 mins
Progress: 1000 time: 3.0767414887746174 mins
Progress: 1100 time: 3.218708407878876 mins
Progress: 1200 time: 3.3451145847638446 mins
Progress: 1300 time: 3.531795557339986 mins
Progress: 1400 time: 3.7349056283632915 mins
Progress: 1500 time: 3.9071831504503884 mins
Progress: 1600 time: 4.043002418677012 mins
Progress: 1700 time: 4.219713048140208 mins
Progress: 1800 time: 4.402484277884166 mins
Progress: 1900 time: 4.522988736629486 mins
Progress: 2000 time: 4.679506953557333 mins
Progress: 2100 time: 4.791323983669281 mins
Progress: 2200 time: 4.895382535457611 mins
Progress: 2300 time: 5.062952379385631 mins
Progress: 2400 time: 5.248430641492208 mins
Progress: 2500 time: 5.398135729630789 mins
Progress: 2600 time: 5.513216328620911 mins
Progress: 2700 time: 5.654313655694326 mins
Progress: 2800 time: 5.800730125109355 mins
Progress: 2900 time: 5.901313598950704 mins
Progress: 3000 time: 5.998262492815654 mins
Progress: 3100 time: 6.096138266722361 mins
Progress: 3200 time: 6.173858801523845 mins
Progress: 3300 time: 6.232561047871908 mins
Progress: 3400 time: 6.322156151135762 mins
Progress: 3500 time: 6.40965964794159 mins
Progress: 3600 time: 6.481941481431325 mins
Progress: 3700 time: 6.5639488657315574 mins
Progress: 3800 time: 6.662886385122935 mins
Progress: 3900 time: 6.784463814894358 mins
Progress: 4000 time: 6.911310092608134 mins
Progress: 4100 time: 7.007915492852529 mins
Progress: 4200 time: 7.1077775955200195 mins
Progress: 4300 time: 7.178253384431203 mins
Progress: 4400 time: 7.254107423623403 mins
Progress: 4500 time: 7.3335017442703245 mins
Progress: 4600 time: 7.438016871611278 mins
Progress: 4700 time: 7.5209612647692365 mins
Progress: 4800 time: 7.610235691070557 mins
Progress: 4900 time: 7.675230097770691 mins
Progress: 5000 time: 7.746425596872966 mins
Progress: 5100 time: 7.8372383197148645 mins
Progress: 5200 time: 7.901761249701182 mins
Progress: 5300 time: 7.949661366144816 mins
Progress: 5400 time: 8.019934483369191 mins
Progress: 5500 time: 8.085203019777934 mins
Progress: 5600 time: 8.140023454030354 mins
Progress: 5700 time: 8.210609412193298 mins
Progress: 5800 time: 8.311635728677114 mins
Progress: 5900 time: 8.423524530728658 mins
Progress: 6000 time: 8.528306519985199 mins
Progress: 6100 time: 8.617738779385885 mins
Progress: 6200 time: 8.708132588863373 mins
Progress: 6300 time: 8.769035291671752 mins
Progress: 6400 time: 8.83524449268977 mins
Progress: 6500 time: 8.898491048812867 mins
Progress: 6600 time: 8.984737650553386 mins
Progress: 6700 time: 9.047496132055919 mins
Progress: 6800 time: 9.120683598518372 mins
Progress: 6900 time: 9.17666213909785 mins
Progress: 7000 time: 9.230610740184783 mins
Progress: 7100 time: 9.276712083816529 mins
Progress: 7200 time: 9.335887165864309 mins
Progress: 7300 time: 9.394490532080333 mins
Progress: 7400 time: 9.433957091967265 mins
Progress: 7500 time: 9.480519354343414 mins
Progress: 7600 time: 9.517752675215403 mins
Progress: 7700 time: 9.55613145828247 mins
Progress: 7800 time: 9.598668396472931 mins
Progress: 7900 time: 9.664093832174936 mins
Progress: 8000 time: 9.708268785476685 mins
Progress: 8100 time: 9.763919480641682 mins
Progress: 8200 time: 9.799495041370392 mins
Progress: 8300 time: 9.850465786457061 mins
Progress: 8400 time: 9.907855808734894 mins
Progress: 8500 time: 9.962306221326193 mins
Progress: 8600 time: 10.024563606580099 mins
Progress: 8700 time: 10.093610219160716 mins
Progress: 8800 time: 10.149063014984131 mins
Progress: 8900 time: 10.222055832544962 mins
Progress: 9000 time: 10.264393746852875 mins
Progress: 9100 time: 10.319163223107656 mins
Progress: 9200 time: 10.360566627979278 mins
Progress: 9300 time: 10.402231860160828 mins
Progress: 9400 time: 10.450748483339945 mins
Progress: 9500 time: 10.489922861258188 mins
Progress: 9600 time: 10.55285305182139 mins
Progress: 9700 time: 10.596829724311828 mins
Progress: 9800 time: 10.640813807646433 mins
Progress: 9900 time: 10.687663833300272 mins
Progress: 10000 time: 10.727385532855987 mins
Progress: 10100 time: 10.770255577564239 mins
Progress: 10200 time: 10.8275008837382 mins
Progress: 10300 time: 10.876065214474997 mins
Progress: 10400 time: 10.915324409802755 mins
Progress: 10500 time: 10.955158483982085 mins
Progress: 10600 time: 10.985497105121613 mins
Progress: 10700 time: 11.018647094567617 mins
Progress: 10800 time: 11.05740423599879 mins
Progress: 10900 time: 11.10866727034251 mins
Progress: 11000 time: 11.149674848715465 mins
Progress: 11100 time: 11.189524845282238 mins
Progress: 11200 time: 11.220699445406597 mins
Progress: 11300 time: 11.26684267918269 mins
Progress: 11400 time: 11.32441931962967 mins
Progress: 11500 time: 11.384362256526947 mins
Progress: 11600 time: 11.445978752772014 mins
Progress: 11700 time: 11.51257800658544 mins
Progress: 11800 time: 11.564662834008535 mins
Progress: 11900 time: 11.626950736840566 mins
Progress: 12000 time: 11.67031033039093 mins
Progress: 12100 time: 11.71619524161021 mins
Progress: 12200 time: 11.750554172197978 mins
Progress: 12300 time: 11.786233460903167 mins
Progress: 12400 time: 11.83251114288966 mins
Progress: 12500 time: 11.869652386506399 mins
Progress: 12600 time: 11.91738603512446 mins
Progress: 12700 time: 11.955225662390392 mins
Progress: 12800 time: 11.990452122688293 mins
Progress: 12900 time: 12.02979673544566 mins
Progress: 13000 time: 12.06411959330241 mins
Progress: 13100 time: 12.094469551245371 mins
Progress: 13200 time: 12.127952321370442 mins
Progress: 13300 time: 12.165030932426452 mins
Progress: 13400 time: 12.206811761856079 mins
Progress: 13500 time: 12.238027302424113 mins
Progress: 13600 time: 12.271750048796337 mins
Progress: 13700 time: 12.303868774573008 mins
Progress: 13800 time: 12.33737136522929 mins
Progress: 13900 time: 12.37693183819453 mins
Progress: 14000 time: 12.410295748710633 mins
Progress: 14100 time: 12.44567909638087 mins
Progress: 14200 time: 12.48304616212845 mins
Progress: 14300 time: 12.534534462292989 mins
Progress: 14400 time: 12.583330317338307 mins
Progress: 14500 time: 12.625628403822581 mins
Progress: 14600 time: 12.661835753917694 mins
Progress: 14700 time: 12.699707027276357 mins
Progress: 14800 time: 12.742741628487904 mins
Progress: 14900 time: 12.776554918289184 mins
Progress: 15000 time: 12.814379839102427 mins
Progress: 15100 time: 12.853747069835663 mins
Progress: 15200 time: 12.892923386891683 mins
Progress: 15300 time: 12.936157329877217 mins
Progress: 15400 time: 12.965910907586416 mins
Progress: 15500 time: 13.003600164254506 mins
Progress: 15600 time: 13.036985731124878 mins
Progress: 15700 time: 13.072318482398988 mins
Progress: 15800 time: 13.109469099839528 mins
Progress: 15900 time: 13.14173686504364 mins
Progress: 16000 time: 13.178786861896516 mins
Progress: 16100 time: 13.21773105065028 mins
Progress: 16200 time: 13.26374176343282 mins
Progress: 16300 time: 13.29522674481074 mins
Part B - Execution time: 13.327540493011474 mins
B: 2536
"""