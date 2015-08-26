import time


class CPUSpeedLimitMixin(object):
    max_delay = 0.01 # maximum time.sleep() value per burst run
    delay = 0 # the current time.sleep() value per burst run

    def delayed_burst_run(self, target_cycles_per_sec):
        """ Run CPU not faster than given speedlimit """
        old_cycles = self.cycles
        start_time = time.time()

        self.burst_run()

        is_duration = time.time() - start_time
        new_cycles = self.cycles - old_cycles
        try:
            is_cycles_per_sec = new_cycles / is_duration
        except ZeroDivisionError:
            pass
        else:
            should_burst_duration = is_cycles_per_sec / target_cycles_per_sec
            target_duration = should_burst_duration * is_duration
            delay = target_duration - is_duration
            if delay > 0:
                if delay > self.max_delay:
                    self.delay = self.max_delay
                else:
                    self.delay = delay
                time.sleep(self.delay)

        self.call_sync_callbacks()
