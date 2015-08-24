import time


class CPUSpeedLimitMixin(object):
    def __init__(self, *args, **kwargs):
        self.max_delay = 0.01 # maximum time.sleep() value per burst run
        self.delay = 0 # the current time.sleep() value per burst run

        self.min_burst_count = 10 # minimum outer op count per burst
        self.max_burst_count = 10000 # maximum outer op count per burst

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


    def calc_new_count(self, burst_count, current_value, target_value):
        """
        >>> calc_new_count(burst_count=100, current_value=30, target_value=30)
        100
        >>> calc_new_count(burst_count=100, current_value=40, target_value=20)
        75
        >>> calc_new_count(burst_count=100, current_value=20, target_value=40)
        150
        """
        # log.critical(
        #     "%i op count current: %.4f target: %.4f",
        #     self.outer_burst_op_count, current_value, target_value
        # )
        try:
            new_burst_count = float(burst_count) / float(current_value) * target_value
            new_burst_count += 1 # At least we need one loop ;)
        except ZeroDivisionError:
            return burst_count * 2

        if new_burst_count > self.max_burst_count:
            return self.max_burst_count

        burst_count = (burst_count + new_burst_count) / 2
        if burst_count < self.min_burst_count:
            return self.min_burst_count
        else:
            return int(burst_count)
