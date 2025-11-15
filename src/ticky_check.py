#!/usr/bin/env python3

import re
import csv
from operator import itemgetter

error_count = {}
user_stats = {}

with open("syslog.log", "r") as f:
    for line in f:
        user_match = re.search(r"\(([\w\.\-]+)\)$", line)
        if not user_match:
            continue
        user = user_match.group(1)

        if user not in user_stats:
            user_stats[user] = {"INFO": 0, "ERROR": 0}

        error_match = re.search(r"ticky: ERROR ([\w ']+)", line)
        if error_match:
            error_message = error_match.group(1).strip()
            # Count error globally
            error_count[error_message] = error_count.get(error_message, 0) + 1
            # Count error per user
            user_stats[user]["ERROR"] += 1
        else:
            info_match = re.search(r"ticky: INFO ([\w ']+)", line)
            if info_match:
                user_stats[user]["INFO"] += 1

sorted_errors = sorted(error_count.items(), key=itemgetter(1), reverse=True)
sorted_errors.insert(0, ("Error", "Count"))

sorted_users = sorted(user_stats.items())
sorted_users.insert(0, ("Username", "INFO", "ERROR"))

# Write error_message.csv
with open("error_message.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(sorted_errors)

# Write user_statistics.csv
with open("user_statistics.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for user, stats in sorted_users[1:]:  
        writer.writerow([user, stats["INFO"], stats["ERROR"]])
    # Insert header at the top
    with open("user_statistics.csv", "r") as f_read:
        lines = f_read.readlines()
    with open("user_statistics.csv", "w") as f_write:
        f_write.write("Username,INFO,ERROR\n")
        f_write.writelines(lines)
