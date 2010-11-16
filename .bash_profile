export PATH="$PATH:~/bin"

# Check for an interactive session
if [ -z "$PS1" ]; then
    . $HOME/.bashrc
fi
