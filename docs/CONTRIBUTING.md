# CloudPad - Contributing Guide

Thank you for considering contributing to CloudPad! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful and inclusive
- Help others learn
- Focus on constructive feedback
- No harassment or discrimination

## How to Contribute

### Reporting Bugs

Use GitHub Issues with this template:

```markdown
**Bug Description:**
[Clear description]

**Steps to Reproduce:**
1. 
2. 
3. 

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Environment:**
- OS: [macOS 13.0 / Windows 11 / Ubuntu 22.04]
- CloudPad Version: [1.0.0]
- Controller: [Thrustmaster HOTAS Warthog]

**Screenshots/Logs:**
[Attach if applicable]
```

### Suggesting Features

Open a GitHub Discussion or Issue:
- Describe the feature clearly
- Explain the use case
- Consider backward compatibility
- Discuss implementation approach

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-awesome-feature
   ```
3. **Make your changes**
   - Follow existing code style
   - Add tests if applicable
   - Update documentation
4. **Test thoroughly**
   ```bash
   python3 test_suite.py
   ```
5. **Commit with clear messages**
   ```bash
   git commit -m "Add support for custom deadzones"
   ```
6. **Push and create PR**
   ```bash
   git push origin feature/my-awesome-feature
   ```

## Development Setup

```bash
# Clone repository
git clone https://github.com/yourname/cloudpad.git
cd cloudpad

# Install dependencies
pip3 install -r requirements.txt

# Run from source
python3 cloudpad.py

# Run tests
python3 test_suite.py
```

## Code Style

- **Python:** Follow PEP 8
- **Naming:** `snake_case` for functions/variables, `PascalCase` for classes
- **Imports:** Stdlib → Third-party → Local
- **Docstrings:** Use for all public methods
- **Type hints:** Preferred but not required

Example:
```python
def calibrate_device(device: DeviceInfo) -> dict:
    """
    Calibrate a HID device and return button mappings.
    
    Args:
        device: DeviceInfo object for the controller
        
    Returns:
        Dictionary mapping Xbox buttons to HID bytes
    """
    pass
```

## Testing Guidelines

### Unit Tests
- Test individual functions
- Mock external dependencies
- Use clear test names

### Integration Tests
- Test component interactions
- Use real HID devices when possible
- Document test setup requirements

### Manual Testing
- Test on actual cloud gaming platforms
- Try different controller types
- Verify UI/UX flows

## Documentation

- Update README.md for user-facing changes
- Update code comments for implementation details
- Add entries to FAQ.md for common questions
- Create/update TESTING.md for new test scenarios

## Pull Request Guidelines

**Good PR:**
- Focused on single feature/fix
- Clear description
- Tests included
- Documentation updated
- No unrelated changes

**PR Description Template:**
```markdown
## Summary
[Brief description]

## Changes
- Change 1
- Change 2

## Testing
- [ ] Tested on macOS
- [ ] Tested on Windows
- [ ] Tested on Linux
- [ ] Added unit tests
- [ ] Manual testing performed

## Screenshots
[If UI changes]

## Related Issues
Fixes #123
```

## Priority Areas

We especially welcome contributions in:
- 🐛 Bug fixes
- 🧪 Test coverage improvements
- 📖 Documentation enhancements
- 🌍 Internationalization (i18n)
- controlled testing
- ♿ Accessibility improvements

## Review Process

1. **Automated checks** run on PR
2. **Maintainer review** (usually within 48h)
3. **Feedback addressed** by contributor
4. **Final approval** and merge
5. **Credit added** to CONTRIBUTORS.md

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Invited to contributor Discord channel

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (see LICENSE file).

## Questions?

- Ask in GitHub Discussions
- Join our Discord: https://discord.gg/cloudpad
- Email: dev@cloudpad.app

## Thank You!

Every contribution, no matter how small, is valued. Thank you for helping make CloudPad better! 🎮

---

**Happy Coding!**
