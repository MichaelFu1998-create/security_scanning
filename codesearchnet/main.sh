for file in *.py; do
    bandit "$file"
done