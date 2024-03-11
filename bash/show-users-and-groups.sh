#!/bin/bash

# Iterate over each user in /etc/passwd
while IFS=: read -r user _; do
    # Display groups for each user
    groups "$user"
done < /etc/passwd
