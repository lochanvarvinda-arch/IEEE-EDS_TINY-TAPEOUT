```python
# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    clock = Clock(dut.clk, 200, unit="us")
    cocotb.start_soon(clock.start())

    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    dut._log.info("Reset")
    await ClockCycles(dut.clk, 2)

    assert dut.uo_out.value == 0

    dut.rst_n.value = 1

    dut._log.info("Test single bit shift")

    dut.ui_in.value = 0b00000011
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00000001

    dut._log.info("Test second shift")

    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00000011

    dut._log.info("Test third shift")

    dut.ui_in.value = 0b00000001
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00000111

    dut._log.info("Test hold")

    dut.ui_in.value = 0b00000000
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0b00000111

    dut._log.info("Test reset again")

    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)

    assert dut.uo_out.value == 0

    dut.rst_n.value = 1

    dut._log.info("Shift register test completed")
```

### But there's one important correction

Look carefully at our `project.v`:

```verilog
else if (ui_in[1])
  shift_reg <= {shift_reg[6:0], ui_in[0]};
```

That means:

* `ui_in[0]` = **serial input**
* `ui_in[1]` = **shift enable**

So the testbench needs to set the input like this:

```text
ui_in[1] = shift enable
ui_in[0] = serial data
```

For example:

| `ui_in[1]` | `ui_in[0]` | Meaning    |
| ---------: | ---------: | ---------- |
|          0 |          0 | Hold       |
|          0 |          1 | Hold       |
|          1 |          0 | Shift in 0 |
|          1 |          1 | Shift in 1 |

Therefore, **the testbench I just gave needs one small correction**: my values such as `0b00000011` happen to mean both enable and data, but the later `0b00000001` means `shift enable = 0`, so the register would actually hold rather than shift.

Let's use a cleaner testbench that explicitly controls the two bits.

```python
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
```

