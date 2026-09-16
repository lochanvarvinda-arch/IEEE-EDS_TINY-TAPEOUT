# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    dut._log.info("Reset")
    await ClockCycles(dut.clk, 2)

    assert dut.uo_out.value == 0

    dut.rst_n.value = 1

    dut._log.info("Shift in 1")

    dut.ui_in.value = 0b00000011
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00000001

    dut._log.info("Shift in 1")

    dut.ui_in.value = 0b00000011
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00000011

    dut._log.info("Shift in 0")

    dut.ui_in.value = 0b00000010
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00000110

    dut._log.info("Shift in 1")

    dut.ui_in.value = 0b00000011
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00001101

    dut._log.info("Test hold")

    dut.ui_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00001101

    dut._log.info("Reset again")

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0

    dut.rst_n.value = 1

    dut._log.info("Shift register test completed")
