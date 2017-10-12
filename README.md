# Lava Triage Engine

Given a failing LAVA job ID and a rules file, determine if the job failure is a
known issue.

## Usage

	$ ./engine.py 46497
	Lava job https://lkft.validation.linaro.org/scheduler/job/46497
	  Known issue:
		ftracetest - see
		- https://bugs.linaro.org/show_bug.cgi?id=3297
		- https://bugs.linaro.org/show_bug.cgi?id=3304

## LAVA resources

This job retrieves the following urls for i.e. job 46497 on lkft:

- job results (yaml): https://lkft.validation.linaro.org/results/46497/yaml
- log file: https://lkft.validation.linaro.org/scheduler/job/46497/log_file/plain
- job definition: https://lkft.validation.linaro.org/scheduler/job/46497/definition/plain
