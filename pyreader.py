import dearpygui.dearpygui as dpg

times = list()
analog = list()
digital = list()
with open('test.export', 'r') as data:
    for line in data:
        parse = line.strip().split(',')
        if parse[0] == 'T':
            times = [float(t) for t in parse[1:]]
        elif parse[0] == 'A':
            if parse[2] != '0':
                analog.append({
                    'name' : parse[1],
                    'channel' : int(parse[2]),
                    'data' : [{
                        'type' : n[0],
                        'val': float(n[1:])
                    } for n in parse[3:]]
                })
        elif parse[0] == 'D':
            if parse[2] != '0':
                digital.append({
                    'name' : parse[1],
                    'channel' : int(parse[2]),
                    'data' : [int(n) for n in parse[3:]]
                })
t_axis = [0.] * (len(times) + 1)
for i in range(1, len(times) + 1):
    t_axis[i] = round(t_axis[i-1] + times[i-1], 2)

# print(t_axis)
# print(analog)
# print(digital)
dpg.create_context()
dpg.create_viewport()

with dpg.window(tag='primary'):
    with dpg.plot(height=-1, width=-1):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label='Time (ms)')
        with dpg.plot_axis(dpg.mvYAxis, label="Value"):
            for item in digital:
                dpg.add_stair_series(t_axis, item['data'], label=f"{item['name']} | D{item['channel']}")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('primary', True)
dpg.start_dearpygui()
dpg.destroy_context()