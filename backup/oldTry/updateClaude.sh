  # Install nvm if needed
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

  # Restart shell or:
  source ~/.bashrc

  # Install and use Node 22
  nvm install 22
  nvm use 22
  nvm alias default 22

  # Then install Claude Code (no sudo needed with nvm)
  npm i -g @anthropic-ai/claude-code