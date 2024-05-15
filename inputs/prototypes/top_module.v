
`timescale 1ns / 1n

// 宏定义数据宽度和地址宽度

`define N 4 // 级联加法器的数量
`define ADDR_WIDTH 4
`define BW python-BW - 1

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

reg [`BW-1:0] adder_inputs[`N-1:0]; // 存储每个加法器的a输入
wire [`BW-1:0] adder_outputs[`N-1:0]; // 存储每个加法器的sum输出
wire [`BW-1:0] rom_outputs[`N-1:0]; // 存储从ROM读取的b输入

// 实例化ROM
rom #(
    .DATA_WIDTH(`BW),
    .ADDR_WIDTH(`ADDR_WIDTH)
) rom_instance (
    .clk(clk),
    .addr(0), // 这里需要一个逻辑来循环或递增地址
    .data_out(rom_outputs[0]) // 假设第一个加法器使用的ROM输出
);

genvar i;
generate
    for (i = 0; i < `N; i = i + 1) begin : adders
        // 第一个加法器的a输入可以是外部输入或固定值
        if (i == 0) assign adder_inputs[i] = 0; // 示例：将第一个加法器的a输入设置为0
        
        // 实例化加法器
        adder adder_instance(
            .clk(clk),
            .rst_n(rst_n),
            .a(adder_inputs[i]),
            .b(rom_outputs[i]), // 假设每个加法器都有唯一的ROM输出
            .sum(adder_outputs[i])
        );
        
        // 将当前加法器的输出连接到下一个加法器的输入
        if (i < `N - 1) assign adder_inputs[i + 1] = adder_outputs[i];
    end
endgenerate

endmodule