"""
Principle:
1. Change the Macro
2. Generate more module

ToDo:
    1. Cascade is better, if you want to use a large bit width.
    2. Find a more rational way to generate and connect modules.
"""
import json
import re


class Modifier:
    def __init__(self, logger, **kwargs):
        self.subject = None
        self.verilog_testbench = None
        self.verilog_module = None
        self.logger = logger
        self.prototype_testbench = None
        self.prototype_module = None
        self.prototype = None
        self.start = None
        self.step = None
        self.mode = None
        self.end = None
        self.amount = None
        self.BW = None
        self.N = None

        self.array = []
        self.index = 0

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.logger.info(f"\nconfiguration of Modifier class:{self.__dict__}")

        self.generate_array()
        self.check_subject()

    def check_subject(self):
        if self.N == -1:
            self.subject = 'N'
        elif self.BW == -1:
            self.subject = 'BW'
        elif self.amount == -1:
            self.subject = 'amount'

        self.logger.info(f"subject is:{self.subject}")

    def generate_array(self):
        """
        call when initialization
        :return:
        """
        self.array = [self.start]

        if self.mode == 'log':
            while self.array[-1] * self.step <= self.end:
                self.array.append(self.array[-1] * self.step)
        elif self.mode == 'linear':
            while self.array[-1] + self.step <= self.end:
                self.array.append(self.array[-1] + self.step)
        else:
            self.logger.error(f"mode {self.mode} is not supported. Please select 'log' or 'linear'.")

        self.logger.info(f"generated array is:{self.array}")
        self.index = len(self.array)
        self.logger.info(f"index is:{self.index}")

    def modify(self):
        self.logger.info(f"Modifying index is:{self.index}")
        self.load_prototype()
        self.modify_jsons()
        self.save_verilog()

        # 这里注意确认一下index的数值和array的长度是否一致
        self.index -= 1
        pass

    def modify_jsons(self):
        if self.subject == 'N':
            self.N = self.array[-self.index]
            self.replace()
        elif self.subject == 'amount':
            self.amount = self.array[-self.index]
            self.replace()
        elif self.subject == 'BW':
            self.BW = self.array[-self.index]
            self.replace()

        self.verilog_module = self.prototype_module
        self.verilog_testbench = self.prototype_testbench

    def replace(self):
        python_str = r'python-N'
        value = self.N
        self.prototype_testbench = re.sub(python_str, str(value), self.prototype_testbench)

        python_str = r'python-BW'
        value = self.BW
        self.prototype_module = re.sub(python_str, str(value), self.prototype_module)
        self.prototype_testbench = re.sub(python_str, str(value), self.prototype_testbench)

        python_str = r'python-amount'
        value = self.amount
        self.prototype_module = re.sub(python_str, str(value), self.prototype_module)

    def save_verilog(self):
        save_path = "../outputs/temp/module.v"
        with open(save_path, 'w') as f:
            f.write(self.verilog_module)
        with open("../outputs/temp/testbench.v", 'w') as f:
            f.write(self.verilog_testbench)

    def load_prototype(self):
        modulename = "../inputs/prototypes/" + self.prototype + '_module.json'
        testbench_name = "../inputs/prototypes/" + self.prototype + '_testbench.json'
        with open(modulename, 'r') as f:
            self.prototype_module = json.load(f)
        with open(testbench_name, 'r') as f:
            self.prototype_testbench = json.load(f)

        if self.prototype_module is not None:
            self.logger.info(f"loading prototype:{modulename}")
        if self.prototype_testbench is not None:
            self.logger.info(f"loading prototype:{testbench_name}")
        pass


