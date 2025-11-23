# CloudPad - Email Templates

## Support Email Templates

### Template: Installation Help

**Subject:** Re: CloudPad Installation Help

Hi [Name],

Thanks for reaching out! I'd be happy to help you get CloudPad running.

**Quick troubleshooting:**

1. **For macOS:**
   - Right-click CloudPad.app → Open (not double-click on first launch)
   - Grant Input Monitoring permission: System Settings → Privacy & Security → Input Monitoring
   - Add Terminal.app or your browser

2. **For Windows:**
   - Click "More info" → "Run anyway" on SmartScreen warning
   - Run as Administrator if permission errors occur

3. **For Linux:**
   - Make sure you're in the `input` group: `sudo usermod -a -G input $USER`
   - Log out and back in for changes to take effect

**Running from source:**
```bash
cd /path/to/cloudpad
python3 cloudpad.py
```

If you're still having issues, please send me:
- Your operating system version
- Error message (screenshot is helpful)
- Controller model

I'll get you sorted!

Best,
[Your Name]

---

### Template: Calibration Issues

**Subject:** Re: Calibration Not Detecting Buttons

Hi [Name],

Let's troubleshoot your calibration issue.

**Common fixes:**

1. **Make sure you're pressing physical buttons**, not moving axes
   - Avoid joystick/throttle movement during calibration
   - Press distinct buttons (trigger, hat switch, etc.)

2. **Try a different button** if one doesn't register
   - Use "Skip This Button" if needed
   - You can always re-calibrate specific buttons later

3. **Check HID permissions**
   - macOS: System Settings → Privacy & Security → Input Monitoring
   - Linux: `groups` command should show "input"

4. **Restart the calibration**
   - Close the dialog
   - Click "Auto-Calibrate" again
   - Try different buttons

**If still not working:**
- What controller model do you have?
- Does it work in other games/apps?
- Can you send a screenshot of the calibration dialog?

We'll figure this out!

Best,
[Your Name]

---

### Template: Pro Upgrade Question

**Subject:** Re: CloudPad Pro Features

Hi [Name],

Great question about Pro features!

**Currently in Pro (v1.0):**
- ✅ Unlimited device support (Free = 1 device)
- ✅ Multiple controller profiles
- ✅ Profile import/export
- ✅ Priority email support (you!)
- ✅ Early access to new features

**Coming soon to Pro (v1.2):**
- ⏳ Axis calibration (deadzones, curves)
- ⏳ Button macros
- ⏳ Advanced remapping
- ⏳ Per-game profiles

**Is it worth it?**
- If you have 1 controller: Free tier is perfect
- If you have multiple devices (HOTAS + wheel, etc.): Pro is worth it
- If you want to support development: Pro helps a lot!

**One-time purchase** - No subscription, own it forever.

Try the free tier first. If you love it and want more devices, upgrade anytime!

Questions? Just ask!

Best,
[Your Name]

---

### Template: Bug Report Response

**Subject:** Re: Bug Report - [Issue]

Hi [Name],

Thanks for the detailed bug report! This helps improve CloudPad for everyone.

**I've logged this as Issue #[XX] on GitHub:** [link]

**What I need from you:**

1. **Environment:**
   - CloudPad version: [check Help → About]
   - Operating system version:
   - Controller model:

2. **Steps to reproduce:**
   - What were you doing when it crashed?
   - Can you make it happen again?

3. **Logs (if possible):**
   ```bash
   # Run CloudPad from terminal to see error output
   python3 cloudpad.py
   ```
   Send me the error messages

**Workaround (if any):**
[Provide temporary solution if available]

I'll investigate and get back to you within 48 hours with a fix or update.

Thanks for helping make CloudPad better!

Best,
[Your Name]

---

## Marketing Email Templates

### Template: Welcome Email (Pro Purchase)

**Subject:** Welcome to CloudPad Pro! 🎉

Hi [Name]!

Welcome to CloudPad Pro! Your license has been activated.

**Your License:**
- Email: [email]
- License Key: [key]
- Tier: Pro (Lifetime)

**Quick Start:**
1. Your license is already active (if you activated in-app)
2. Connect any controller and calibrate
3. Install browser extension
4. Start cloud gaming!

**Pro Features Now Available:**
✅ Unlimited devices
✅ Multiple profiles
✅ Priority support (email me anytime!)
✅ Early access to v1.2 features

