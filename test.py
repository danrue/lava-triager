import engine

assert (engine.main(46497) ==
"""Lava job https://lkft.validation.linaro.org/scheduler/job/46497
  Known issue:
    LKFT: linux-next: x15: kselftest: ftracetest hangs forever
    - https://bugs.linaro.org/show_bug.cgi?id=3297
    - https://bugs.linaro.org/show_bug.cgi?id=3304
"""
)

assert (engine.main(46575) ==
"""Lava job https://lkft.validation.linaro.org/scheduler/job/46575
  Known issue:
    LTP: 20170929: hikey: fanotify07 sometimes causes kernel trace and LTP to hang
    - https://bugs.linaro.org/show_bug.cgi?id=3303
"""
)
