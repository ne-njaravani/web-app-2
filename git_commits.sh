#!/bin/bash

# Add all changes to staging
git add .

# Commit changes
read -p "Commit description: " desc
git commit -m "$desc"

# Push changes
git push