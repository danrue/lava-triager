import engine

# This should be able to read in rules.yaml and execute engine.py against each
# rule and ensure that each rule matches its defined output and nothing more.

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

assert (engine.main(46493) ==
"""Lava job https://lkft.validation.linaro.org/scheduler/job/46493
Known issue:
  lkft-ltp-sched issue on juno-r2 and x86
  nfs: server 10.66.16.115 not responding, still trying
  No bug open yet
"""
)
