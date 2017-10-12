import engine

assert (engine.main(46497) ==
"""Lava job https://lkft.validation.linaro.org/scheduler/job/46497
  Known issue:
    ftracetest - see
    - https://bugs.linaro.org/show_bug.cgi?id=3297
    - https://bugs.linaro.org/show_bug.cgi?id=3304
"""
)
