#!/bin/bash


## @brief This is an automatic scripts for running Icarus Verilog and recording the time and memory used.
# @param1 The script only have one parameter now, which is seen as a simple string and it will be attached in the result
# json as the "basic_info" item.
# There are also something you need to do:
# @ToDo: It is not a good option to just use a simple string to record the specific information of verilog file.

# Novel pattern of result file
#{
#  "info": {
#    "simulator": "all/iv/qs",
#    "subject": "amount/BW/N",
#    "value": 1
#    },
#  "compile_time": "0:00.18",
#  "compile_memory": "3704",
#  "simulate_time": "0:00.20",
#  "simulate_memory": "4268"
#}
# New command of generate json

simulator="$1"
subject="$2"
value="$3"


compile_command="iverilog -o ../outputs/temp/testbench.vvp ../outputs/temp/testbench.v ../outputs/temp/module.v"
run_command="vvp ../outputs/temp/testbench.vvp"
json_name="../outputs/result/result_${simulator}_${subject}_${value}.json"

prepare() {
    # 确保目录存在
    mkdir -p "../outputs/temp/"
    mkdir -p "../outputs/result/"

    # 检查module.v和testbench.v文件是否存在
    if [ ! -f "../outputs/temp/module.v" ]; then
        echo "Error: module.v does not exist in ../outputs/temp directory."
        exit 1
    fi

    if [ ! -f "../outputs/temp/testbench.v" ]; then
        echo "Error: testbench.v does not exist in ../outputs/temp directory."
        exit 1
    fi

    # 其他准备工作...
}

execute_command() {
    # 使用/usr/bin/time执行提供的命令，并将详细输出重定向到临时文件
    TEMP_FILE=$(mktemp)
    /usr/bin/time -v $compile_command &> "$TEMP_FILE"

    # 提取感兴趣的信息并保存到JSON文件
    compile_time=$(grep 'Elapsed (wall clock) time' "$TEMP_FILE" | awk '{print $NF}')
#    echo '------------------------------' "$compile_time"
    compile_memory=$(grep 'Maximum resident set size' "$TEMP_FILE" | awk '{print $NF}')

   # 提取并显示感兴趣的信息
    echo "=============================================================================="
    echo "Summary for command: compile"

    grep 'Elapsed (wall clock) time' "$TEMP_FILE"
    grep 'Maximum resident set size' "$TEMP_FILE"

    /usr/bin/time -v $run_command &> "$TEMP_FILE"

    # 提取感兴趣的信息并保存到JSON文件
    simulate_time=$(grep 'Elapsed (wall clock) time' "$TEMP_FILE" | awk '{print $NF}')
    simulate_memory=$(grep 'Maximum resident set size' "$TEMP_FILE" | awk '{print $NF}')

    # 提取并显示感兴趣的信息
    echo "Summary for command: run"
    grep 'Elapsed (wall clock) time' "$TEMP_FILE"
    grep 'Maximum resident set size' "$TEMP_FILE"

    echo "=============================================================================="
	

    jsonString=$(jq -n \
                      --arg simulator "$simulator" \
                      --arg subject "$subject" \
                      --arg value "$value" \
                      --arg compile_time "$compile_time" \
                      --arg compile_memory "$compile_memory" \
                      --arg simulate_time "$simulate_time" \
                      --arg simulate_memory "$simulate_memory" \
                      '{
                        info: {simulator: $simulator, subject: $subject, value: $value},
                        compile_time: $compile_time,
                        compile_memory: $compile_memory,
                        simulate_time: $simulate_time,
                        simulate_memory: $simulate_memory
                      }')

    echo "$jsonString" | jq '.' > "$json_name"
	echo "result name: $json_name"

    # 清理临时文件
    rm "$TEMP_FILE"
}

prepare "$@"
execute_command "$@"