# This is an example of how to generate a prototype json file by a verilog.
if __name__ == "__main__":
    testbench = """
`timescale 1ns / 1ns

`define BW python-BW - 1 
`define N python-N

module top_tb;

// 参数定义
localparam BW = `BW;
localparam N = `N;

// 测试信号
reg clk;
reg rst_n;
wire [BW-1:0] adder_outputs[N-1:0];

// 实例化被测试模块
top top_instance (
    .clk(clk),
    .rst_n(rst_n)
);

// 时钟生成
initial begin
    clk = 0;
    forever #5 clk = ~clk; // 产生一个周期为10ns的时钟信号
end

// 测试初始化和复位
initial begin
    // 初始化复位信号
    rst_n = 0;
    #20; // 等待一段时间后释放复位
    rst_n = 1;
end

// 初始化ROM内容
initial begin
    $readmemb("rom_data.txt", top_instance.rom_instance.mem); // 从文件加载ROM内容
end

initial begin
    $dumpfile("top_tb.vcd"); // 指定VCD文件名
    $dumpvars(0, top_tb); // 记录所有信号
end

// 测试结束条件（可选）
initial begin
    #N; // 运行一段时间后结束测试
    $finish;
end

endmodule
"""
    module = """

`timescale 1ns / 1ns

// 宏定义数据宽度和地址宽度

`define AMOUNT python-amount // 级联加法器的数量
`define ADDR_WIDTH 4// 地址宽度
`define BW  python-BW - 1 // 级联加法器的位宽

module adder(
    input clk, // 加入时钟信号
    input rst_n, // 复位信号，低电平有效
    input [`BW - 1:0] a,
    input [`BW - 1:0] b,
    output reg [`BW - 1:0] sum // 声明为 reg 类型以在 always 块中赋值
);

    // 使用时钟边沿和复位信号控制逻辑
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) // 如果复位信号为低电平，则重置 sum
            sum <= 0;
        else
            sum <= a + b; // 在时钟上升沿更新 sum
    end

endmodule   


module rom #(
    parameter DATA_WIDTH = `BW, // 使用宏定义的数据位宽
    parameter ADDR_WIDTH = `ADDR_WIDTH  // 使用宏定义的地址位宽，决定了ROM的大小
)(
    input wire clk, // 时钟信号
    input wire [ADDR_WIDTH-1:0] addr, // 地址线
    output reg [DATA_WIDTH-1:0] data_out // 读出的数据
);

// ROM存储器数组
// 注意：实际ROM的内容需要预先定义或通过初始块进行初始化
reg [DATA_WIDTH-1:0] mem [(2**ADDR_WIDTH)-1:0];

// 同步读操作
always @(posedge clk) begin
    data_out <= mem[addr]; // 在时钟上升沿读取数据
end

// 可选：初始化ROM内容
// initial begin
//     // 初始化代码，例如：mem[0] = 8'hFF;
// end

endmodule


module top(
    input clk,
    input rst_n
);

wire [`BW-1:0] adder_inputs[`AMOUNT-1:0]; // 存储每个加法器的a输入
wire [`BW-1:0] adder_outputs[`AMOUNT-1:0]; // 存储每个加法器的sum输出
wire [`BW-1:0] rom_outputs; // 存储从ROM读取的b输入

// 实例化ROM
rom #(
    .DATA_WIDTH(`BW),
    .ADDR_WIDTH(`ADDR_WIDTH)
) rom_instance (
    .clk(clk),
    .addr(0), // 这里需要一个逻辑来循环或递增地址
    .data_out(rom_outputs) // 假设第一个加法器使用的ROM输出
);

genvar i;
generate
    for (i = 0; i < `AMOUNT; i = i + 1) begin : adders
        // 第一个加法器的a输入可以是外部输入或固定值
        if (i == 0) assign adder_inputs[i] = adder_inputs[`AMOUNT-1]; // 示例：将第一个加法器的a输入设置为0
        
        // 实例化加法器
        adder adder_instance(
            .clk(clk),
            .rst_n(rst_n),
            .a(adder_inputs[i]),
            .b(rom_outputs),
            .sum(adder_outputs[i])
        );
        
        // 将当前加法器的输出连接到下一个加法器的输入
        if (i < `AMOUNT - 1) assign adder_inputs[i + 1] = adder_outputs[i];
    end
endgenerate

endmodule
"""
    with open("../inputs/prototypes/adder_module.json", 'w') as f:
        json.dump(module, open("../inputs/prototypes/adder_module.json", 'w'))
    with open("../inputs/prototypes/adder_testbench.json", 'w') as f:
        json.dump(testbench, open("../inputs/prototypes/adder_testbench.json", 'w'))

    with open("../inputs/prototypes/adder_testbench.json", 'r') as f:
        load = json.load(f)
        print(load)
    with open("./test.v", 'w') as f:
        f.write(load)
