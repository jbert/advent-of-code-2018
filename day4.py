#!/usr/bin/python3
import re
from collections import namedtuple, defaultdict

Record = namedtuple('Record', ['monthday', 'id', 'sleeps'])

def record_repr(r):
    sleep_str = [" "] * 60
    for sleep in r.sleeps:
        for day in range(sleep[0],sleep[1]):
            sleep_str[day] = '#'
    return format("{:4}: {:02}/{:02} {}".format(r.id, r.monthday[0],r.monthday[1], "".join(sleep_str)))


def main():
    with open("day4-input.txt") as f:
#    with open("day4-test.txt") as f:
        lines = f.readlines()
    schedule = parse_schedule_lines(lines)
    print_schedule(schedule)
    part1(schedule)


def part1(schedule):
    guard_sleep = defaultdict(int)
    for record in schedule:
        this_sleep = sum([finish-start for (start, finish) in record.sleeps])
        guard_sleep[record.id] += this_sleep

    print("GS {}".format(guard_sleep))
    sleepy_guard_info = max(enumerate(guard_sleep.items()), key=lambda t: t[1][1])

    (_, (sleepy_guard_id, _)) = sleepy_guard_info
    print("Guard {} sleepiest".format(sleepy_guard_id))

    times_asleep = [0] * 60
    for record in [r for r in schedule if r.id == sleepy_guard_id]:
        for sleep in record.sleeps:
            for i in range(sleep[0],sleep[1]):
                times_asleep[i] += 1
    print(times_asleep)

    sleepy_minute_info = max(enumerate(times_asleep), key=lambda t: t[1])
    sleepy_minute = sleepy_minute_info[0]
    print("sleepiest minute {}".format(sleepy_minute))
    print("Guard {} most asleep in {} - product {}".format(sleepy_guard_id, sleepy_minute, sleepy_guard_id * sleepy_minute))


def print_schedule(schedule):
    schedule = sorted(schedule,key=lambda r: r.id)
    for r in schedule:
        print(record_repr(r))


def parse_schedule_lines(lines):
    def parse_line(line):
        pattern = r"^\[1518-(\d+)-(\d+) (\d+):(\d+)\] (wakes|falls|Guard) #?(\d+)?"
        match = re.search(pattern, line)
        if not match:
            raise RuntimeError("Failed to match line: {}".format(line))

        (month, day, hour, minute) = [int(s) for s in match.groups()[0:4]]
        event = match.group(5)
        guard_id = match.group(6)
        if guard_id is not None:
            guard_id = int(guard_id)
        return (month, day, hour, minute, event, guard_id)

    events = [parse_line(l) for l in lines]
    events = sorted(events)     # Tuples sort nicely

    schedule = []
    guard_id = None
    sleeps = []

    for event in events:
        (month, day, hour, minute, event, event_guard_id) = event
        if event == "falls":
            sleeps.append([minute])
        elif event == "wakes":
            sleeps[-1].append(minute)
        elif event == "Guard":
            if guard_id is not None:
                record = Record((month, day), guard_id, sleeps)
                schedule.append(record)
            guard_id = event_guard_id
            sleeps = []
        else:
            raise RuntimeError("Unknown event: {}".format(event))
    if guard_id is None:
        raise RuntimeError("None-guard at end")
    record = Record((month, day), guard_id, sleeps)
    schedule.append(record)

    return schedule


if __name__ == "__main__":
    main()
