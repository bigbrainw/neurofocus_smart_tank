#!/bin/bash
# Fix uv PATH - run this in your terminal

# Add to .zshrc if not already there
if ! grep -q 'export PATH.*\.local/bin' ~/.zshrc 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    echo "✅ Added uv PATH to ~/.zshrc"
else
    echo "✅ uv PATH already in ~/.zshrc"
fi

# Add to current session
export PATH="$HOME/.local/bin:$PATH"

echo ""
echo "✅ uv is now available in this session!"
echo ""
echo "Verify with:"
echo "  uv --version"
echo ""
echo "To make it permanent, restart your terminal or run:"
echo "  source ~/.zshrc"

