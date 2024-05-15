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