**Resources:**
- Docs: [link]
- Discord (Pro channel): [link]
- YouTube tutorials: [link]

**What's Next?**
- v1.1 (next month): Firefox extension
- v1.2 (3 months): Axis curves, macros
- v1.3 (6 months): Cloud sync

Your purchase directly funds development. Thank you!

Questions? Reply to this email.

Happy gaming! 🎮

Best,
[Your Name]
CloudPad Team

---

### Template: Feature Request Follow-up

**Subject:** Re: Feature Request - [Feature Name]

Hi [Name],

Thanks for the feature request! [Feature Name] is a great idea.

**Current Status:**
- Added to roadmap for v[X.X]
- Upvoted by [X] community members
- Estimated implementation: [timeframe]

**Why it's valuable:**
[Explain benefit]

**Implementation plan:**
[Brief technical approach]

**You can help:**
- Vote on GitHub discussion: [link]
- Share use cases in Discord
- Test beta when available (Pro members get early access!)

I'll keep you updated on progress. Feature requests shape CloudPad's direction, so thank you!

Best,
[Your Name]

---

### Template: Refund Request

**Subject:** Re: Refund Request

Hi [Name],

I'm sorry CloudPad didn't work out for you.

**Refund processed:**
- Amount: $14.99
- Method: [Original payment method]
- Timeframe: 3-5 business days

**Before you go:**
Was there something specific that didn't work? I'd love to improve CloudPad, and your feedback helps.

No pressure - your refund is already processing. But if you want to share:
- What controller were you trying to use?
- What issue did you encounter?
- What would have made it work better?

Thanks for trying CloudPad. Hope to serve you better in the future!

Best,
[Your Name]

---

## Community Email Templates

### Template: Contributor Thank You

**Subject:** Thanks for Contributing to CloudPad!

Hi [Contributor Name],

I just merged your pull request #[XX]! 🎉

**Your contribution:**
- [Brief description]
- Impact: [How it helps]
- Lines changed: [stats]

**What happens now:**
- Included in next release (v[X.X])
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Invited to contributor Discord channel

**Swag (if applicable):**
Major contributors get CloudPad stickers and Pro license (if you don't have one already). Send me your address!

**Keep contributing:**
Other areas that need help:
- [Issue/feature 1]
- [Issue/feature 2]
- [Documentation]

CloudPad is better because of you. Thank you!

Best,
[Your Name]

---

### Template: Community Spotlight

**Subject:** CloudPad Community Spotlight - [Month Year]

Hey CloudPad Community! 👋

Monthly update from CloudPad HQ:

**🎉 This Month:**
- [X] downloads
- [X] GitHub stars
- [X] Discord members
- [X] Pro upgrades

**✨ New Features (v[X.X]):**
- [Feature 1]
- [Feature 2]
- [Bug fixes]

**🏆 Top Contributors:**
1. [@user1] - [contribution]
2. [@user2] - [contribution]
3. [@user3] - [contribution]

**📺 Content:**
- New tutorial: [link]
- Blog post: [link]
- Community showcase: [link]

**🔮 Coming Next Month:**
- [Feature 1]
- [Feature 2]
- [Event/release]

**💬 Feedback Requested:**
We're planning v[X.X] and want YOUR input:
- What feature do you want most?
- What controller should we test next?
- What docs need improvement?

Reply or vote in Discord!

**🙏 Thank You:**
CloudPad exists because of YOU. Every download, star, bug report, and share helps grow the community.

Keep gaming! 🎮

Best,
[Your Name]
CloudPad Team

P.S. - Have a CloudPad success story? Share in #user-setups on Discord!

---

## Auto-Response Templates

### Template: Out of Office

**Subject:** Auto-Reply: Your CloudPad Email

Hi there!

Thanks for contacting CloudPad support!

I'm currently [away/at conference/on vacation] and will respond within [timeframe].

**In the meantime:**
- Check docs: [link]
- Search FAQ: [link]
- Ask Discord: [link]
- Browse GitHub issues: [link]

**Urgent issues?**
- Post in Discord #support channel
- Open GitHub issue for bugs

I'll respond as soon as I'm back!

Best,
[Your Name]
CloudPad Team

---

*All templates customizable. Update [placeholders] with actual information.*
