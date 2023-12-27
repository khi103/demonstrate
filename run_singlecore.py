import os, datetime, time

##Run parameters
sim_title = "checkpoints_10B_runtest_100M"
##

gem5_root_dir = "/home/khi103/gem5/"
gem5_binary_file = gem5_root_dir+"build/X86/gem5.fast"
se_mode_config_file = gem5_root_dir+"configs/deprecated/example/se.py"
checkpoint_dir = "/home/shared/checkpoint_for_gem5/URP_10B/"

se_mode_config_1 = {
    "cpu-clock" : "3GHz",
    "sys-clock" : "1GHz",
    "cpu-type" : "TimingSimpleCPU",
    "mem-type" : "DDR4_2400_8x8",
    "mem-channels" : "1",
    "mem-size" : "16GB",
    "num-l2caches" : "1",
    "l1d_size" : "32kB",
    "l1i_size" : "32kB",
    "l1d_assoc" : "8",
    "l1i_assoc" : "8",
    "l2_size" : "2MB",
    "l2_assoc" : "16",
    "cacheline_size" : "64",
    #"maxinsts" : "90000000000", #10B
    "maxinsts" : "1000000000", #1B
    #"maxinsts" : "500000000", #500M
    #"maxinsts" : "100000000", #100M
    "checkpoint-restore" : "1", 
}
se_mode_config_2 = {
    "caches" : "",
    "l2cache" : "",
    #"checkpoint-at-end" : ""
}

spec2006_cmd = {
    #benchname, cmd, option, input
    "GemsFDTD" : ["./GemsFDTD", "", ""],
    "mcf" : ["./mcf", "inp.in", ""],
    "lbm" : ["./lbm","3000 reference.dat 0 0 100_100_130_ldc.of",""],
    #"leslie3d" : ["./leslie3d", "", "leslie3d.in"],
    #"zeusmp" : ["./zeusmp","",""],
    "libquantum" : ["./libquantum", "1397 8", ""]
}

graphbig_cmd = {
    #benchname, cmd, option, input
    "BFS" : ["/home/shared/benchmark/GraphBIG/benchmark/bench_BFS/bfs", "--dataset /home/shared/benchmark/GraphBIG/dataset/ldbc", ""],
    "DFS" : ["/home/shared/benchmark/GraphBIG/benchmark/bench_DFS/dfs", "--dataset /home/shared/benchmark/GraphBIG/dataset/ldbc", ""],
    "GC" : ["/home/shared/benchmark/GraphBIG/benchmark/bench_graphColoring/graphcoloring", "--dataset /home/shared/benchmark/GraphBIG/dataset/ldbc", ""],
}

now  = datetime.datetime.now()
try:
    os.makedirs(gem5_root_dir+"result/"+now.strftime("%Y_%m_%d")+"/"+sim_title)
except:
    print("[ERROR]: Exist directory : " + gem5_root_dir+now.strftime("%Y_%m_%d")+"/"+sim_title)
    exit()

output_dir = gem5_root_dir+"result/"+now.strftime("%Y_%m_%d")+"/"+sim_title
os.chdir("/home/shared/benchmark/SPEC2006/mix/")

for bench_name, bench_op in spec2006_cmd.items() :
    
    config_1 = ["--"+key+"="+value+" " for key, value in se_mode_config_1.items()]
    config_2 = ["--"+key+" " for key, value in se_mode_config_2.items()]
    config = ''.join(config_1) + ''.join(config_2)

    command_line = "nohup "+ gem5_binary_file + " " + \
                    "--outdir=" + output_dir + " " + \
                    "--stats-file=" + bench_name + ".result" + " " + \
                    se_mode_config_file + " " + \
                    config + \
                    "--checkpoint-dir=" + checkpoint_dir + bench_name + " " + \
                    "--cmd=\'" + bench_op[0] + "\' " + \
                    "--options=\'" + bench_op[1] + "\' " + \
                    "--input=\'" + bench_op[2] + "\' &"
    print(command_line)
    os.system(command_line)
    time.sleep(0.2)

for bench_name, bench_op in graphbig_cmd.items() :
    
    config_1 = ["--"+key+"="+value+" " for key, value in se_mode_config_1.items()]
    config_2 = ["--"+key+" " for key, value in se_mode_config_2.items()]
    config = ''.join(config_1) + ''.join(config_2)

    command_line = "nohup "+ gem5_binary_file + " " + \
                    "--outdir=" + output_dir + " " + \
                    "--stats-file=" + bench_name + ".result" + " " + \
                    se_mode_config_file + " " + \
                    config + \
                    "--checkpoint-dir=" + checkpoint_dir + bench_name + " " + \
                    "--cmd=\'" + bench_op[0] + "\' " + \
                    "--options=\'" + bench_op[1] + "\' " + \
                    "--input=\'" + bench_op[2] + "\' &"
    print(command_line)
    os.system(command_line)
    time.sleep(0.2)


